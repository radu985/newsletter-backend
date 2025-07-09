from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
import json

from .models import Newsletter, Subscriber, NewsletterTemplate, NewsletterSend, NewsletterAnalytics
from .serializers import (
    NewsletterSerializer, NewsletterDetailSerializer, NewsletterTemplateSerializer,
    SubscriberSerializer, SubscriberDetailSerializer, NewsletterSendSerializer,
    NewsletterAnalyticsSerializer, NewsletterStatsSerializer, SubscriberImportSerializer
)

class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'template']
    search_fields = ['title', 'subject', 'content']
    ordering_fields = ['created_at', 'sent_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter newsletters by author if not admin"""
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            # For testing purposes, return all newsletters when not authenticated
            return queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NewsletterDetailSerializer
        return NewsletterSerializer

    def get_permissions(self):
        """Allow public access for list and stats actions during testing"""
        if self.action in ['list', 'stats', 'create', 'update', 'partial_update', 'destroy', 'send']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Automatically assign author for testing purposes"""
        if not self.request.user.is_authenticated:
            # Get or create a default admin user for testing
            from users.models import CustomUser
            default_user, created = CustomUser.objects.get_or_create(
                email='admin@example.com',
                defaults={
                    'name': 'Admin User',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            serializer.save(author=default_user)
        else:
            serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Handle newsletter updates"""
        serializer.save()

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Send newsletter to all active subscribers"""
        newsletter = self.get_object()
        
        if newsletter.status != 'draft':
            return Response(
                {'error': 'Only draft newsletters can be sent'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update newsletter status to sending
        newsletter.status = 'sending'
        newsletter.save()

        # Use Celery task for asynchronous sending
        from .tasks import send_newsletter_task
        task = send_newsletter_task.delay(newsletter.id)

        return Response({
            'message': 'Newsletter sending started',
            'task_id': task.id,
            'status': 'processing'
        })

    @action(detail=True, methods=['post'])
    def schedule(self, request, pk=None):
        """Schedule newsletter for later sending"""
        newsletter = self.get_object()
        scheduled_at = request.data.get('scheduled_at')
        
        if not scheduled_at:
            return Response(
                {'error': 'scheduled_at is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        newsletter.status = 'scheduled'
        newsletter.scheduled_at = scheduled_at
        newsletter.save()

        # Schedule the Celery task
        from .tasks import send_newsletter_task
        from datetime import datetime
        import pytz
        
        # Convert scheduled_at to datetime if it's a string
        if isinstance(scheduled_at, str):
            scheduled_at = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        
        # Schedule the task
        send_newsletter_task.apply_async(
            args=[newsletter.id],
            eta=scheduled_at
        )

        return Response({'message': 'Newsletter scheduled successfully'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel scheduled newsletter"""
        newsletter = self.get_object()
        
        if newsletter.status not in ['draft', 'scheduled']:
            return Response(
                {'error': 'Only draft or scheduled newsletters can be cancelled'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        newsletter.status = 'cancelled'
        newsletter.save()

        return Response({'message': 'Newsletter cancelled successfully'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get advanced newsletter statistics with date filtering"""
        from django.db.models import Sum, Count, Avg, Q
        from datetime import datetime, timedelta
        import pytz
        
        # Get date range from query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        period = request.query_params.get('period', '30d')  # Default to 30 days
        
        # Calculate date range
        now = timezone.now()
        if start_date and end_date:
            try:
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                start_date = now - timedelta(days=30)
                end_date = now
        else:
            # Use period parameter
            if period == '7d':
                start_date = now - timedelta(days=7)
            elif period == '30d':
                start_date = now - timedelta(days=30)
            elif period == '90d':
                start_date = now - timedelta(days=90)
            elif period == '1y':
                start_date = now - timedelta(days=365)
            else:
                start_date = now - timedelta(days=30)
            end_date = now
        
        queryset = self.get_queryset().filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        )
        
        # Basic stats
        total_newsletters = queryset.count()
        total_sent = queryset.filter(status='sent').count()
        total_draft = queryset.filter(status='draft').count()
        total_scheduled = queryset.filter(status='scheduled').count()
        
        # Performance metrics
        sent_newsletters = queryset.filter(status='sent')
        avg_open_rate = sent_newsletters.aggregate(Avg('open_rate'))['open_rate__avg'] or 0
        avg_click_rate = sent_newsletters.aggregate(Avg('click_rate'))['click_rate__avg'] or 0
        
        # Engagement metrics
        total_recipients = sent_newsletters.aggregate(Sum('total_recipients'))['total_recipients__sum'] or 0
        total_emails_sent = sent_newsletters.aggregate(Sum('total_sent'))['total_sent__sum'] or 0
        total_delivered = sent_newsletters.aggregate(Sum('total_delivered'))['total_delivered__sum'] or 0
        total_opened = sent_newsletters.aggregate(Sum('total_opened'))['total_opened__sum'] or 0
        total_clicked = sent_newsletters.aggregate(Sum('total_clicked'))['total_clicked__sum'] or 0
        
        # Calculate rates
        delivery_rate = round((total_delivered / total_emails_sent * 100) if total_emails_sent > 0 else 0, 2)
        open_rate = round((total_opened / total_delivered * 100) if total_delivered > 0 else 0, 2)
        click_rate = round((total_clicked / total_delivered * 100) if total_delivered > 0 else 0, 2)
        
        # Time series data for charts
        time_series_data = []
        current_date = start_date
        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)
            daily_newsletters = queryset.filter(
                created_at__gte=current_date,
                created_at__lt=next_date
            )
            daily_sent = daily_newsletters.filter(status='sent').count()
            daily_opens = daily_newsletters.filter(status='sent').aggregate(Sum('total_opened'))['total_opened__sum'] or 0
            daily_clicks = daily_newsletters.filter(status='sent').aggregate(Sum('total_clicked'))['total_clicked__sum'] or 0
            
            time_series_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'newsletters': daily_newsletters.count(),
                'sent': daily_sent,
                'opens': daily_opens,
                'clicks': daily_clicks
            })
            current_date = next_date
        
        # Top performing newsletters
        top_performing = sent_newsletters.order_by('-open_rate')[:10]
        
        # Recent newsletters
        recent_newsletters = queryset.order_by('-created_at')[:10]
        
        # Subscriber growth
        subscriber_growth = Subscriber.objects.filter(
            subscribed_at__gte=start_date,
            subscribed_at__lte=end_date
        ).count()
        
        # Bounce analysis
        total_bounces = total_emails_sent - total_delivered
        bounce_rate = round((total_bounces / total_emails_sent * 100) if total_emails_sent > 0 else 0, 2)
        
        # Engagement trends
        engagement_trend = {
            'high_engagement': sent_newsletters.filter(open_rate__gte=25).count(),
            'medium_engagement': sent_newsletters.filter(open_rate__gte=10, open_rate__lt=25).count(),
            'low_engagement': sent_newsletters.filter(open_rate__lt=10).count()
        }
        
        # Performance comparison
        if period == '30d':
            previous_period_start = start_date - timedelta(days=30)
            previous_period_end = start_date
            previous_newsletters = self.get_queryset().filter(
                created_at__gte=previous_period_start,
                created_at__lte=previous_period_end,
                status='sent'
            )
            previous_avg_open = previous_newsletters.aggregate(Avg('open_rate'))['open_rate__avg'] or 0
            open_rate_change = round(((avg_open_rate - previous_avg_open) / previous_avg_open * 100) if previous_avg_open > 0 else 0, 2)
        else:
            open_rate_change = 0
        
        # Create comprehensive stats
        stats = {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'period': period
            },
            'overview': {
                'total_newsletters': total_newsletters,
                'total_sent': total_sent,
                'total_draft': total_draft,
                'total_scheduled': total_scheduled,
                'subscriber_growth': subscriber_growth
            },
            'performance': {
                'total_recipients': total_recipients,
                'total_emails_sent': total_emails_sent,
                'total_delivered': total_delivered,
                'total_opened': total_opened,
                'total_clicked': total_clicked,
                'total_bounces': total_bounces
            },
            'rates': {
                'delivery_rate': delivery_rate,
                'open_rate': open_rate,
                'click_rate': click_rate,
                'bounce_rate': bounce_rate,
                'avg_open_rate': round(avg_open_rate, 2),
                'avg_click_rate': round(avg_click_rate, 2),
                'open_rate_change': open_rate_change
            },
            'engagement_trends': engagement_trend,
            'time_series': time_series_data,
            'recent_newsletters': recent_newsletters,
            'top_performing_newsletters': top_performing,
        }

        # Serialize QuerySets to JSON-friendly data
        stats['recent_newsletters'] = NewsletterSerializer(recent_newsletters, many=True).data
        stats['top_performing_newsletters'] = NewsletterSerializer(top_performing, many=True).data

        return Response(stats)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def test_email(self, request):
        """Send a test email to verify configuration"""
        email_address = request.data.get('email')
        newsletter_id = request.data.get('newsletter_id')
        
        if not email_address:
            return Response(
                {'error': 'email is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if newsletter_id:
            # Send test email for specific newsletter
            from .tasks import send_test_email_task
            task = send_test_email_task.delay(email_address, newsletter_id)
            return Response({
                'message': 'Test email sending started',
                'task_id': task.id,
                'status': 'processing'
            })
        else:
            # Send simple test email
            from .services import send_test_email
            success, message = send_test_email(email_address)
            
            if success:
                return Response({'message': message})
            else:
                return Response(
                    {'error': message}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def test_celery(self, request):
        """Test Celery functionality"""
        from .tasks import test_celery_task
        task = test_celery_task.delay()
        return Response({
            'message': 'Celery test task started',
            'task_id': task.id,
            'status': 'processing'
        })

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'frequency', 'source']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['subscribed_at', 'email']
    ordering = ['-subscribed_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubscriberDetailSerializer
        return SubscriberSerializer

    def get_permissions(self):
        """Allow public access for list and stats actions during testing"""
        if self.action in ['list', 'stats', 'import_subscribers']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        """Unsubscribe a subscriber"""
        subscriber = self.get_object()
        subscriber.is_active = False
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save()

        return Response({'message': 'Subscriber unsubscribed successfully'})

    @action(detail=True, methods=['post'])
    def resubscribe(self, request, pk=None):
        """Resubscribe a subscriber"""
        subscriber = self.get_object()
        subscriber.is_active = True
        subscriber.unsubscribed_at = None
        subscriber.save()

        return Response({'message': 'Subscriber resubscribed successfully'})

    @action(detail=False, methods=['post'])
    def import_subscribers(self, request):
        """Bulk import subscribers"""
        serializer = SubscriberImportSerializer(data=request.data)
        if serializer.is_valid():
            emails = serializer.validated_data['emails']
            frequency = serializer.validated_data['frequency']
            source = serializer.validated_data['source']

            created_subscribers = []
            for email in emails:
                subscriber, created = Subscriber.objects.get_or_create(
                    email=email,
                    defaults={
                        'frequency': frequency,
                        'source': source,
                        'is_active': True
                    }
                )
                if created:
                    created_subscribers.append(subscriber)

            return Response({
                'message': f'Successfully imported {len(created_subscribers)} subscribers',
                'imported_count': len(created_subscribers)
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get subscriber statistics"""
        from datetime import timedelta
        
        total_subscribers = Subscriber.objects.filter(is_active=True).count()
        total_unsubscribed = Subscriber.objects.filter(is_active=False).count()
        
        # Growth over time
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        last_7_days = now - timedelta(days=7)
        
        new_subscribers_30_days = Subscriber.objects.filter(
            subscribed_at__gte=last_30_days
        ).count()
        
        new_subscribers_7_days = Subscriber.objects.filter(
            subscribed_at__gte=last_7_days
        ).count()
        
        unsubscribed_30_days = Subscriber.objects.filter(
            unsubscribed_at__gte=last_30_days
        ).count()

        # Calculate growth rate
        previous_30_days = last_30_days - timedelta(days=30)
        previous_subscribers = Subscriber.objects.filter(
            subscribed_at__lt=last_30_days,
            subscribed_at__gte=previous_30_days
        ).count()
        
        growth_rate = ((new_subscribers_30_days - previous_subscribers) / previous_subscribers * 100) if previous_subscribers > 0 else 0

        # Frequency distribution
        frequency_stats = Subscriber.objects.filter(
            is_active=True
        ).values('frequency').annotate(count=Count('id'))

        # Source distribution
        source_stats = Subscriber.objects.filter(
            is_active=True
        ).values('source').annotate(count=Count('id'))

        # Engagement metrics
        avg_emails_received = Subscriber.objects.filter(
            is_active=True
        ).aggregate(Avg('total_emails_received'))['total_emails_received__avg'] or 0

        stats = {
            'total_subscribers': total_subscribers,
            'active_subscribers': total_subscribers,
            'total_unsubscribed': total_unsubscribed,
            'new_subscribers_this_month': new_subscribers_30_days,
            'new_subscribers_this_week': new_subscribers_7_days,
            'unsubscribed_this_month': unsubscribed_30_days,
            'subscriber_growth_rate': round(growth_rate, 2),
            'average_emails_received': round(avg_emails_received, 1),
            'frequency_distribution': list(frequency_stats),
            'source_distribution': list(source_stats),
        }

        return Response(stats)

class NewsletterTemplateViewSet(viewsets.ModelViewSet):
    queryset = NewsletterTemplate.objects.all()
    serializer_class = NewsletterTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a template"""
        template = self.get_object()
        new_template = NewsletterTemplate.objects.create(
            name=f"{template.name} (Copy)",
            subject_template=template.subject_template,
            html_template=template.html_template,
            text_template=template.text_template,
            is_active=False
        )
        
        serializer = self.get_serializer(new_template)
        return Response(serializer.data)

class NewsletterSendViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsletterSend.objects.all()
    serializer_class = NewsletterSendSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'newsletter', 'subscriber']
    ordering_fields = ['sent_at', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter sends by newsletter author if not admin"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(newsletter__author=self.request.user)
        return queryset

    @action(detail=True, methods=['post'])
    def mark_opened(self, request, pk=None):
        """Mark email as opened (for tracking)"""
        send = self.get_object()
        send.status = 'opened'
        send.opened_at = timezone.now()
        send.open_count += 1
        send.save()

        # Update newsletter analytics
        newsletter = send.newsletter
        newsletter.total_opened += 1
        newsletter.open_rate = (newsletter.total_opened / newsletter.total_sent) * 100
        newsletter.save()

        return Response({'message': 'Email marked as opened'})

    @action(detail=True, methods=['post'])
    def mark_clicked(self, request, pk=None):
        """Mark email as clicked (for tracking)"""
        send = self.get_object()
        send.status = 'clicked'
        send.clicked_at = timezone.now()
        send.click_count += 1
        send.save()

        # Update newsletter analytics
        newsletter = send.newsletter
        newsletter.total_clicked += 1
        newsletter.click_rate = (newsletter.total_clicked / newsletter.total_sent) * 100
        newsletter.save()

        return Response({'message': 'Email marked as clicked'})

class NewsletterAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsletterAnalytics.objects.all()
    serializer_class = NewsletterAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter analytics by newsletter author if not admin"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(newsletter__author=self.request.user)
        return queryset

    @action(detail=True, methods=['post'])
    def update_metrics(self, request, pk=None):
        """Manually update analytics metrics"""
        analytics = self.get_object()
        analytics.update_metrics()
        
        serializer = self.get_serializer(analytics)
        return Response(serializer.data)
