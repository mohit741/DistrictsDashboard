from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from DashboardApi import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'add', views.HealthViewSet,base_name='health')
# router.register(r'add', views.HealthUploadView,base_name='health')
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('health/', views.HealthUploadView.as_view()),
    path('query/', views.BlockWiseList.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
