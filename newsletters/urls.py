from rest_framework import routers
from .views import (
    NewsletterViewSet, SubscriberViewSet, NewsletterTemplateViewSet,
    NewsletterSendViewSet, NewsletterAnalyticsViewSet
)
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'newsletters', NewsletterViewSet)
router.register(r'subscribers', SubscriberViewSet)
router.register(r'templates', NewsletterTemplateViewSet)
router.register(r'sends', NewsletterSendViewSet)
router.register(r'analytics', NewsletterAnalyticsViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 