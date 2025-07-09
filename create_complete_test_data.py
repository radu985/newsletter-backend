#!/usr/bin/env python
import os
import django
import random
from datetime import datetime, timedelta, date
from django.utils import timezone
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import CustomUser
from articles.models import Topic, Article
from newsletters.models import (
    NewsletterTemplate, Subscriber, Newsletter, 
    NewsletterSend, NewsletterAnalytics
)
from playbooks.models import Playbook
from tools.models import Tool
from reports.models import RevenueReport, NewsletterReport, AnalyticsReport

def create_complete_test_data():
    print("🚀 Creating complete test data for the newsletter project...")
    
    # Create users (if not exists)
    print("\n👥 Creating users...")
    users_data = [
        {'email': 'admin@newsletter.com', 'name': 'Admin User', 'is_staff': True, 'is_superuser': True, 'is_premium': True},
        {'email': 'editor@newsletter.com', 'name': 'Sarah Editor', 'is_staff': True, 'is_premium': True},
        {'email': 'writer@newsletter.com', 'name': 'John Writer', 'is_premium': True},
        {'email': 'contributor@newsletter.com', 'name': 'Maria Contributor', 'is_premium': False},
        {'email': 'test@newsletter.com', 'name': 'Test User', 'is_premium': False},
        {'email': 'demo@newsletter.com', 'name': 'Demo User', 'is_premium': True},
        {'email': 'analyst@newsletter.com', 'name': 'Alex Analyst', 'is_premium': True},
        {'email': 'manager@newsletter.com', 'name': 'Mike Manager', 'is_premium': True},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = CustomUser.objects.get_or_create(
            email=user_data['email'],
            defaults=user_data
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print(f"  ✅ Created user: {user.email} ({user.name})")
        else:
            print(f"  ℹ️  User already exists: {user.email}")
        created_users.append(user)
    
    # Create topics (if not exists)
    print("\n📚 Creating topics...")
    topics_data = [
        'Technology', 'Business', 'Marketing', 'Productivity', 'Health & Wellness',
        'Finance', 'Education', 'Travel', 'Food & Cooking', 'Science',
        'Entertainment', 'Sports', 'Politics', 'Environment', 'Personal Development'
    ]
    
    created_topics = []
    for topic_name in topics_data:
        topic, created = Topic.objects.get_or_create(
            name=topic_name,
            defaults={'slug': topic_name.lower().replace(' & ', '-').replace(' ', '-')}
        )
        if created:
            print(f"  ✅ Created topic: {topic.name}")
        else:
            print(f"  ℹ️  Topic already exists: {topic.name}")
        created_topics.append(topic)
    
    # Create articles (if not exists)
    print("\n📝 Creating articles...")
    articles_data = [
        {
            'title': 'The Future of AI in Business: 2024 Trends',
            'content': '''
            <h2>Artificial Intelligence is reshaping the business landscape</h2>
            <p>As we move through 2024, artificial intelligence continues to transform how businesses operate, compete, and serve their customers. Here are the key trends that are defining the AI landscape this year.</p>
            
            <h3>1. Generative AI Goes Mainstream</h3>
            <p>Generative AI tools like ChatGPT, DALL-E, and Midjourney have moved from experimental to essential business tools. Companies are now integrating these technologies into their workflows for content creation, design, and customer service.</p>
            
            <h3>2. AI-Powered Personalization</h3>
            <p>Businesses are leveraging AI to deliver hyper-personalized experiences to their customers. From product recommendations to marketing campaigns, AI is making personalization more sophisticated and effective than ever before.</p>
            
            <h3>3. Ethical AI and Governance</h3>
            <p>With the rapid adoption of AI comes increased focus on ethical considerations and governance. Companies are establishing AI ethics committees and implementing responsible AI practices to ensure their AI systems are fair, transparent, and accountable.</p>
            
            <h3>4. AI in Cybersecurity</h3>
            <p>AI is playing a crucial role in detecting and preventing cyber threats. Machine learning algorithms can identify patterns and anomalies that human analysts might miss, providing faster and more accurate threat detection.</p>
            
            <p>The future of AI in business is not just about automation—it's about augmentation, enabling humans to work smarter and more efficiently while creating new opportunities for innovation and growth.</p>
            ''',
            'topic': 'Technology',
            'is_published': True
        },
        {
            'title': '10 Productivity Hacks That Actually Work',
            'content': '''
            <h2>Boost your productivity with these proven strategies</h2>
            <p>In today's fast-paced world, productivity is more important than ever. Here are 10 scientifically-backed productivity hacks that can help you get more done in less time.</p>
            
            <h3>1. The Two-Minute Rule</h3>
            <p>If a task takes less than two minutes, do it immediately. This prevents small tasks from accumulating and becoming overwhelming.</p>
            
            <h3>2. Time Blocking</h3>
            <p>Schedule specific time slots for different types of work. This helps you focus and prevents context switching, which can reduce productivity by up to 40%.</p>
            
            <h3>3. The Pomodoro Technique</h3>
            <p>Work for 25 minutes, then take a 5-minute break. This technique helps maintain focus and prevents burnout.</p>
            
            <h3>4. Batch Similar Tasks</h3>
            <p>Group similar tasks together to reduce the mental overhead of switching between different types of work.</p>
            
            <h3>5. Eliminate Distractions</h3>
            <p>Turn off notifications, close unnecessary tabs, and create a dedicated workspace to minimize interruptions.</p>
            
            <h3>6. Use the 80/20 Rule</h3>
            <p>Focus on the 20% of tasks that produce 80% of your results. Identify your highest-impact activities and prioritize them.</p>
            
            <h3>7. Take Regular Breaks</h3>
            <p>Your brain needs rest to function optimally. Take short breaks throughout the day to maintain peak performance.</p>
            
            <h3>8. Set Clear Goals</h3>
            <p>Define specific, measurable, achievable, relevant, and time-bound (SMART) goals to guide your work.</p>
            
            <h3>9. Use Technology Wisely</h3>
            <p>Leverage productivity apps and tools, but don't let them become distractions themselves.</p>
            
            <h3>10. Review and Reflect</h3>
            <p>Regularly review your productivity systems and make adjustments based on what's working and what isn't.</p>
            
            <p>Remember, productivity is personal. Experiment with these techniques to find what works best for you and your unique circumstances.</p>
            ''',
            'topic': 'Productivity',
            'is_published': True
        }
    ]
    
    created_articles = []
    for article_data in articles_data:
        topic = Topic.objects.get(name=article_data['topic'])
        author = random.choice(created_users)
        
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults={
                'content': article_data['content'],
                'author': author,
                'topic': topic,
                'is_published': article_data['is_published']
            }
        )
        if created:
            print(f"  ✅ Created article: {article.title}")
        else:
            print(f"  ℹ️  Article already exists: {article.title}")
        created_articles.append(article)
    
    # Create newsletter templates (if not exists)
    print("\n📧 Creating newsletter templates...")
    templates_data = [
        {
            'name': 'Weekly Newsletter',
            'subject_template': '{{ title }} - Your Weekly Update',
            'html_template': '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{{ title }}</title>
            </head>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center;">
                    <h1 style="margin: 0;">{{ title }}</h1>
                </div>
                <div style="padding: 20px 0;">
                    {{ content|safe }}
                </div>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px;">
                    <h3 style="margin-top: 0;">Quick Links</h3>
                    <ul>
                        <li><a href="{{ site_url }}">Visit Our Website</a></li>
                        <li><a href="{{ site_url }}/articles">Read More Articles</a></li>
                        <li><a href="{{ site_url }}/newsletters">Newsletter Archive</a></li>
                    </ul>
                </div>
                <hr style="margin: 30px 0;">
                <p style="color: #666; font-size: 12px;">
                    You received this email because you're subscribed to our newsletter.<br>
                    <a href="{{ unsubscribe_url }}">Unsubscribe</a> | 
                    <a href="{{ site_url }}">View in browser</a>
                </p>
            </body>
            </html>
            ''',
            'text_template': '''
            {{ title }}
            
            {{ content }}
            
            Quick Links:
            - Visit Our Website: {{ site_url }}
            - Read More Articles: {{ site_url }}/articles
            - Newsletter Archive: {{ site_url }}/newsletters
            
            ---
            You received this email because you're subscribed to our newsletter.
            To unsubscribe, visit: {{ unsubscribe_url }}
            '''
        }
    ]
    
    created_templates = []
    for template_data in templates_data:
        template, created = NewsletterTemplate.objects.get_or_create(
            name=template_data['name'],
            defaults=template_data
        )
        if created:
            print(f"  ✅ Created template: {template.name}")
        else:
            print(f"  ℹ️  Template already exists: {template.name}")
        created_templates.append(template)
    
    # Create subscribers (if not exists)
    print("\n👥 Creating subscribers...")
    subscribers_data = [
        {'email': 'john.doe@example.com', 'first_name': 'John', 'last_name': 'Doe', 'frequency': 'weekly', 'source': 'website'},
        {'email': 'jane.smith@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'frequency': 'biweekly', 'source': 'admin'},
        {'email': 'mike.johnson@example.com', 'first_name': 'Mike', 'last_name': 'Johnson', 'frequency': 'monthly', 'source': 'import'},
        {'email': 'sarah.wilson@example.com', 'first_name': 'Sarah', 'last_name': 'Wilson', 'frequency': 'weekly', 'source': 'website'},
        {'email': 'david.brown@example.com', 'first_name': 'David', 'last_name': 'Brown', 'frequency': 'weekly', 'source': 'admin'},
    ]
    
    created_subscribers = []
    for sub_data in subscribers_data:
        subscriber, created = Subscriber.objects.get_or_create(
            email=sub_data['email'],
            defaults=sub_data
        )
        if created:
            print(f"  ✅ Created subscriber: {subscriber.email}")
        else:
            print(f"  ℹ️  Subscriber already exists: {subscriber.email}")
        created_subscribers.append(subscriber)
    
    # Create newsletters (if not exists)
    print("\n📰 Creating newsletters...")
    newsletters_data = [
        {
            'title': 'Welcome to Our Newsletter!',
            'subject': 'Welcome to Our Newsletter - Get Started Today',
            'content': '''
            <h2>Welcome to our community!</h2>
            <p>We're excited to have you on board. In this newsletter, you'll find:</p>
            <ul>
                <li>Latest industry insights</li>
                <li>Exclusive tips and tricks</li>
                <li>Product updates and announcements</li>
                <li>Community highlights</li>
            </ul>
            <p>Stay tuned for more valuable content coming your way!</p>
            ''',
            'status': 'sent',
            'template': 'Weekly Newsletter'
        }
    ]
    
    created_newsletters = []
    for newsletter_data in newsletters_data:
        template = NewsletterTemplate.objects.get(name=newsletter_data['template'])
        author = random.choice(created_users)
        
        # Set different dates for newsletters
        sent_at = None
        scheduled_at = None
        if newsletter_data['status'] == 'sent':
            sent_at = timezone.now() - timedelta(days=random.randint(1, 30))
        elif newsletter_data['status'] == 'scheduled':
            scheduled_at = timezone.now() + timedelta(days=random.randint(1, 7))
        
        newsletter, created = Newsletter.objects.get_or_create(
            title=newsletter_data['title'],
            defaults={
                'subject': newsletter_data['subject'],
                'content': newsletter_data['content'],
                'status': newsletter_data['status'],
                'author': author,
                'template': template,
                'sent_at': sent_at,
                'scheduled_at': scheduled_at,
                'total_recipients': len(created_subscribers),
                'total_sent': len(created_subscribers) if newsletter_data['status'] == 'sent' else 0,
                'total_delivered': len(created_subscribers) if newsletter_data['status'] == 'sent' else 0,
                'total_opened': random.randint(5, len(created_subscribers)) if newsletter_data['status'] == 'sent' else 0,
                'total_clicked': random.randint(2, 10) if newsletter_data['status'] == 'sent' else 0,
            }
        )
        if created:
            print(f"  ✅ Created newsletter: {newsletter.title}")
        else:
            print(f"  ℹ️  Newsletter already exists: {newsletter.title}")
        created_newsletters.append(newsletter)
    
    # Create playbooks
    print("\n📚 Creating playbooks...")
    playbooks_data = [
        {
            'title': 'Email Marketing Mastery Playbook',
            'description': 'A comprehensive guide to mastering email marketing strategies, from building lists to crafting compelling content.',
            'content': '''
            # Email Marketing Mastery Playbook
            
            ## Chapter 1: Building Your Email List
            - Lead magnet strategies
            - Opt-in form optimization
            - List segmentation techniques
            
            ## Chapter 2: Crafting Compelling Content
            - Subject line best practices
            - Email copywriting tips
            - Visual design principles
            
            ## Chapter 3: Automation and Sequences
            - Welcome series setup
            - Drip campaign creation
            - Behavioral triggers
            
            ## Chapter 4: Analytics and Optimization
            - Key metrics to track
            - A/B testing strategies
            - Performance optimization
            ''',
            'category': 'Marketing',
            'tags': 'email marketing, automation, copywriting, analytics',
            'is_featured': True,
            'download_count': random.randint(50, 500),
            'view_count': random.randint(200, 2000)
        },
        {
            'title': 'Productivity System Setup',
            'description': 'Step-by-step guide to setting up a personal productivity system that actually works.',
            'content': '''
            # Productivity System Setup
            
            ## Phase 1: Assessment
            - Current workflow analysis
            - Time tracking implementation
            - Goal setting framework
            
            ## Phase 2: System Design
            - Task management setup
            - Calendar optimization
            - Communication protocols
            
            ## Phase 3: Implementation
            - Tool selection and setup
            - Habit formation strategies
            - Team collaboration setup
            
            ## Phase 4: Optimization
            - Performance review
            - System refinement
            - Continuous improvement
            ''',
            'category': 'Productivity',
            'tags': 'productivity, time management, workflow, habits',
            'is_featured': False,
            'download_count': random.randint(30, 300),
            'view_count': random.randint(150, 1500)
        },
        {
            'title': 'Content Strategy Framework',
            'description': 'A strategic framework for creating and distributing content that drives business results.',
            'content': '''
            # Content Strategy Framework
            
            ## Strategic Foundation
            - Audience research and personas
            - Content audit and gap analysis
            - Brand voice and messaging
            
            ## Content Planning
            - Editorial calendar creation
            - Content themes and topics
            - Distribution strategy
            
            ## Content Creation
            - Writing guidelines and templates
            - Visual content creation
            - SEO optimization
            
            ## Measurement and Optimization
            - Performance metrics
            - Content ROI analysis
            - Strategy refinement
            ''',
            'category': 'Content Marketing',
            'tags': 'content strategy, SEO, branding, analytics',
            'is_featured': True,
            'download_count': random.randint(40, 400),
            'view_count': random.randint(180, 1800)
        },
        {
            'title': 'Social Media Growth Playbook',
            'description': 'Proven strategies for growing your social media presence and building engaged communities.',
            'content': '''
            # Social Media Growth Playbook
            
            ## Platform Strategy
            - Platform selection criteria
            - Audience analysis per platform
            - Content adaptation strategies
            
            ## Content Creation
            - Visual content guidelines
            - Caption writing techniques
            - Hashtag strategies
            
            ## Community Building
            - Engagement tactics
            - Influencer collaboration
            - User-generated content
            
            ## Analytics and Growth
            - Key performance indicators
            - Growth hacking techniques
            - Monetization strategies
            ''',
            'category': 'Social Media',
            'tags': 'social media, growth, community, engagement',
            'is_featured': False,
            'download_count': random.randint(35, 350),
            'view_count': random.randint(160, 1600)
        },
        {
            'title': 'Business Development Playbook',
            'description': 'Strategic framework for business development, partnerships, and revenue growth.',
            'content': '''
            # Business Development Playbook
            
            ## Market Analysis
            - Industry research methods
            - Competitive analysis
            - Opportunity identification
            
            ## Partnership Strategy
            - Partnership types and models
            - Negotiation frameworks
            - Relationship management
            
            ## Revenue Growth
            - Sales strategy development
            - Pricing optimization
            - Customer retention
            
            ## Scaling Operations
            - Team building and management
            - Process optimization
            - International expansion
            ''',
            'category': 'Business',
            'tags': 'business development, partnerships, sales, scaling',
            'is_featured': True,
            'download_count': random.randint(45, 450),
            'view_count': random.randint(220, 2200)
        }
    ]
    
    created_playbooks = []
    for playbook_data in playbooks_data:
        author = random.choice(created_users)
        
        playbook, created = Playbook.objects.get_or_create(
            title=playbook_data['title'],
            defaults={
                'description': playbook_data['description'],
                'content': playbook_data['content'],
                'category': playbook_data['category'],
                'tags': playbook_data['tags'],
                'is_featured': playbook_data['is_featured'],
                'download_count': playbook_data['download_count'],
                'view_count': playbook_data['view_count'],
                'author': author
            }
        )
        if created:
            print(f"  ✅ Created playbook: {playbook.title}")
        else:
            print(f"  ℹ️  Playbook already exists: {playbook.title}")
        created_playbooks.append(playbook)
    
    # Create tools
    print("\n🛠️ Creating tools...")
    tools_data = [
        {
            'name': 'Canva',
            'description': 'Graphic design platform for creating professional visuals, presentations, and marketing materials.',
            'url': 'https://canva.com',
            'category': 'Design',
            'tags': 'design, graphics, marketing, presentations',
            'is_featured': True,
            'is_free': True,
            'pricing_model': 'freemium',
            'rating': 4.8,
            'review_count': random.randint(1000, 10000),
            'click_count': random.randint(500, 5000),
            'icon': '🎨',
            'documentation_url': 'https://canva.com/help'
        },
        {
            'name': 'Mailchimp',
            'description': 'Email marketing platform for creating, sending, and analyzing email campaigns.',
            'url': 'https://mailchimp.com',
            'category': 'Email Marketing',
            'tags': 'email marketing, automation, analytics, campaigns',
            'is_featured': True,
            'is_free': True,
            'pricing_model': 'freemium',
            'rating': 4.5,
            'review_count': random.randint(800, 8000),
            'click_count': random.randint(400, 4000),
            'icon': '📧',
            'documentation_url': 'https://mailchimp.com/help'
        },
        {
            'name': 'Notion',
            'description': 'All-in-one workspace for notes, docs, project management, and team collaboration.',
            'url': 'https://notion.so',
            'category': 'Productivity',
            'tags': 'productivity, notes, project management, collaboration',
            'is_featured': True,
            'is_free': True,
            'pricing_model': 'freemium',
            'rating': 4.7,
            'review_count': random.randint(1200, 12000),
            'click_count': random.randint(600, 6000),
            'icon': '📝',
            'documentation_url': 'https://notion.so/help'
        },
        {
            'name': 'Hootsuite',
            'description': 'Social media management platform for scheduling posts, monitoring mentions, and analyzing performance.',
            'url': 'https://hootsuite.com',
            'category': 'Social Media',
            'tags': 'social media, scheduling, monitoring, analytics',
            'is_featured': False,
            'is_free': False,
            'price': Decimal('29.00'),
            'pricing_model': 'subscription',
            'rating': 4.3,
            'review_count': random.randint(600, 6000),
            'click_count': random.randint(300, 3000),
            'icon': '📱',
            'documentation_url': 'https://hootsuite.com/help'
        },
        {
            'name': 'Google Analytics',
            'description': 'Web analytics service that tracks and reports website traffic and user behavior.',
            'url': 'https://analytics.google.com',
            'category': 'Analytics',
            'tags': 'analytics, tracking, SEO, performance',
            'is_featured': True,
            'is_free': True,
            'pricing_model': 'free',
            'rating': 4.6,
            'review_count': random.randint(1500, 15000),
            'click_count': random.randint(800, 8000),
            'icon': '📊',
            'documentation_url': 'https://support.google.com/analytics'
        },
        {
            'name': 'Trello',
            'description': 'Visual project management tool for organizing tasks and collaborating with teams.',
            'url': 'https://trello.com',
            'category': 'Project Management',
            'tags': 'project management, kanban, collaboration, tasks',
            'is_featured': False,
            'is_free': True,
            'pricing_model': 'freemium',
            'rating': 4.4,
            'review_count': random.randint(900, 9000),
            'click_count': random.randint(450, 4500),
            'icon': '📋',
            'documentation_url': 'https://trello.com/help'
        },
        {
            'name': 'Buffer',
            'description': 'Social media management platform for scheduling and analyzing social media posts.',
            'url': 'https://buffer.com',
            'category': 'Social Media',
            'tags': 'social media, scheduling, analytics, management',
            'is_featured': False,
            'is_free': True,
            'pricing_model': 'freemium',
            'rating': 4.2,
            'review_count': random.randint(500, 5000),
            'click_count': random.randint(250, 2500),
            'icon': '📤',
            'documentation_url': 'https://buffer.com/help'
        },
        {
            'name': 'Grammarly',
            'description': 'AI-powered writing assistant that helps improve grammar, style, and tone.',
            'url': 'https://grammarly.com',
            'category': 'Writing',
            'tags': 'writing, grammar, editing, AI',
            'is_featured': True,
            'is_free': True,
            'pricing_model': 'freemium',
            'rating': 4.5,
            'review_count': random.randint(1100, 11000),
            'click_count': random.randint(550, 5500),
            'icon': '✍️',
            'documentation_url': 'https://grammarly.com/help'
        }
    ]
    
    created_tools = []
    for tool_data in tools_data:
        author = random.choice(created_users)
        
        tool, created = Tool.objects.get_or_create(
            name=tool_data['name'],
            defaults={
                'description': tool_data['description'],
                'url': tool_data['url'],
                'category': tool_data['category'],
                'tags': tool_data['tags'],
                'is_featured': tool_data['is_featured'],
                'is_free': tool_data['is_free'],
                'price': tool_data.get('price'),
                'pricing_model': tool_data['pricing_model'],
                'rating': tool_data['rating'],
                'review_count': tool_data['review_count'],
                'click_count': tool_data['click_count'],
                'icon': tool_data['icon'],
                'documentation_url': tool_data['documentation_url'],
                'author': author
            }
        )
        if created:
            print(f"  ✅ Created tool: {tool.name}")
        else:
            print(f"  ℹ️  Tool already exists: {tool.name}")
        created_tools.append(tool)
    
    # Create revenue reports
    print("\n💰 Creating revenue reports...")
    revenue_reports_data = [
        {
            'website_name': 'TechBlog Pro',
            'revenue_monthly': Decimal('12500.00'),
            'revenue_yearly': Decimal('150000.00'),
            'description': 'Technology blog focused on AI and software development with premium content and courses.',
            'traffic_monthly': 45000,
            'conversion_rate': 2.8,
            'profit_margin': 65.5,
            'is_featured': True
        },
        {
            'website_name': 'Marketing Masters',
            'revenue_monthly': Decimal('8900.00'),
            'revenue_yearly': Decimal('106800.00'),
            'description': 'Digital marketing resource site with tools, templates, and consulting services.',
            'traffic_monthly': 32000,
            'conversion_rate': 2.1,
            'profit_margin': 58.2,
            'is_featured': False
        },
        {
            'website_name': 'Productivity Hub',
            'revenue_monthly': Decimal('6700.00'),
            'revenue_yearly': Decimal('80400.00'),
            'description': 'Productivity and personal development platform with courses and coaching.',
            'traffic_monthly': 28000,
            'conversion_rate': 1.9,
            'profit_margin': 72.1,
            'is_featured': True
        },
        {
            'website_name': 'Design Studio',
            'revenue_monthly': Decimal('11200.00'),
            'revenue_yearly': Decimal('134400.00'),
            'description': 'Creative design marketplace selling templates, graphics, and design services.',
            'traffic_monthly': 38000,
            'conversion_rate': 3.2,
            'profit_margin': 61.8,
            'is_featured': False
        },
        {
            'website_name': 'Business Insights',
            'revenue_monthly': Decimal('9500.00'),
            'revenue_yearly': Decimal('114000.00'),
            'description': 'Business strategy and entrepreneurship content with premium reports and consulting.',
            'traffic_monthly': 35000,
            'conversion_rate': 2.5,
            'profit_margin': 68.4,
            'is_featured': True
        }
    ]
    
    created_revenue_reports = []
    for report_data in revenue_reports_data:
        author = random.choice(created_users)
        
        report, created = RevenueReport.objects.get_or_create(
            website_name=report_data['website_name'],
            defaults={
                'revenue_monthly': report_data['revenue_monthly'],
                'revenue_yearly': report_data['revenue_yearly'],
                'description': report_data['description'],
                'traffic_monthly': report_data['traffic_monthly'],
                'conversion_rate': report_data['conversion_rate'],
                'profit_margin': report_data['profit_margin'],
                'is_featured': report_data['is_featured'],
                'author': author
            }
        )
        if created:
            print(f"  ✅ Created revenue report: {report.website_name}")
        else:
            print(f"  ℹ️  Revenue report already exists: {report.website_name}")
        created_revenue_reports.append(report)
    
    # Create newsletter reports
    print("\n📊 Creating newsletter reports...")
    newsletter_reports_data = [
        {
            'title': 'Q1 2024 Newsletter Performance Report',
            'description': 'Comprehensive analysis of newsletter performance for Q1 2024, including subscriber growth, engagement metrics, and revenue impact.',
            'total_subscribers': 15420,
            'open_rate': 24.8,
            'click_rate': 3.2,
            'conversion_rate': 1.8,
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 3, 31),
            'is_featured': True
        },
        {
            'title': 'Email Marketing Campaign Analysis - March 2024',
            'description': 'Detailed analysis of email marketing campaigns in March 2024, including A/B test results and optimization recommendations.',
            'total_subscribers': 14850,
            'open_rate': 26.1,
            'click_rate': 3.5,
            'conversion_rate': 2.1,
            'start_date': date(2024, 3, 1),
            'end_date': date(2024, 3, 31),
            'is_featured': False
        },
        {
            'title': 'Subscriber Engagement Deep Dive',
            'description': 'In-depth analysis of subscriber engagement patterns, segment performance, and personalization strategies.',
            'total_subscribers': 15200,
            'open_rate': 28.3,
            'click_rate': 4.1,
            'conversion_rate': 2.3,
            'start_date': date(2024, 2, 1),
            'end_date': date(2024, 4, 30),
            'is_featured': True
        }
    ]
    
    created_newsletter_reports = []
    for report_data in newsletter_reports_data:
        author = random.choice(created_users)
        
        report, created = NewsletterReport.objects.get_or_create(
            title=report_data['title'],
            defaults={
                'description': report_data['description'],
                'total_subscribers': report_data['total_subscribers'],
                'open_rate': report_data['open_rate'],
                'click_rate': report_data['click_rate'],
                'conversion_rate': report_data['conversion_rate'],
                'start_date': report_data['start_date'],
                'end_date': report_data['end_date'],
                'is_featured': report_data['is_featured'],
                'author': author
            }
        )
        if created:
            print(f"  ✅ Created newsletter report: {report.title}")
        else:
            print(f"  ℹ️  Newsletter report already exists: {report.title}")
        created_newsletter_reports.append(report)
    
    # Create analytics reports
    print("\n📈 Creating analytics reports...")
    analytics_reports_data = [
        {
            'title': 'Website Traffic Analysis - Q1 2024',
            'description': 'Comprehensive analysis of website traffic patterns, user behavior, and conversion optimization opportunities.',
            'report_type': 'traffic',
            'data': {
                'total_visitors': 125000,
                'unique_visitors': 89000,
                'page_views': 450000,
                'avg_session_duration': 245,
                'bounce_rate': 42.3,
                'top_pages': [
                    {'page': '/home', 'views': 25000},
                    {'page': '/articles', 'views': 18000},
                    {'page': '/newsletter', 'views': 12000},
                    {'page': '/tools', 'views': 8000},
                    {'page': '/playbooks', 'views': 6000}
                ],
                'traffic_sources': {
                    'organic': 45.2,
                    'direct': 28.1,
                    'social': 15.3,
                    'email': 8.7,
                    'referral': 2.7
                }
            },
            'is_featured': True
        },
        {
            'title': 'Content Performance Report',
            'description': 'Analysis of content performance across different channels and content types.',
            'report_type': 'content',
            'data': {
                'total_articles': 45,
                'total_newsletters': 12,
                'total_playbooks': 8,
                'avg_engagement_rate': 4.2,
                'top_performing_content': [
                    {'title': 'AI in Business Trends', 'views': 8500, 'engagement': 6.8},
                    {'title': 'Productivity Hacks Guide', 'views': 7200, 'engagement': 5.9},
                    {'title': 'Email Marketing Mastery', 'views': 6800, 'engagement': 5.2}
                ],
                'content_categories': {
                    'technology': 35.2,
                    'productivity': 28.1,
                    'marketing': 22.3,
                    'business': 14.4
                }
            },
            'is_featured': False
        },
        {
            'title': 'User Engagement Metrics',
            'description': 'Detailed analysis of user engagement patterns and behavior across the platform.',
            'report_type': 'engagement',
            'data': {
                'avg_time_on_site': 325,
                'pages_per_session': 3.2,
                'return_visitor_rate': 34.5,
                'mobile_vs_desktop': {
                    'mobile': 58.2,
                    'desktop': 41.8
                },
                'engagement_by_device': {
                    'mobile': 2.8,
                    'desktop': 4.1,
                    'tablet': 3.5
                },
                'peak_usage_hours': [
                    {'hour': 9, 'users': 8500},
                    {'hour': 12, 'users': 9200},
                    {'hour': 15, 'users': 7800},
                    {'hour': 19, 'users': 6800}
                ]
            },
            'is_featured': True
        }
    ]
    
    created_analytics_reports = []
    for report_data in analytics_reports_data:
        author = random.choice(created_users)
        
        report, created = AnalyticsReport.objects.get_or_create(
            title=report_data['title'],
            defaults={
                'description': report_data['description'],
                'report_type': report_data['report_type'],
                'data': report_data['data'],
                'is_featured': report_data['is_featured'],
                'author': author
            }
        )
        if created:
            print(f"  ✅ Created analytics report: {report.title}")
        else:
            print(f"  ℹ️  Analytics report already exists: {report.title}")
        created_analytics_reports.append(report)
    
    print("\n✅ Complete test data created successfully!")
    print(f"\n📊 Summary:")
    print(f"  👥 Users: {CustomUser.objects.count()}")
    print(f"  📚 Topics: {Topic.objects.count()}")
    print(f"  📝 Articles: {Article.objects.count()}")
    print(f"  📧 Templates: {NewsletterTemplate.objects.count()}")
    print(f"  👥 Subscribers: {Subscriber.objects.count()}")
    print(f"  📰 Newsletters: {Newsletter.objects.count()}")
    print(f"  📚 Playbooks: {Playbook.objects.count()}")
    print(f"  🛠️ Tools: {Tool.objects.count()}")
    print(f"  💰 Revenue Reports: {RevenueReport.objects.count()}")
    print(f"  📊 Newsletter Reports: {NewsletterReport.objects.count()}")
    print(f"  📈 Analytics Reports: {AnalyticsReport.objects.count()}")
    
    print(f"\n🔑 Test Login Credentials:")
    print(f"  Email: admin@newsletter.com")
    print(f"  Password: testpass123")
    print(f"  Email: test@newsletter.com")
    print(f"  Password: testpass123")

if __name__ == '__main__':
    create_complete_test_data() 