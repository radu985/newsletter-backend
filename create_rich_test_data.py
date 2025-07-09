#!/usr/bin/env python
import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

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

def create_rich_test_data():
    print("🚀 Creating rich test data for the newsletter project...")
    
    # Create users
    print("\n👥 Creating users...")
    users_data = [
        {'email': 'admin@newsletter.com', 'name': 'Admin User', 'is_staff': True, 'is_superuser': True, 'is_premium': True},
        {'email': 'editor@newsletter.com', 'name': 'Sarah Editor', 'is_staff': True, 'is_premium': True},
        {'email': 'writer@newsletter.com', 'name': 'John Writer', 'is_premium': True},
        {'email': 'contributor@newsletter.com', 'name': 'Maria Contributor', 'is_premium': False},
        {'email': 'test@newsletter.com', 'name': 'Test User', 'is_premium': False},
        {'email': 'demo@newsletter.com', 'name': 'Demo User', 'is_premium': True},
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
    
    # Create topics
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
    
    # Create articles
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
        },
        {
            'title': 'Digital Marketing Trends for 2024',
            'content': '''
            <h2>Stay ahead of the curve with these digital marketing trends</h2>
            <p>The digital marketing landscape is constantly evolving. Here are the key trends that will shape marketing strategies in 2024 and beyond.</p>
            
            <h3>1. AI-Powered Marketing Automation</h3>
            <p>Artificial intelligence is revolutionizing marketing automation, enabling more sophisticated targeting, personalization, and campaign optimization.</p>
            
            <h3>2. Voice Search Optimization</h3>
            <p>With the growing popularity of voice assistants, optimizing for voice search is becoming increasingly important for SEO and content marketing.</p>
            
            <h3>3. Video Marketing Dominance</h3>
            <p>Video content continues to dominate social media and search results. Short-form videos, live streaming, and interactive video experiences are key trends.</p>
            
            <h3>4. Privacy-First Marketing</h3>
            <p>With increasing privacy regulations and consumer concerns, marketers are adopting privacy-first approaches that respect user data while still delivering personalized experiences.</p>
            
            <h3>5. Social Commerce Integration</h3>
            <p>Social media platforms are becoming shopping destinations, with features that allow users to discover and purchase products without leaving the platform.</p>
            
            <h3>6. Sustainability Marketing</h3>
            <p>Consumers are increasingly choosing brands that align with their values, particularly around sustainability and social responsibility.</p>
            
            <h3>7. Micro-Influencer Partnerships</h3>
            <p>Brands are shifting from celebrity endorsements to partnerships with micro-influencers who have smaller but more engaged and authentic followings.</p>
            
            <h3>8. Interactive Content</h3>
            <p>Interactive content like quizzes, polls, and augmented reality experiences are driving higher engagement and providing valuable data about consumer preferences.</p>
            
            <p>The key to success in digital marketing is staying adaptable and continuously learning about new technologies and consumer behaviors.</p>
            ''',
            'topic': 'Marketing',
            'is_published': True
        },
        {
            'title': 'Building a Sustainable Business Model',
            'content': '''
            <h2>How to create a business that thrives in the long term</h2>
            <p>Sustainability in business goes beyond environmental concerns—it's about creating a business model that can thrive and adapt over time. Here's how to build a sustainable business.</p>
            
            <h3>1. Focus on Customer Value</h3>
            <p>The foundation of any sustainable business is providing genuine value to customers. Understand their needs deeply and continuously improve your offerings.</p>
            
            <h3>2. Build Strong Relationships</h3>
            <p>Develop long-term relationships with customers, employees, suppliers, and other stakeholders. These relationships are the backbone of sustainable growth.</p>
            
            <h3>3. Diversify Revenue Streams</h3>
            <p>Don't rely on a single source of revenue. Diversify your income streams to reduce risk and increase stability.</p>
            
            <h3>4. Invest in Innovation</h3>
            <p>Continuously invest in research and development to stay ahead of the competition and adapt to changing market conditions.</p>
            
            <h3>5. Maintain Financial Discipline</h3>
            <p>Keep your finances healthy by maintaining adequate cash reserves, managing debt wisely, and making strategic investments.</p>
            
            <h3>6. Build a Strong Team</h3>
            <p>Your people are your most valuable asset. Invest in hiring, training, and retaining top talent.</p>
            
            <h3>7. Embrace Technology</h3>
            <p>Use technology to improve efficiency, reduce costs, and enhance customer experiences.</p>
            
            <h3>8. Plan for the Long Term</h3>
            <p>Make decisions with the long-term health of your business in mind, not just short-term gains.</p>
            
            <p>Building a sustainable business takes time and patience, but the rewards are worth the effort.</p>
            ''',
            'topic': 'Business',
            'is_published': True
        },
        {
            'title': 'The Science of Habit Formation',
            'content': '''
            <h2>How to build positive habits that stick</h2>
            <p>Habits are the compound interest of self-improvement. Small changes, when repeated consistently, can lead to remarkable results over time.</p>
            
            <h3>Understanding the Habit Loop</h3>
            <p>Every habit follows a three-step pattern: cue, craving, response, and reward. Understanding this loop is key to changing habits.</p>
            
            <h3>1. Make It Obvious</h3>
            <p>Design your environment to make good habits obvious and bad habits invisible. Use visual cues and strategic placement.</p>
            
            <h3>2. Make It Attractive</h3>
            <p>Pair new habits with activities you enjoy. This creates a positive association that makes the habit more appealing.</p>
            
            <h3>3. Make It Easy</h3>
            <p>Reduce friction for good habits and increase friction for bad ones. Start with small, manageable steps.</p>
            
            <h3>4. Make It Satisfying</h3>
            <p>Provide immediate rewards for completing your habits. This reinforces the behavior and makes it more likely to stick.</p>
            
            <h3>5. Track Your Progress</h3>
            <p>Use habit trackers to visualize your progress and maintain motivation. Seeing your streak can be incredibly motivating.</p>
            
            <h3>6. Stack Your Habits</h3>
            <p>Link new habits to existing ones. This creates a natural trigger that makes it easier to remember and perform the new habit.</p>
            
            <h3>7. Be Patient</h3>
            <p>Habits take time to form. Research suggests it can take anywhere from 18 to 254 days to form a new habit, with an average of 66 days.</p>
            
            <p>Remember, the goal is not perfection but consistency. Focus on showing up every day, even if it's just for a few minutes.</p>
            ''',
            'topic': 'Personal Development',
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
    
    # Create newsletter templates
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
        },
        {
            'name': 'Product Update',
            'subject_template': '🚀 {{ title }} - New Features & Updates',
            'html_template': '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{{ title }}</title>
            </head>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 20px; border-radius: 10px; text-align: center;">
                    <h1 style="margin: 0;">🚀 {{ title }}</h1>
                </div>
                <div style="padding: 20px 0;">
                    {{ content|safe }}
                </div>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px;">
                    <h3 style="margin-top: 0;">What's New?</h3>
                    <ul>
                        <li>Enhanced features</li>
                        <li>Improved performance</li>
                        <li>Better user experience</li>
                        <li>New integrations</li>
                    </ul>
                </div>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{{ site_url }}" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Learn More</a>
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
            🚀 {{ title }}
            
            {{ content }}
            
            What's New?
            - Enhanced features
            - Improved performance
            - Better user experience
            - New integrations
            
            Learn More: {{ site_url }}
            
            ---
            You received this email because you're subscribed to our newsletter.
            To unsubscribe, visit: {{ unsubscribe_url }}
            '''
        },
        {
            'name': 'Industry Insights',
            'subject_template': '📊 {{ title }} - Industry Analysis & Trends',
            'html_template': '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{{ title }}</title>
            </head>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: white; padding: 20px; border-radius: 10px; text-align: center;">
                    <h1 style="margin: 0;">📊 {{ title }}</h1>
                </div>
                <div style="padding: 20px 0;">
                    {{ content|safe }}
                </div>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px;">
                    <h3 style="margin-top: 0;">Key Takeaways</h3>
                    <ul>
                        <li>Market trends analysis</li>
                        <li>Expert insights</li>
                        <li>Actionable recommendations</li>
                        <li>Future predictions</li>
                    </ul>
                </div>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{{ site_url }}/reports" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">View Full Report</a>
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
            📊 {{ title }}
            
            {{ content }}
            
            Key Takeaways:
            - Market trends analysis
            - Expert insights
            - Actionable recommendations
            - Future predictions
            
            View Full Report: {{ site_url }}/reports
            
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
    
    # Create subscribers
    print("\n👥 Creating subscribers...")
    subscribers_data = [
        {'email': 'john.doe@example.com', 'first_name': 'John', 'last_name': 'Doe', 'frequency': 'weekly', 'source': 'website'},
        {'email': 'jane.smith@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'frequency': 'biweekly', 'source': 'admin'},
        {'email': 'mike.johnson@example.com', 'first_name': 'Mike', 'last_name': 'Johnson', 'frequency': 'monthly', 'source': 'import'},
        {'email': 'sarah.wilson@example.com', 'first_name': 'Sarah', 'last_name': 'Wilson', 'frequency': 'weekly', 'source': 'website'},
        {'email': 'david.brown@example.com', 'first_name': 'David', 'last_name': 'Brown', 'frequency': 'weekly', 'source': 'admin'},
        {'email': 'emma.davis@example.com', 'first_name': 'Emma', 'last_name': 'Davis', 'frequency': 'biweekly', 'source': 'website'},
        {'email': 'alex.garcia@example.com', 'first_name': 'Alex', 'last_name': 'Garcia', 'frequency': 'monthly', 'source': 'import'},
        {'email': 'lisa.martinez@example.com', 'first_name': 'Lisa', 'last_name': 'Martinez', 'frequency': 'weekly', 'source': 'website'},
        {'email': 'tom.anderson@example.com', 'first_name': 'Tom', 'last_name': 'Anderson', 'frequency': 'biweekly', 'source': 'admin'},
        {'email': 'rachel.lee@example.com', 'first_name': 'Rachel', 'last_name': 'Lee', 'frequency': 'weekly', 'source': 'website'},
        {'email': 'chris.taylor@example.com', 'first_name': 'Chris', 'last_name': 'Taylor', 'frequency': 'monthly', 'source': 'import'},
        {'email': 'amanda.white@example.com', 'first_name': 'Amanda', 'last_name': 'White', 'frequency': 'weekly', 'source': 'website'},
        {'email': 'kevin.clark@example.com', 'first_name': 'Kevin', 'last_name': 'Clark', 'frequency': 'biweekly', 'source': 'admin'},
        {'email': 'jessica.hall@example.com', 'first_name': 'Jessica', 'last_name': 'Hall', 'frequency': 'monthly', 'source': 'website'},
        {'email': 'ryan.young@example.com', 'first_name': 'Ryan', 'last_name': 'Young', 'frequency': 'weekly', 'source': 'import'},
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
    
    # Create newsletters
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
        },
        {
            'title': 'Top 10 Productivity Tips for 2024',
            'subject': 'Boost Your Productivity with These 10 Proven Tips',
            'content': '''
            <h2>Maximize Your Productivity in 2024</h2>
            <p>Here are our top 10 productivity tips that will help you achieve more:</p>
            <ol>
                <li><strong>Time Blocking:</strong> Schedule specific time slots for different tasks</li>
                <li><strong>Pomodoro Technique:</strong> Work in 25-minute focused sessions</li>
                <li><strong>Digital Minimalism:</strong> Reduce digital distractions</li>
                <li><strong>Morning Routine:</strong> Start your day with intention</li>
                <li><strong>Task Batching:</strong> Group similar tasks together</li>
                <li><strong>Energy Management:</strong> Work on important tasks when you're most alert</li>
                <li><strong>Single Tasking:</strong> Focus on one thing at a time</li>
                <li><strong>Regular Breaks:</strong> Take short breaks to maintain focus</li>
                <li><strong>Goal Setting:</strong> Set clear, achievable goals</li>
                <li><strong>Continuous Learning:</strong> Invest in your skills and knowledge</li>
            </ol>
            <p>Implement these tips gradually and watch your productivity soar!</p>
            ''',
            'status': 'sent',
            'template': 'Weekly Newsletter'
        },
        {
            'title': 'Monthly Industry Roundup - January 2024',
            'subject': 'Industry Insights: What Happened in January 2024',
            'content': '''
            <h2>January 2024 Industry Highlights</h2>
            <p>Here's what's been happening in our industry this month:</p>
            
            <h3>🚀 Major Developments</h3>
            <ul>
                <li>New AI regulations announced</li>
                <li>Major tech company acquisitions</li>
                <li>Breakthrough in sustainable technology</li>
            </ul>
            
            <h3>📊 Market Trends</h3>
            <ul>
                <li>Remote work continues to evolve</li>
                <li>Cybersecurity concerns on the rise</li>
                <li>Green technology gaining momentum</li>
            </ul>
            
            <h3>🎯 What This Means for You</h3>
            <p>These developments present both challenges and opportunities. Stay informed and adapt your strategies accordingly.</p>
            ''',
            'status': 'sent',
            'template': 'Industry Insights'
        },
        {
            'title': 'New Features Released - February 2024',
            'subject': '🚀 Exciting New Features Just Released!',
            'content': '''
            <h2>We're excited to announce our latest features!</h2>
            <p>After months of development and testing, we're proud to release these new features that will enhance your experience:</p>
            
            <h3>🎯 Enhanced Analytics Dashboard</h3>
            <p>Get deeper insights into your performance with our new analytics dashboard featuring real-time data, customizable reports, and advanced filtering options.</p>
            
            <h3>🤖 AI-Powered Recommendations</h3>
            <p>Our new AI system analyzes your behavior and provides personalized recommendations to help you achieve your goals faster.</p>
            
            <h3>📱 Mobile App Improvements</h3>
            <p>We've completely redesigned our mobile app with a focus on speed, usability, and offline functionality.</p>
            
            <h3>🔒 Enhanced Security Features</h3>
            <p>New security features including two-factor authentication, advanced encryption, and automated threat detection.</p>
            
            <p>Try these features today and let us know what you think!</p>
            ''',
            'status': 'scheduled',
            'template': 'Product Update'
        },
        {
            'title': 'Q1 2024 Business Strategy Guide',
            'subject': 'Your Complete Q1 2024 Business Strategy Guide',
            'content': '''
            <h2>Plan Your Q1 2024 Success</h2>
            <p>As we begin a new quarter, it's the perfect time to review and refine your business strategy. Here's our comprehensive guide to help you succeed in Q1 2024.</p>
            
            <h3>📈 Market Analysis</h3>
            <p>Current market conditions and what to expect in the coming months. We'll help you identify opportunities and prepare for potential challenges.</p>
            
            <h3>🎯 Goal Setting Framework</h3>
            <p>A proven framework for setting and achieving your business goals, including SMART goal methodology and progress tracking.</p>
            
            <h3>💰 Financial Planning</h3>
            <p>Essential financial planning strategies for Q1, including budgeting, cash flow management, and investment priorities.</p>
            
            <h3>👥 Team Development</h3>
            <p>How to build and motivate your team for maximum productivity and engagement in the new quarter.</p>
            
            <h3>🚀 Growth Strategies</h3>
            <p>Proven strategies for sustainable business growth, including market expansion, product development, and customer acquisition.</p>
            
            <p>Download our complete Q1 strategy template and start planning your success today!</p>
            ''',
            'status': 'draft',
            'template': 'Industry Insights'
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
    
    # Create newsletter sends and analytics
    print("\n📊 Creating newsletter sends and analytics...")
    for newsletter in created_newsletters:
        if newsletter.status == 'sent':
            # Create newsletter sends for each subscriber
            for subscriber in created_subscribers:
                # Randomize engagement metrics
                is_opened = random.choice([True, False, False, False])  # 25% open rate
                is_clicked = random.choice([True, False, False, False, False]) if is_opened else False  # 20% click rate of opens
                
                status = 'clicked' if is_clicked else ('opened' if is_opened else 'delivered')
                
                sent_at_val = newsletter.sent_at
                if sent_at_val:
                    delivered_at = sent_at_val + timedelta(minutes=random.randint(1, 10))
                    opened_at = delivered_at + timedelta(minutes=random.randint(5, 60)) if is_opened else None
                    clicked_at = opened_at + timedelta(minutes=random.randint(1, 30)) if is_clicked and opened_at else None
                else:
                    delivered_at = None
                    opened_at = None
                    clicked_at = None
                
                newsletter_send, created = NewsletterSend.objects.get_or_create(
                    newsletter=newsletter,
                    subscriber=subscriber,
                    defaults={
                        'status': status,
                        'sent_at': sent_at_val,
                        'delivered_at': delivered_at,
                        'opened_at': opened_at,
                        'clicked_at': clicked_at,
                        'open_count': 1 if is_opened else 0,
                        'click_count': 1 if is_clicked else 0,
                        'message_id': f"msg_{random.randint(100000, 999999)}"
                    }
                )
            
            # Create analytics
            analytics, created = NewsletterAnalytics.objects.get_or_create(
                newsletter=newsletter,
                defaults={
                    'total_sent': newsletter.total_sent,
                    'total_delivered': newsletter.total_delivered,
                    'total_bounced': 0,
                    'total_opened': newsletter.total_opened,
                    'total_clicked': newsletter.total_clicked,
                    'total_unsubscribed': random.randint(0, 2),
                }
            )
            
            # Calculate rates
            if analytics.total_sent > 0:
                analytics.delivery_rate = (analytics.total_delivered / analytics.total_sent) * 100
                analytics.open_rate = (analytics.total_opened / analytics.total_sent) * 100
                analytics.click_rate = (analytics.total_clicked / analytics.total_sent) * 100
                analytics.unsubscribe_rate = (analytics.total_unsubscribed / analytics.total_sent) * 100
            
            analytics.save()
    
    # Update subscriber analytics
    print("\n📈 Updating subscriber analytics...")
    for subscriber in created_subscribers:
        # Get all sends for this subscriber
        sends = NewsletterSend.objects.filter(subscriber=subscriber)
        
        subscriber.total_emails_received = sends.count()
        subscriber.total_emails_opened = sends.filter(status__in=['opened', 'clicked']).count()
        subscriber.total_emails_clicked = sends.filter(status='clicked').count()
        
        # Set last email dates
        last_sent = sends.order_by('-sent_at').first()
        if last_sent:
            subscriber.last_email_sent = last_sent.sent_at
        
        last_opened = sends.filter(status__in=['opened', 'clicked']).order_by('-opened_at').first()
        if last_opened:
            subscriber.last_email_opened = last_opened.opened_at
        
        subscriber.save()
    
    print("\n✅ Rich test data created successfully!")
    print(f"\n📊 Summary:")
    print(f"  👥 Users: {CustomUser.objects.count()}")
    print(f"  📚 Topics: {Topic.objects.count()}")
    print(f"  📝 Articles: {Article.objects.count()}")
    print(f"  📧 Templates: {NewsletterTemplate.objects.count()}")
    print(f"  👥 Subscribers: {Subscriber.objects.count()}")
    print(f"  📰 Newsletters: {Newsletter.objects.count()}")
    print(f"  📊 Newsletter Sends: {NewsletterSend.objects.count()}")
    print(f"  📈 Analytics Records: {NewsletterAnalytics.objects.count()}")
    
    print(f"\n🔑 Test Login Credentials:")
    print(f"  Email: admin@newsletter.com")
    print(f"  Password: testpass123")
    print(f"  Email: test@newsletter.com")
    print(f"  Password: testpass123")

if __name__ == '__main__':
    create_rich_test_data() 