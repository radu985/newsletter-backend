#!/usr/bin/env python
import os
import django
import random
from datetime import datetime, timedelta, date
from django.utils import timezone
from decimal import Decimal
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_mockup_data():
    """Create mockup data for frontend testing"""
    
    print("🎨 Creating mockup data for frontend testing...")
    
    # Dashboard statistics
    dashboard_stats = {
        "total_subscribers": 15420,
        "total_newsletters": 45,
        "total_articles": 23,
        "total_revenue": 125000,
        "growth_rate": 12.5,
        "active_users": 8920,
        "conversion_rate": 3.2,
        "open_rate": 24.8
    }
    
    # Chart data for subscriber growth
    subscriber_growth = []
    start_date = date(2024, 1, 1)
    base_subscribers = 12000
    
    for i in range(90):  # 3 months of data
        current_date = start_date + timedelta(days=i)
        growth_factor = 1 + (i * 0.001) + random.uniform(-0.002, 0.002)
        subscribers = int(base_subscribers * growth_factor)
        
        subscriber_growth.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "subscribers": subscribers,
            "new_subscribers": random.randint(5, 25),
            "unsubscribers": random.randint(1, 8)
        })
    
    # Newsletter performance data
    newsletter_performance = [
        {
            "title": "Welcome to Our Newsletter!",
            "sent": 15420,
            "delivered": 15100,
            "opened": 3740,
            "clicked": 480,
            "bounced": 320,
            "open_rate": 24.8,
            "click_rate": 3.2,
            "date": "2024-03-15"
        },
        {
            "title": "Top 10 Productivity Tips for 2024",
            "sent": 15420,
            "delivered": 15050,
            "opened": 3920,
            "clicked": 520,
            "bounced": 370,
            "open_rate": 26.0,
            "click_rate": 3.5,
            "date": "2024-03-08"
        },
        {
            "title": "Monthly Industry Roundup - January 2024",
            "sent": 14800,
            "delivered": 14500,
            "opened": 3550,
            "clicked": 440,
            "bounced": 300,
            "open_rate": 24.5,
            "click_rate": 3.0,
            "date": "2024-02-29"
        },
        {
            "title": "New Features Released - February 2024",
            "sent": 14800,
            "delivered": 14450,
            "opened": 3780,
            "clicked": 510,
            "bounced": 350,
            "open_rate": 26.2,
            "click_rate": 3.5,
            "date": "2024-02-22"
        },
        {
            "title": "Q1 2024 Business Strategy Guide",
            "sent": 14200,
            "delivered": 13900,
            "opened": 3420,
            "clicked": 430,
            "bounced": 300,
            "open_rate": 24.6,
            "click_rate": 3.1,
            "date": "2024-02-15"
        }
    ]
    
    # Revenue data
    revenue_data = []
    base_revenue = 8000
    
    for i in range(12):  # 12 months
        month = i + 1
        growth_factor = 1 + (i * 0.05) + random.uniform(-0.02, 0.02)
        revenue = int(base_revenue * growth_factor)
        
        revenue_data.append({
            "month": f"2024-{month:02d}",
            "revenue": revenue,
            "growth": round((growth_factor - 1) * 100, 1),
            "subscriptions": random.randint(800, 1200),
            "courses": random.randint(200, 400),
            "consulting": random.randint(100, 300)
        })
    
    # Top performing content
    top_content = [
        {
            "title": "The Future of AI in Business: 2024 Trends",
            "views": 8500,
            "engagement": 6.8,
            "shares": 420,
            "comments": 89,
            "category": "Technology",
            "published_date": "2024-03-10"
        },
        {
            "title": "10 Productivity Hacks That Actually Work",
            "views": 7200,
            "engagement": 5.9,
            "shares": 380,
            "comments": 67,
            "category": "Productivity",
            "published_date": "2024-03-05"
        },
        {
            "title": "Email Marketing Mastery Playbook",
            "views": 6800,
            "engagement": 5.2,
            "shares": 320,
            "comments": 45,
            "category": "Marketing",
            "published_date": "2024-02-28"
        },
        {
            "title": "Digital Marketing Trends for 2024",
            "views": 6100,
            "engagement": 4.8,
            "shares": 290,
            "comments": 52,
            "category": "Marketing",
            "published_date": "2024-02-20"
        },
        {
            "title": "Building a Sustainable Business Model",
            "views": 5800,
            "engagement": 4.5,
            "shares": 270,
            "comments": 38,
            "category": "Business",
            "published_date": "2024-02-15"
        }
    ]
    
    # User activity data
    user_activity = []
    for i in range(24):  # 24 hours
        hour = i
        users_online = random.randint(50, 200)
        if 9 <= hour <= 17:  # Business hours
            users_online = random.randint(150, 300)
        
        user_activity.append({
            "hour": hour,
            "users_online": users_online,
            "page_views": users_online * random.randint(2, 5),
            "newsletter_signups": random.randint(0, 5),
            "tool_downloads": random.randint(0, 3)
        })
    
    # Geographic data
    geographic_data = [
        {"country": "United States", "users": 4520, "percentage": 29.3},
        {"country": "United Kingdom", "users": 2340, "percentage": 15.2},
        {"country": "Canada", "users": 1890, "percentage": 12.3},
        {"country": "Australia", "users": 1560, "percentage": 10.1},
        {"country": "Germany", "users": 1230, "percentage": 8.0},
        {"country": "France", "users": 980, "percentage": 6.4},
        {"country": "Netherlands", "users": 760, "percentage": 4.9},
        {"country": "Sweden", "users": 620, "percentage": 4.0},
        {"country": "Other", "users": 1520, "percentage": 9.8}
    ]
    
    # Device usage data
    device_data = [
        {"device": "Desktop", "users": 8920, "percentage": 57.9},
        {"device": "Mobile", "users": 5420, "percentage": 35.2},
        {"device": "Tablet", "users": 1080, "percentage": 7.0}
    ]
    
    # Traffic sources
    traffic_sources = [
        {"source": "Organic Search", "users": 6950, "percentage": 45.2},
        {"source": "Direct", "users": 4320, "percentage": 28.1},
        {"source": "Social Media", "users": 2350, "percentage": 15.3},
        {"source": "Email", "users": 1340, "percentage": 8.7},
        {"source": "Referral", "users": 410, "percentage": 2.7}
    ]
    
    # Recent activities
    recent_activities = [
        {
            "type": "newsletter_sent",
            "title": "Welcome to Our Newsletter!",
            "description": "Newsletter sent to 15,420 subscribers",
            "timestamp": "2024-03-15T10:30:00Z",
            "user": "admin@newsletter.com",
            "icon": "📧"
        },
        {
            "type": "article_published",
            "title": "The Future of AI in Business: 2024 Trends",
            "description": "New article published",
            "timestamp": "2024-03-10T14:15:00Z",
            "user": "writer@newsletter.com",
            "icon": "📝"
        },
        {
            "type": "playbook_created",
            "title": "Email Marketing Mastery Playbook",
            "description": "New playbook created",
            "timestamp": "2024-03-08T09:45:00Z",
            "user": "editor@newsletter.com",
            "icon": "📚"
        },
        {
            "type": "tool_added",
            "title": "Canva",
            "description": "New tool added to the directory",
            "timestamp": "2024-03-05T16:20:00Z",
            "user": "admin@newsletter.com",
            "icon": "🛠️"
        },
        {
            "type": "report_generated",
            "title": "Q1 2024 Newsletter Performance Report",
            "description": "Analytics report generated",
            "timestamp": "2024-03-01T11:00:00Z",
            "user": "analyst@newsletter.com",
            "icon": "📊"
        }
    ]
    
    # Notification data
    notifications = [
        {
            "id": 1,
            "type": "success",
            "title": "Newsletter Sent Successfully",
            "message": "Your newsletter 'Welcome to Our Newsletter!' has been sent to 15,420 subscribers.",
            "timestamp": "2024-03-15T10:30:00Z",
            "read": False
        },
        {
            "id": 2,
            "type": "info",
            "title": "New Subscriber Milestone",
            "message": "Congratulations! You've reached 15,000 subscribers.",
            "timestamp": "2024-03-14T15:20:00Z",
            "read": False
        },
        {
            "id": 3,
            "type": "warning",
            "title": "High Bounce Rate",
            "message": "Your recent newsletter had a bounce rate of 2.1%, which is above the recommended threshold.",
            "timestamp": "2024-03-13T09:15:00Z",
            "read": True
        },
        {
            "id": 4,
            "type": "success",
            "title": "Article Published",
            "message": "Your article 'The Future of AI in Business: 2024 Trends' has been published successfully.",
            "timestamp": "2024-03-10T14:15:00Z",
            "read": True
        }
    ]
    
    # Create mockup data file
    mockup_data = {
        "dashboard_stats": dashboard_stats,
        "subscriber_growth": subscriber_growth,
        "newsletter_performance": newsletter_performance,
        "revenue_data": revenue_data,
        "top_content": top_content,
        "user_activity": user_activity,
        "geographic_data": geographic_data,
        "device_data": device_data,
        "traffic_sources": traffic_sources,
        "recent_activities": recent_activities,
        "notifications": notifications
    }
    
    # Save to file
    with open('mockup_data.json', 'w') as f:
        json.dump(mockup_data, f, indent=2)
    
    print("✅ Mockup data created successfully!")
    print("📁 Saved to: mockup_data.json")
    print("\n📊 Mockup data includes:")
    print("  📈 Dashboard statistics")
    print("  📊 Subscriber growth charts")
    print("  📧 Newsletter performance data")
    print("  💰 Revenue analytics")
    print("  📝 Top performing content")
    print("  👥 User activity tracking")
    print("  🌍 Geographic distribution")
    print("  📱 Device usage statistics")
    print("  🔗 Traffic sources")
    print("  ⏰ Recent activities")
    print("  🔔 Notifications")
    
    return mockup_data

if __name__ == '__main__':
    create_mockup_data() 