from django.shortcuts import render
from rest_framework import viewsets
from .models import Playbook
from .serializers import PlaybookSerializer

# Create your views here.

class PlaybookViewSet(viewsets.ModelViewSet):
    queryset = Playbook.objects.all()
    serializer_class = PlaybookSerializer
