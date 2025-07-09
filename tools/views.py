from django.shortcuts import render
from rest_framework import viewsets
from .models import Tool
from .serializers import ToolSerializer

# Create your views here.

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
