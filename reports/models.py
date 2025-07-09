from django.db import models
from users.models import CustomUser

# Create your models here.

class RevenueReport(models.Model):
    website_name = models.CharField(max_length=255)
    revenue_monthly = models.DecimalField(max_digits=12, decimal_places=2)
    revenue_yearly = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    
    # Additional metrics
    traffic_monthly = models.IntegerField(default=0)
    conversion_rate = models.FloatField(default=0.0)
    profit_margin = models.FloatField(default=0.0)
    
    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Author and ownership
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='revenue_reports', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.website_name

class NewsletterReport(models.Model):
    """Report for newsletter performance analytics"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Metrics
    total_subscribers = models.IntegerField(default=0)
    open_rate = models.FloatField(default=0.0)
    click_rate = models.FloatField(default=0.0)
    conversion_rate = models.FloatField(default=0.0)
    
    # Date range
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Author and ownership
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='newsletter_reports', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class AnalyticsReport(models.Model):
    """General analytics report"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    report_type = models.CharField(max_length=100)  # traffic, conversion, engagement, etc.
    
    # Data (stored as JSON)
    data = models.JSONField(default=dict)
    
    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Author and ownership
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='analytics_reports', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
