from rest_framework import serializers
from .models import ChatHistory


class ChatHistorySerializer(serializers.ModelSerializer):
    """对话历史序列化器"""
    class Meta:
        model = ChatHistory
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ChatRequestSerializer(serializers.Serializer):
    """AI问答请求序列化器"""
    message = serializers.CharField(required=True, label='用户消息')
    session_id = serializers.CharField(required=False, allow_blank=True, label='会话ID')


class ChatResponseSerializer(serializers.Serializer):
    """AI问答响应序列化器"""
    reply = serializers.CharField(label='AI回复')
    session_id = serializers.CharField(label='会话ID')
