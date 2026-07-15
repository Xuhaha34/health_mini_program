from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from utils.common_response import success_response, error_response
from .models import NewsCategory, News
from .serializers import NewsCategorySerializer, NewsListSerializer, NewsDetailSerializer


class NewsCategoryListView(generics.ListAPIView):
    """资讯分类列表"""
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    permission_classes = [permissions.AllowAny]


class NewsListView(generics.ListAPIView):
    """资讯列表（小程序端）"""
    serializer_class = NewsListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_published']
    search_fields = ['title', 'summary']
    ordering_fields = ['published_at', 'view_count']
    ordering = ['-published_at']

    def get_queryset(self):
        # 只返回已发布的资讯
        return News.objects.filter(is_published=True)


class NewsDetailView(APIView):
    """资讯详情"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            news = News.objects.get(pk=pk)
            
            # 增加浏览量
            news.view_count += 1
            news.save(update_fields=['view_count'])
            
            serializer = NewsDetailSerializer(news)
            return success_response(data=serializer.data)
        except News.DoesNotExist:
            return error_response(message='资讯不存在', code=404)


# ==================== 管理后台接口 ====================
class NewsManageListView(generics.ListCreateAPIView):
    """资讯管理列表/创建（管理员）"""
    serializer_class = NewsDetailSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_published']
    search_fields = ['title']
    ordering = ['-created_at']

    def get_queryset(self):
        return News.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(
                data=NewsDetailSerializer(instance).data,
                message='创建成功'
            )
        return error_response(message=serializer.errors, code=400)


class NewsManageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """资讯管理详情/更新/删除（管理员）"""
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return success_response(data=response.data, message='更新成功')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return success_response(message='删除成功')
