from rest_framework import serializers
from .models import NewsCategory, News


class NewsCategorySerializer(serializers.ModelSerializer):
    """资讯分类序列化器"""
    class Meta:
        model = NewsCategory
        fields = '__all__'


class NewsListSerializer(serializers.ModelSerializer):
    """资讯列表序列化器（轻量）"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'cover_image', 'summary', 'category', 'category_name',
                  'source', 'author', 'view_count', 'published_at']


class NewsDetailSerializer(serializers.ModelSerializer):
    """资讯详情序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = News
        fields = '__all__'