from rest_framework import serializers
from .models import Playbook

class PlaybookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playbook
        fields = '__all__' 