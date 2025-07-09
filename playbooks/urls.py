from rest_framework import routers
from .views import PlaybookViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'playbooks', PlaybookViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 