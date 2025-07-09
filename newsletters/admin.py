from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Newsletter, Subscriber, NewsletterTemplate, NewsletterSend, NewsletterAnalytics

@admin.register(NewsletterTemplate)
class NewsletterTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'subject_template']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'is_active', 'frequency', 'source', 'subscribed_at', 'total_emails_received']
    list_filter = ['is_active', 'frequency', 'source', 'subscribed_at']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at', 'total_emails_received', 'total_emails_opened', 'total_emails_clicked']
    ordering = ['-subscribed_at']
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f'{updated} subscribers activated.')
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscribers deactivated.')
    deactivate_subscribers.short_description = "Deactivate selected subscribers"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'scheduled_at', 'sent_at', 'total_recipients', 'open_rate', 'click_rate']
    list_filter = ['status', 'author', 'created_at', 'sent_at']
    search_fields = ['title', 'subject', 'content']
    readonly_fields = ['author', 'sent_at', 'total_recipients', 'total_sent', 'total_delivered', 
                      'total_opened', 'total_clicked', 'open_rate', 'click_rate', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subject', 'content', 'html_content', 'summary', 'featured_image')
        }),
        ('Settings', {
            'fields': ('author', 'template', 'status', 'scheduled_at')
        }),
        ('Analytics', {
            'fields': ('total_recipients', 'total_sent', 'total_delivered', 'total_opened', 
                      'total_clicked', 'open_rate', 'click_rate'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'sent_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['send_newsletters', 'schedule_newsletters', 'cancel_newsletters']
    
    def send_newsletters(self, request, queryset):
        from django.utils import timezone
        updated = 0
        for newsletter in queryset.filter(status='draft'):
            newsletter.status = 'sent'
            newsletter.sent_at = timezone.now()
            newsletter.save()
            updated += 1
        self.message_user(request, f'{updated} newsletters marked as sent.')
    send_newsletters.short_description = "Mark selected newsletters as sent"
    
    def schedule_newsletters(self, request, queryset):
        updated = queryset.filter(status='draft').update(status='scheduled')
        self.message_user(request, f'{updated} newsletters scheduled.')
    schedule_newsletters.short_description = "Schedule selected newsletters"
    
    def cancel_newsletters(self, request, queryset):
        updated = queryset.filter(status__in=['draft', 'scheduled']).update(status='cancelled')
        self.message_user(request, f'{updated} newsletters cancelled.')
    cancel_newsletters.short_description = "Cancel selected newsletters"

@admin.register(NewsletterSend)
class NewsletterSendAdmin(admin.ModelAdmin):
    list_display = ['newsletter_title', 'subscriber_email', 'status', 'sent_at', 'opened_at', 'clicked_at']
    list_filter = ['status', 'sent_at', 'opened_at', 'clicked_at']
    search_fields = ['newsletter__title', 'subscriber__email']
    readonly_fields = ['newsletter', 'subscriber', 'sent_at', 'delivered_at', 'opened_at', 
                      'clicked_at', 'message_id', 'provider_response', 'open_count', 'click_count']
    ordering = ['-created_at']
    
    def newsletter_title(self, obj):
        return obj.newsletter.title
    newsletter_title.short_description = 'Newsletter'
    
    def subscriber_email(self, obj):
        return obj.subscriber.email
    subscriber_email.short_description = 'Subscriber'

@admin.register(NewsletterAnalytics)
class NewsletterAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['newsletter_title', 'total_sent', 'total_delivered', 'total_opened', 
                   'delivery_rate', 'open_rate', 'click_rate']
    list_filter = ['updated_at']
    readonly_fields = ['newsletter', 'total_sent', 'total_delivered', 'total_bounced', 
                      'total_opened', 'total_clicked', 'total_unsubscribed', 'delivery_rate', 
                      'open_rate', 'click_rate', 'unsubscribe_rate', 'first_open_at', 
                      'last_open_at', 'average_time_to_open', 'updated_at']
    ordering = ['-updated_at']
    
    def newsletter_title(self, obj):
        return obj.newsletter.title
    newsletter_title.short_description = 'Newsletter'
    
    def delivery_rate(self, obj):
        return f"{obj.delivery_rate:.1f}%"
    delivery_rate.short_description = 'Delivery Rate'
    
    def open_rate(self, obj):
        return f"{obj.open_rate:.1f}%"
    open_rate.short_description = 'Open Rate'
    
    def click_rate(self, obj):
        return f"{obj.click_rate:.1f}%"
    click_rate.short_description = 'Click Rate'
