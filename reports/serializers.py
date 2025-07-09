from rest_framework import serializers
from .models import RevenueReport

class RevenueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueReport
        fields = '__all__' 