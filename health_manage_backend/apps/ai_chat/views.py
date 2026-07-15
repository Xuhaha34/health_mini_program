from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.db.models import Max, Count
import uuid

from utils.common_response import success_response, error_response
from utils.ai_proxy import call_ai_api, get_provider_config
from .models import ChatHistory
from .serializers import (
    ChatHistorySerializer,
    ChatRequestSerializer,
    ChatResponseSerializer,
)


def _gather_user_profile(user) -> dict:
    """聚合用户体征数据（体重 / 身高 / 年龄 / 性别 / 健康计划数），传给大模型做个性化回答"""
    profile = {}
    try:
        if getattr(user, "birthday", None):
            from django.utils import timezone
            today = timezone.localdate()
            bd = user.birthday
            profile["年龄"] = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    except Exception:
        pass

    if getattr(user, "gender", None):
        g = str(user.gender)
        if g.lower() in ("male", "男", "0"):
            profile["性别"] = "男"
        elif g.lower() in ("female", "女", "1"):
            profile["性别"] = "女"
        else:
            profile["性别"] = g

    # —— 用户体重 / 身高（从 health_record 尝试查询）——
    try:
        from apps.health_record.models import HealthRecord
        latest = (
            HealthRecord.objects.filter(user=user)
            .order_by("-recorded_at")
            .only("weight", "height", "bmi", "blood_pressure_systolic", "blood_pressure_diastolic", "blood_glucose")
            .first()
        )
        if latest:
            if latest.weight:
                profile["体重"] = f"{latest.weight}kg"
            if latest.height:
                profile["身高"] = f"{latest.height}cm"
            if latest.bmi:
                profile["BMI"] = str(latest.bmi)
            if latest.blood_pressure_systolic and latest.blood_pressure_diastolic:
                profile["血压"] = f"{latest.blood_pressure_systolic}/{latest.blood_pressure_diastolic} mmHg"
            if latest.blood_glucose:
                profile["血糖"] = f"{latest.blood_glucose} mmol/L"
    except Exception:
        pass

    # —— 用户健康计划数（作为活跃度指标）——
    try:
        from apps.health_plan.models import HealthPlan
        plan_count = HealthPlan.objects.filter(user=user).count()
        if plan_count > 0:
            profile["健康计划数"] = plan_count
    except Exception:
        pass

    return profile


class AIChatView(APIView):
    """AI健康问答接口"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message=serializer.errors, code=400)

        user_message = serializer.validated_data['message']
        session_id = serializer.validated_data.get('session_id') or str(uuid.uuid4())

        try:
            # 保存用户消息
            ChatHistory.objects.create(
                user=request.user,
                role='user',
                message=user_message,
                session_id=session_id,
            )

            # 读取最近 6 条对话历史（给大模型上下文）
            recent_history = list(
                ChatHistory.objects.filter(
                    user=request.user, session_id=session_id
                )
                .order_by('-created_at')[:6]
            )[::-1]  # 倒序取再反转：最早的在前
            history_list = [
                {"role": h.role, "content": h.message}
                for h in recent_history
                if h.role in ("user", "assistant") and h.message != user_message
            ]

            # 聚合用户体征数据
            user_profile = _gather_user_profile(request.user)

            # 调用AI接口（统一回落到本地知识库）
            ai_result = call_ai_api(user_message, history=history_list, user_profile=user_profile)
            ai_reply = ai_result["reply"]

            # 保存AI回复
            ChatHistory.objects.create(
                user=request.user,
                role='assistant',
                message=ai_reply,
                session_id=session_id,
            )

            return success_response(data={
                'reply': ai_reply,
                'session_id': session_id,
                'provider': ai_result['provider'],
                'model': ai_result['model'],
                'from_external': ai_result['from_external'],
                'user_profile': user_profile,
            })

        except Exception as e:
            return error_response(message=f'AI服务异常：{str(e)}', code=500)


class AIChatConfigView(APIView):
    """返回当前 AI 配置（不返回密钥），供前端调试显示"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return success_response(data=get_provider_config())


class ChatHistoryListView(generics.ListAPIView):
    """对话历史列表"""
    serializer_class = ChatHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['session_id']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return ChatHistory.objects.filter(user=self.request.user)


class ClearChatHistoryView(APIView):
    """清空对话历史"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        session_id = request.query_params.get('session_id')

        if session_id:
            ChatHistory.objects.filter(
                user=request.user,
                session_id=session_id,
            ).delete()
        else:
            ChatHistory.objects.filter(user=request.user).delete()

        return success_response(message='清空成功')


class ChatSessionListView(APIView):
    """会话列表（返回所有session及最新消息）"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sessions = (
            ChatHistory.objects.filter(user=request.user)
            .values('session_id')
            .annotate(last_time=Max('created_at'), msg_count=Count('id'))
            .order_by('-last_time')
        )

        result = []
        for s in sessions:
            first_msg = ChatHistory.objects.filter(
                user=request.user, session_id=s['session_id'], role='user'
            ).order_by('created_at').first()
            title = first_msg.message[:20] if first_msg else '新对话'
            result.append({
                'id': s['session_id'],
                'title': title,
                'last_time': s['last_time'].strftime('%Y-%m-%d %H:%M'),
                'msg_count': s['msg_count'],
            })
        return success_response(data=result)