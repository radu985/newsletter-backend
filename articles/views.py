from django.shortcuts import render
from rest_framework import viewsets
from .models import Topic, Article
from .serializers import TopicSerializer, ArticleSerializer

# Create your views here.

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
