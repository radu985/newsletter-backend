from django.db import models
from users.models import CustomUser

# Create your models here.

class Tool(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    
    # Categories and tags
    category = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=500, blank=True)  # Comma-separated tags
    
    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_free = models.BooleanField(default=True)
    
    # Pricing and access
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pricing_model = models.CharField(max_length=50, blank=True)  # free, freemium, paid, subscription
    
    # Author and ownership
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tools', null=True, blank=True)
    
    # Usage tracking
    click_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    
    # Additional info
    icon = models.CharField(max_length=100, blank=True)  # Icon class or emoji
    documentation_url = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
