from rest_framework import routers
from .views import UserViewSet, RegisterView, create_checkout_session, stripe_webhook, change_password, me
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('stripe-webhook/', stripe_webhook, name='stripe_webhook'),
    path('change-password/', change_password, name='change_password'),
    path('me/', me, name='me'),
] 