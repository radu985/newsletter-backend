from rest_framework import serializers
from .models import Newsletter, Subscriber, NewsletterTemplate, NewsletterSend, NewsletterAnalytics
from users.serializers import UserSerializer

class NewsletterTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterTemplate
        fields = '__all__'

class SubscriberSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Subscriber
        fields = '__all__'
        read_only_fields = ('subscribed_at', 'unsubscribed_at', 'total_emails_received', 
                           'total_emails_opened', 'total_emails_clicked', 'last_email_sent', 
                           'last_email_opened')

class NewsletterSendSerializer(serializers.ModelSerializer):
    subscriber_email = serializers.ReadOnlyField(source='subscriber.email')
    subscriber_name = serializers.ReadOnlyField(source='subscriber.full_name')
    
    class Meta:
        model = NewsletterSend
        fields = '__all__'
        read_only_fields = ('sent_at', 'delivered_at', 'opened_at', 'clicked_at', 
                           'message_id', 'provider_response', 'open_count', 'click_count')

class NewsletterAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterAnalytics
        fields = '__all__'
        read_only_fields = ('updated_at',)

class NewsletterSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    template = NewsletterTemplateSerializer(read_only=True)
    template_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    analytics = NewsletterAnalyticsSerializer(read_only=True)
    sends_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Newsletter
        fields = '__all__'
        read_only_fields = ('author', 'sent_at', 'total_recipients', 'total_sent', 
                           'total_delivered', 'total_opened', 'total_clicked', 
                           'open_rate', 'click_rate', 'created_at', 'updated_at')

    def get_sends_count(self, obj):
        return obj.sends.count()

    def create(self, validated_data):
        # Only set author if user is authenticated
        if self.context['request'].user.is_authenticated:
            validated_data['author'] = self.context['request'].user
        # If not authenticated, let the view's perform_create handle it
        return super().create(validated_data)

    def validate_status(self, value):
        """Validate status transitions"""
        if self.instance:
            current_status = self.instance.status
            if current_status == 'sent' and value != 'sent':
                raise serializers.ValidationError("Cannot change status of sent newsletter")
            if current_status == 'cancelled' and value != 'cancelled':
                raise serializers.ValidationError("Cannot change status of cancelled newsletter")
        return value

class NewsletterDetailSerializer(NewsletterSerializer):
    """Extended serializer for newsletter detail view with sends"""
    sends = NewsletterSendSerializer(many=True, read_only=True)
    
    class Meta(NewsletterSerializer.Meta):
        fields = list(NewsletterSerializer.Meta.fields) + ['sends']

class NewsletterSendDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for newsletter sends with subscriber info"""
    subscriber = SubscriberSerializer(read_only=True)
    newsletter_title = serializers.ReadOnlyField(source='newsletter.title')
    
    class Meta:
        model = NewsletterSend
        fields = '__all__'

class SubscriberDetailSerializer(SubscriberSerializer):
    """Extended serializer for subscriber detail with newsletter history"""
    newsletter_sends = NewsletterSendSerializer(many=True, read_only=True)
    total_newsletters_received = serializers.SerializerMethodField()
    
    class Meta(SubscriberSerializer.Meta):
        fields = list(SubscriberSerializer.Meta.fields) + ['newsletter_sends', 'total_newsletters_received']

    def get_total_newsletters_received(self, obj):
        return obj.newsletter_sends.count()

class NewsletterStatsSerializer(serializers.Serializer):
    """Serializer for newsletter statistics"""
    total_newsletters = serializers.IntegerField()
    total_subscribers = serializers.IntegerField()
    total_sent = serializers.IntegerField()
    total_recipients = serializers.IntegerField()
    total_emails_sent = serializers.IntegerField()
    average_open_rate = serializers.FloatField()
    average_click_rate = serializers.FloatField()
    delivery_rate = serializers.FloatField()
    recent_newsletters = NewsletterSerializer(many=True)
    top_performing_newsletters = NewsletterSerializer(many=True)

class SubscriberImportSerializer(serializers.Serializer):
    """Serializer for bulk subscriber import"""
    emails = serializers.ListField(
        child=serializers.EmailField(),
        max_length=1000  # Limit to 1000 emails per import
    )
    frequency = serializers.ChoiceField(
        choices=Subscriber.frequency.field.choices,
        default='weekly'
    )
    source = serializers.CharField(max_length=100, default='import')

    def validate_emails(self, value):
        """Validate that emails are unique and not already subscribed"""
        from .models import Subscriber
        
        existing_emails = set(Subscriber.objects.filter(
            email__in=value, 
            is_active=True
        ).values_list('email', flat=True))
        
        duplicate_emails = [email for email in value if email in existing_emails]
        if duplicate_emails:
            raise serializers.ValidationError(
                f"These emails are already subscribed: {', '.join(duplicate_emails)}"
            )
        
        return value 