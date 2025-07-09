#!/usr/bin/env python
"""
Script to create sample newsletter data for testing
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from newsletters.models import Newsletter, NewsletterTemplate
from users.models import CustomUser

def create_sample_newsletters():
    """Create sample newsletters for testing"""
    
    # Get or create a default user
    user, created = CustomUser.objects.get_or_create(
        email='admin@example.com',
        defaults={
            'name': 'Admin User',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    # Get newsletter templates
    templates = list(NewsletterTemplate.objects.all())
    if not templates:
        print("No newsletter templates found. Creating a default template...")
        template = NewsletterTemplate.objects.create(
            name='Default Template',
            subject_template='{title}',
            html_template='<h1>{title}</h1><p>{content}</p>',
            text_template='{title}\n\n{content}'
        )
        templates = [template]
    
    # Sample newsletter data
    sample_newsletters = [
        {
            'title': 'Weekly Tech Roundup',
            'subject': 'This Week in Technology: AI Breakthroughs and Startup News',
            'content': 'This week brought exciting developments in artificial intelligence, with major breakthroughs in natural language processing and computer vision. Startups across the tech ecosystem are leveraging these advances to create innovative solutions...',
            'status': 'sent',
            'open_rate': 24.5,
            'click_rate': 8.2,
            'total_recipients': 1250,
            'total_sent': 1250,
            'total_delivered': 1200,
            'total_opened': 294,
            'total_clicked': 103,
            'sent_at': datetime.now() - timedelta(days=2)
        },
        {
            'title': 'Marketing Insights Monthly',
            'subject': 'Digital Marketing Trends: What\'s Working in 2024',
            'content': 'Digital marketing continues to evolve rapidly, with new platforms and strategies emerging every month. Our analysis shows that video content, personalized email campaigns, and social commerce are driving the highest engagement rates...',
            'status': 'sent',
            'open_rate': 31.2,
            'click_rate': 12.8,
            'total_recipients': 890,
            'total_sent': 890,
            'total_delivered': 865,
            'total_opened': 277,
            'total_clicked': 114,
            'sent_at': datetime.now() - timedelta(days=7)
        },
        {
            'title': 'Product Development Newsletter',
            'subject': 'Building Better Products: User Research and Iteration',
            'content': 'Successful product development relies heavily on understanding user needs and iterating based on feedback. This month, we explore best practices for conducting user research, analyzing feedback, and implementing changes that drive user satisfaction...',
            'status': 'draft',
            'open_rate': 0,
            'click_rate': 0,
            'total_recipients': 0,
            'total_sent': 0,
            'total_delivered': 0,
            'total_opened': 0,
            'total_clicked': 0
        },
        {
            'title': 'Startup Funding Report',
            'subject': 'Q1 2024 Funding Landscape: Who\'s Raising and Why',
            'content': 'The first quarter of 2024 has seen significant activity in the startup funding space. AI and fintech companies continue to dominate, but we\'re also seeing increased interest in climate tech and healthtech startups...',
            'status': 'scheduled',
            'open_rate': 0,
            'click_rate': 0,
            'total_recipients': 0,
            'total_sent': 0,
            'total_delivered': 0,
            'total_opened': 0,
            'total_clicked': 0,
            'scheduled_at': datetime.now() + timedelta(days=3)
        },
        {
            'title': 'Developer Tools Update',
            'subject': 'New Tools and Libraries: What Developers Need to Know',
            'content': 'The developer ecosystem is constantly evolving with new tools, libraries, and frameworks being released regularly. This month, we highlight the most promising new technologies that can improve your development workflow...',
            'status': 'sent',
            'open_rate': 28.7,
            'click_rate': 15.3,
            'total_recipients': 2100,
            'total_sent': 2100,
            'total_delivered': 2050,
            'total_opened': 603,
            'total_clicked': 321,
            'sent_at': datetime.now() - timedelta(days=14)
        },
        {
            'title': 'Business Strategy Insights',
            'subject': 'Strategic Planning for Growth: Lessons from Successful Companies',
            'content': 'Building a successful business requires more than just a good product. Strategic planning, market positioning, and execution excellence are crucial components. We examine how successful companies approach these challenges...',
            'status': 'draft',
            'open_rate': 0,
            'click_rate': 0,
            'total_recipients': 0,
            'total_sent': 0,
            'total_delivered': 0,
            'total_opened': 0,
            'total_clicked': 0
        }
    ]
    
    created_count = 0
    for newsletter_data in sample_newsletters:
        # Check if newsletter already exists
        if not Newsletter.objects.filter(title=newsletter_data['title']).exists():
            newsletter = Newsletter.objects.create(
            title=newsletter_data['title'],
                subject=newsletter_data['subject'],
                content=newsletter_data['content'],
                status=newsletter_data['status'],
                author=user,
                template=random.choice(templates),
                open_rate=newsletter_data['open_rate'],
                click_rate=newsletter_data['click_rate'],
                total_recipients=newsletter_data['total_recipients'],
                total_sent=newsletter_data['total_sent'],
                total_delivered=newsletter_data['total_delivered'],
                total_opened=newsletter_data['total_opened'],
                total_clicked=newsletter_data['total_clicked'],
                sent_at=newsletter_data.get('sent_at'),
                scheduled_at=newsletter_data.get('scheduled_at')
            )
            created_count += 1
            print(f"Created newsletter: {newsletter.title}")
    
    print(f"\nCreated {created_count} new newsletters")
    print(f"Total newsletters in database: {Newsletter.objects.count()}")

if __name__ == '__main__':
    create_sample_newsletters() 