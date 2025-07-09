from rest_framework import routers
from .views import RevenueReportViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'reports', RevenueReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 