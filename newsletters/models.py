from django.db import models
from django.contrib.auth.models import User
from users.models import CustomUser

class NewsletterTemplate(models.Model):
    """Template for newsletter emails"""
    name = models.CharField(max_length=100)
    subject_template = models.CharField(max_length=200)
    html_template = models.TextField()
    text_template = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Subscriber(models.Model):
    """Email subscriber for newsletters"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100, blank=True)  # e.g., "website", "admin", "import"
    
    # Preferences
    frequency = models.CharField(
        max_length=20,
        choices=[
            ('weekly', 'Weekly'),
            ('biweekly', 'Bi-weekly'),
            ('monthly', 'Monthly'),
        ],
        default='weekly'
    )
    
    # Analytics
    total_emails_received = models.IntegerField(default=0)
    total_emails_opened = models.IntegerField(default=0)
    total_emails_clicked = models.IntegerField(default=0)
    last_email_sent = models.DateTimeField(null=True, blank=True)
    last_email_opened = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

class Newsletter(models.Model):
    """Newsletter content and metadata"""
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    
    # Status
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sending', 'Sending'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Author and template
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='newsletters')
    template = models.ForeignKey(NewsletterTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Scheduling
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Content
    featured_image = models.ImageField(upload_to='newsletters/', null=True, blank=True)
    summary = models.TextField(blank=True)
    
    # Analytics
    total_recipients = models.IntegerField(default=0)
    total_sent = models.IntegerField(default=0)
    total_delivered = models.IntegerField(default=0)
    total_opened = models.IntegerField(default=0)
    total_clicked = models.IntegerField(default=0)
    open_rate = models.FloatField(default=0.0)
    click_rate = models.FloatField(default=0.0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-generate summary if not provided
        if not self.summary and self.content:
            self.summary = self.content[:200] + "..." if len(self.content) > 200 else self.content
        super().save(*args, **kwargs)

class NewsletterSend(models.Model):
    """Track individual newsletter sends to subscribers"""
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name='sends')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='newsletter_sends')
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('bounced', 'Bounced'),
        ('unsubscribed', 'Unsubscribed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Tracking
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    # Email provider data
    message_id = models.CharField(max_length=255, blank=True)
    provider_response = models.TextField(blank=True)
    
    # Analytics
    open_count = models.IntegerField(default=0)
    click_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['newsletter', 'subscriber']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.newsletter.title} -> {self.subscriber.email}"

class NewsletterAnalytics(models.Model):
    """Aggregated analytics for newsletters"""
    newsletter = models.OneToOneField(Newsletter, on_delete=models.CASCADE, related_name='analytics')
    
    # Send metrics
    total_sent = models.IntegerField(default=0)
    total_delivered = models.IntegerField(default=0)
    total_bounced = models.IntegerField(default=0)
    
    # Engagement metrics
    total_opened = models.IntegerField(default=0)
    total_clicked = models.IntegerField(default=0)
    total_unsubscribed = models.IntegerField(default=0)
    
    # Rates
    delivery_rate = models.FloatField(default=0.0)
    open_rate = models.FloatField(default=0.0)
    click_rate = models.FloatField(default=0.0)
    unsubscribe_rate = models.FloatField(default=0.0)
    
    # Time-based metrics
    first_open_at = models.DateTimeField(null=True, blank=True)
    last_open_at = models.DateTimeField(null=True, blank=True)
    average_time_to_open = models.FloatField(null=True, blank=True)  # in hours
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.newsletter.title}"

    def update_metrics(self):
        """Update all metrics based on NewsletterSend records"""
        sends = self.newsletter.sends.all()
        
        self.total_sent = sends.count()
        self.total_delivered = sends.filter(status__in=['delivered', 'opened', 'clicked']).count()
        self.total_bounced = sends.filter(status='bounced').count()
        self.total_opened = sends.filter(status__in=['opened', 'clicked']).count()
        self.total_clicked = sends.filter(status='clicked').count()
        self.total_unsubscribed = sends.filter(status='unsubscribed').count()
        
        # Calculate rates
        if self.total_sent > 0:
            self.delivery_rate = (self.total_delivered / self.total_sent) * 100
            self.open_rate = (self.total_opened / self.total_sent) * 100
            self.click_rate = (self.total_clicked / self.total_sent) * 100
            self.unsubscribe_rate = (self.total_unsubscribed / self.total_sent) * 100
        
        self.save()
