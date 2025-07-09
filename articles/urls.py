from rest_framework import routers
from .views import ArticleViewSet, TopicViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'topics', TopicViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 