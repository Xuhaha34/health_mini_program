from django.urls import path
from .views import (
    NewsCategoryListView, NewsListView, NewsDetailView,
    NewsManageListView, NewsManageDetailView
)

urlpatterns = [
    # 小程序端接口（公开）
    path('categories/', NewsCategoryListView.as_view(), name='news-categories'),
    path('articles/', NewsListView.as_view(), name='news-articles'),
    path('articles/<int:pk>/', NewsDetailView.as_view(), name='news-articles-detail'),
    path('', NewsListView.as_view(), name='news-list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news-detail'),

    # 管理后台接口（管理员）
    path('manage/', NewsManageListView.as_view(), name='news-manage-list'),
    path('manage/<int:pk>/', NewsManageDetailView.as_view(), name='news-manage-detail'),
]