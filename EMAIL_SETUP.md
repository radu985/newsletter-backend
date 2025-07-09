# Email Configuration Setup Guide

This guide will help you configure SMTP email sending for your newsletter platform.

## Gmail Configuration

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification if not already enabled

### Step 2: Generate App Password
1. Go to Google Account settings
2. Navigate to Security > 2-Step Verification
3. Click on "App passwords" at the bottom
4. Select "Mail" and "Other (Custom name)"
5. Enter "Newsletter Platform" as the name
6. Copy the generated 16-character password

### Step 3: Update Django Settings
Edit `backend/config/settings.py` and update the email configuration:

```python
# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@gmail.com"  # Your Gmail address
EMAIL_HOST_PASSWORD = "your-16-char-app-password"  # App password from Step 2
DEFAULT_FROM_EMAIL = "your-email@gmail.com"
```

## Outlook Configuration

### Step 1: Enable App Access
1. Go to Outlook.com settings
2. Navigate to Security & Privacy
3. Enable "Less secure app access" (if available)
4. Or use OAuth2 authentication (more secure)

### Step 2: Update Django Settings
Edit `backend/config/settings.py` and update the email configuration:

```python
# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-mail.outlook.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-email@outlook.com"
EMAIL_HOST_PASSWORD = "your-password"
DEFAULT_FROM_EMAIL = "your-email@outlook.com"
```

## Testing Your Configuration

1. Start your Django server: `python manage.py runserver`
2. Visit `http://localhost:3000/email-test` in your browser
3. Enter your email address and click "Send Test Email"
4. Check your inbox for the test email

## Troubleshooting

### Common Gmail Issues:
- **Authentication failed**: Make sure you're using an App Password, not your regular password
- **2FA not enabled**: You must enable 2-Factor Authentication to use App Passwords
- **Less secure app access**: Gmail no longer supports this option

### Common Outlook Issues:
- **Authentication failed**: Try enabling "Less secure app access"
- **Connection timeout**: Check your firewall settings
- **Port blocked**: Some networks block port 587, try port 465 with SSL

### General Issues:
- **Connection refused**: Check if your email provider allows SMTP access
- **Rate limiting**: Email providers may limit the number of emails you can send
- **Spam filters**: Your emails might be marked as spam initially

## Production Considerations

For production use, consider:

1. **Email Service Providers**: Use services like SendGrid, Mailgun, or Amazon SES
2. **Environment Variables**: Store email credentials in environment variables
3. **Rate Limiting**: Implement proper rate limiting for email sending
4. **Monitoring**: Set up monitoring for email delivery and bounce rates
5. **DKIM/SPF**: Configure proper email authentication to improve deliverability

## Environment Variables Setup

For better security, use environment variables:

```python
import os

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your-email@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your-app-password')
```

Create a `.env` file in your backend directory:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Next Steps

Once email is configured:
1. Test sending newsletters to subscribers
2. Set up email tracking and analytics
3. Implement newsletter scheduling
4. Add unsubscribe functionality
5. Monitor email delivery rates 