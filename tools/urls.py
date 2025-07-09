from rest_framework import routers
from .views import ToolViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'tools', ToolViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 