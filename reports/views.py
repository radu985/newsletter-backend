from django.shortcuts import render
from rest_framework import viewsets
from .models import RevenueReport
from .serializers import RevenueReportSerializer

# Create your views here.

class RevenueReportViewSet(viewsets.ModelViewSet):
    queryset = RevenueReport.objects.all()
    serializer_class = RevenueReportSerializer
