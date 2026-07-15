from django.urls import path
from .views import HealthPlanListView, HealthPlanDetailView, HealthPlanCheckInView

urlpatterns = [
    path('', HealthPlanListView.as_view(), name='plan-list'),
    path('<int:pk>/', HealthPlanDetailView.as_view(), name='plan-detail'),
    path('<int:pk>/checkin/', HealthPlanCheckInView.as_view(), name='plan-checkin'),
]