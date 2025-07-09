from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import stripe
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.

#stripe.api_key = settings.STRIPE_SECRET_KEY

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Try to send welcome email (optional)
            try:
                send_mail(
                    "Welcome to Newsletter Platform!",
                    "Thank you for registering. Enjoy our content!",
                    "no-reply@yourdomain.com",
                    [serializer.data["email"]],
                    fail_silently=True,  # Don't fail if email is not configured
                )
            except Exception as e:
                # Log the error but don't fail the registration
                print(f"Failed to send welcome email: {e}")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Premium Upgrade'},
                'unit_amount': 1000,  # $10.00
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:3000/upgrade?success=true',
        cancel_url='http://localhost:3000/upgrade?canceled=true',
        customer_email=request.user.email,
    )
    return Response({'id': session.id})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        email = session.get('customer_email')
        from users.models import CustomUser
        try:
            user = CustomUser.objects.get(email=email)
            user.is_premium = True
            user.save()
            # Try to send upgrade email (optional)
            try:
                send_mail(
                    "Your account has been upgraded!",
                    "Thank you for upgrading to premium. Enjoy exclusive features!",
                    "no-reply@yourdomain.com",
                    [user.email],
                    fail_silently=True,  # Don't fail if email is not configured
                )
            except Exception as e:
                # Log the error but don't fail the webhook
                print(f"Failed to send upgrade email: {e}")
        except CustomUser.DoesNotExist:
            pass

    return HttpResponse(status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if not user.check_password(old_password):
        return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({'detail': 'Password changed successfully.'})

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserSerializer(user, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

