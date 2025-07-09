import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
import uuid

def send_newsletter_email(newsletter, subscriber, newsletter_send):
    """
    Send a newsletter email to a subscriber
    """
    try:
        # Generate tracking URLs
        tracking_id = str(uuid.uuid4())
        open_tracking_url = f"{settings.SITE_URL}/newsletters/track/open/{tracking_id}/"
        click_tracking_url = f"{settings.SITE_URL}/newsletters/track/click/{tracking_id}/"
        unsubscribe_url = f"{settings.SITE_URL}/newsletters/unsubscribe/{subscriber.id}/"
        
        # Prepare email context
        context = {
            'newsletter': newsletter,
            'subscriber': subscriber,
            'open_tracking_url': open_tracking_url,
            'click_tracking_url': click_tracking_url,
            'unsubscribe_url': unsubscribe_url,
            'tracking_id': tracking_id,
        }
        
        # Render email content
        if newsletter.template:
            # Use newsletter template
            html_content = render_newsletter_with_template(newsletter, context)
            text_content = strip_tags(html_content)
        else:
            # Use default template
            html_content = render_to_string('newsletters/email_template.html', context)
            text_content = render_to_string('newsletters/email_template.txt', context)
        
        # Create email
        subject = newsletter.subject
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = subscriber.email
        
        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        
        # Add tracking headers
        email.extra_headers = {
            'X-Newsletter-ID': str(newsletter.id),
            'X-Subscriber-ID': str(subscriber.id),
            'X-Tracking-ID': tracking_id,
        }
        
        # Send email
        email.send()
        
        # Update newsletter send record
        newsletter_send.status = 'sent'
        newsletter_send.sent_at = timezone.now()
        newsletter_send.message_id = tracking_id
        newsletter_send.save()
        
        # Update subscriber stats
        subscriber.total_emails_received += 1
        subscriber.last_email_sent = timezone.now()
        subscriber.save()
        
        return True, None
        
    except Exception as e:
        # Update newsletter send record with error
        newsletter_send.status = 'bounced'
        newsletter_send.provider_response = str(e)
        newsletter_send.save()
        
        return False, str(e)

def render_newsletter_with_template(newsletter, context):
    """
    Render newsletter content using the selected template
    """
    if not newsletter.template:
        return newsletter.content
    
    # Replace template variables
    html_template = newsletter.template.html_template
    subject_template = newsletter.template.subject_template
    
    # Replace common variables
    replacements = {
        '{{ title }}': newsletter.title,
        '{{ content }}': newsletter.content,
        '{{ subject }}': newsletter.subject,
        '{{ unsubscribe_url }}': context['unsubscribe_url'],
        '{{ open_tracking_url }}': context['open_tracking_url'],
        '{{ subscriber.email }}': context['subscriber'].email,
        '{{ subscriber.first_name }}': context['subscriber'].first_name or '',
        '{{ subscriber.last_name }}': context['subscriber'].last_name or '',
        '{{ subscriber.full_name }}': context['subscriber'].full_name,
    }
    
    # Apply replacements
    html_content = html_template
    for key, value in replacements.items():
        html_content = html_content.replace(key, str(value))
    
    return html_content

def send_test_email(email_address, newsletter_id=None):
    """
    Send a test email to verify email configuration
    """
    try:
        subject = "Test Email - Newsletter Platform"
        html_content = """
        <html>
        <body>
            <h1>Test Email</h1>
            <p>This is a test email to verify your email configuration is working correctly.</p>
            <p>If you received this email, your SMTP settings are configured properly!</p>
        </body>
        </html>
        """
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_address]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        return True, "Test email sent successfully!"
        
    except Exception as e:
        return False, f"Failed to send test email: {str(e)}"

def send_bulk_newsletters(newsletter):
    """
    Send newsletter to all active subscribers
    """
    from .models import Subscriber, NewsletterSend
    
    active_subscribers = Subscriber.objects.filter(is_active=True)
    total_sent = 0
    total_failed = 0
    errors = []
    
    for subscriber in active_subscribers:
        # Create or get newsletter send record
        newsletter_send, created = NewsletterSend.objects.get_or_create(
            newsletter=newsletter,
            subscriber=subscriber,
            defaults={'status': 'pending'}
        )
        
        if newsletter_send.status == 'pending':
            success, error = send_newsletter_email(newsletter, subscriber, newsletter_send)
            
            if success:
                total_sent += 1
            else:
                total_failed += 1
                errors.append(f"{subscriber.email}: {error}")
    
    # Update newsletter stats
    newsletter.total_sent = total_sent
    newsletter.total_recipients = active_subscribers.count()
    newsletter.save()
    
    return {
        'total_sent': total_sent,
        'total_failed': total_failed,
        'errors': errors
    } 