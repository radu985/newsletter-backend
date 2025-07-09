from django.db import models
from users.models import CustomUser

# Create your models here.

class Playbook(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField(blank=True)  # Rich text content
    file = models.FileField(upload_to='playbooks/', null=True, blank=True)
    
    # Categories and tags
    category = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=500, blank=True)  # Comma-separated tags
    
    # Status and visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    
    # Author and ownership
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playbooks', null=True, blank=True)
    
    # Usage tracking
    download_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
