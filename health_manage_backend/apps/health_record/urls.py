from django.urls import path
from .views import (
    BodyDataListView, BodyDataDetailView, BodyDataStatsView,
    DietRecordListView, DietRecordDetailView, DietStatsView,
    SportRecordListView, SportRecordDetailView, SportStatsView,
    OverallStatisticsView, RecentActivitiesView,
)

urlpatterns = [
    # 体征数据
    path('body-data/', BodyDataListView.as_view(), name='bodydata-list'),
    path('body-data/stats/', BodyDataStatsView.as_view(), name='bodydata-stats'),
    path('body-data/<int:pk>/', BodyDataDetailView.as_view(), name='bodydata-detail'),

    # 饮食记录
    path('diet/', DietRecordListView.as_view(), name='diet-list'),
    path('diet/stats/', DietStatsView.as_view(), name='diet-stats'),
    path('diet/<int:pk>/', DietRecordDetailView.as_view(), name='diet-detail'),

    # 运动记录
    path('sport/', SportRecordListView.as_view(), name='sport-list'),
    path('sport/stats/', SportStatsView.as_view(), name='sport-stats'),
    path('sport/<int:pk>/', SportRecordDetailView.as_view(), name='sport-detail'),

    # 综合统计（小程序首页）
    path('statistics/', OverallStatisticsView.as_view(), name='overall-statistics'),

    # 最近活动（Dashboard）
    path('recent-activities/', RecentActivitiesView.as_view(), name='recent-activities'),
]