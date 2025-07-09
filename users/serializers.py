from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'is_premium', 'password', 'is_active', 'is_staff', 'date_joined', 'avatar')
        read_only_fields = ('id', 'is_active', 'is_staff', 'date_joined')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user 