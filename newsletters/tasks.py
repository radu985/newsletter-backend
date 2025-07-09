from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Newsletter, NewsletterSend, Subscriber
import logging

logger = logging.getLogger(__name__)

@shared_task
def test_celery_task():
    """
    Simple test task to verify Celery is working
    """
    logger.info("Celery test task executed successfully!")
    return {
        'status': 'success',
        'message': 'Celery is working correctly',
        'timestamp': timezone.now().isoformat()
    }

@shared_task
def send_newsletter_task(newsletter_id):
    """
    Celery task to send a newsletter to all subscribers
    """
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        
        # Import the service function
        from .services import send_bulk_newsletters
        
        # Send newsletters using the existing service
        result = send_bulk_newsletters(newsletter)
        
        # Update newsletter status
        newsletter.status = 'sent'
        newsletter.sent_at = timezone.now()
        newsletter.save()
        
        logger.info(f"Newsletter {newsletter_id} sent successfully. Sent: {result['total_sent']}, Failed: {result['total_failed']}")
        return {
            'newsletter_id': newsletter_id,
            'sent_count': result['total_sent'],
            'failed_count': result['total_failed'],
            'status': 'completed'
        }
        
    except Newsletter.DoesNotExist:
        logger.error(f"Newsletter {newsletter_id} not found")
        return {'status': 'error', 'message': 'Newsletter not found'}
    except Exception as e:
        logger.error(f"Error sending newsletter {newsletter_id}: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def send_scheduled_newsletters():
    """
    Celery beat task to check and send scheduled newsletters
    """
    try:
        now = timezone.now()
        scheduled_newsletters = Newsletter.objects.filter(
            status='scheduled',
            scheduled_at__lte=now
        )
        
        for newsletter in scheduled_newsletters:
            # Send the newsletter asynchronously
            send_newsletter_task.delay(newsletter.id)
            
        logger.info(f"Found {scheduled_newsletters.count()} newsletters to send")
        return {'status': 'success', 'count': scheduled_newsletters.count()}
        
    except Exception as e:
        logger.error(f"Error in send_scheduled_newsletters: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def cleanup_old_newsletter_sends():
    """
    Clean up old newsletter send records (older than 90 days)
    """
    try:
        cutoff_date = timezone.now() - timezone.timedelta(days=90)
        deleted_count = NewsletterSend.objects.filter(
            sent_at__lt=cutoff_date
        ).delete()[0]
        
        logger.info(f"Cleaned up {deleted_count} old newsletter send records")
        return {'status': 'success', 'deleted_count': deleted_count}
        
    except Exception as e:
        logger.error(f"Error in cleanup_old_newsletter_sends: {str(e)}")
        return {'status': 'error', 'message': str(e)}

@shared_task
def send_test_email_task(email_address, newsletter_id):
    """
    Send a test email for a newsletter
    """
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        
        # Import the service function
        from .services import send_test_email
        
        # Send test email
        success, message = send_test_email(email_address, newsletter_id)
        
        if success:
            logger.info(f"Test email sent successfully to {email_address}")
            return {'status': 'success', 'message': 'Test email sent successfully'}
        else:
            logger.error(f"Failed to send test email to {email_address}")
            return {'status': 'error', 'message': 'Failed to send test email'}
            
    except Newsletter.DoesNotExist:
        logger.error(f"Newsletter {newsletter_id} not found for test email")
        return {'status': 'error', 'message': 'Newsletter not found'}
    except Exception as e:
        logger.error(f"Error sending test email: {str(e)}")
        return {'status': 'error', 'message': str(e)} 