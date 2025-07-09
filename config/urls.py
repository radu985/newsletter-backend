"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

@csrf_exempt
def api_info(request):
    """Simple API info endpoint for the root URL"""
    return JsonResponse({
        'message': 'Newsletter API is running!',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'users': '/api/users/',
            'articles': '/api/articles/',
            'playbooks': '/api/playbooks/',
            'tools': '/api/tools/',
            'reports': '/api/reports/',
            'newsletters': '/api/newsletters/',
            'mockup_data': '/api/mockup-data/',
        },
        'status': 'active'
    })

@csrf_exempt
def mockup_data(request):
    """Serve mockup data for frontend testing"""
    try:
        # Try to load from file first
        mockup_file = os.path.join(settings.BASE_DIR, 'mockup_data.json')
        if os.path.exists(mockup_file):
            with open(mockup_file, 'r') as f:
                data = json.load(f)
        else:
            # Fallback to basic data
            data = {
                "dashboard_stats": {
                    "total_subscribers": 15420,
                    "total_newsletters": 45,
                    "total_articles": 23,
                    "total_revenue": 125000,
                    "growth_rate": 12.5,
                    "active_users": 8920,
                    "conversion_rate": 3.2,
                    "open_rate": 24.8
                },
                "message": "Mockup data file not found, using fallback data"
            }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to load mockup data',
            'message': str(e)
        }, status=500)

urlpatterns = [
    path("", api_info, name="api_info"),
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/articles/", include("articles.urls")),
    path("api/playbooks/", include("playbooks.urls")),
    path("api/tools/", include("tools.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/newsletters/", include("newsletters.urls")),
    path("api/mockup-data/", mockup_data, name="mockup_data"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
