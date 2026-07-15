from django.db import models


class NewsCategory(models.Model):
    """资讯分类"""
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'health_news_newscategory'
        verbose_name = '资讯分类'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class News(models.Model):
    """健康资讯"""
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news', verbose_name='分类')
    title = models.CharField(max_length=200, verbose_name='标题')
    cover_image = models.ImageField(upload_to='news/%Y/%m/', blank=True, null=True, verbose_name='封面图片')
    summary = models.TextField(blank=True, null=True, verbose_name='摘要')
    content = models.TextField(verbose_name='内容')
    author = models.CharField(max_length=50, blank=True, null=True, verbose_name='作者')
    source = models.CharField(max_length=100, blank=True, null=True, verbose_name='来源')
    view_count = models.IntegerField(default=0, verbose_name='浏览量')
    is_published = models.BooleanField(default=False, verbose_name='是否发布')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'health_news_news'
        verbose_name = '健康资讯'
        verbose_name_plural = verbose_name
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['category', 'is_published']),
            models.Index(fields=['published_at']),
        ]

    def __str__(self):
        return self.title
