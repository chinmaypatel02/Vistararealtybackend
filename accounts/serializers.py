from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    company_code = serializers.CharField(max_length=20)
    user_code    = serializers.CharField(max_length=20)
    password     = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    company_code = serializers.CharField(source='company.code', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model  = User
        fields = [
            'id', 'user_code', 'name', 'email', 'phone',
            'role', 'department', 'designation', 'avatar_url',
            'company_code', 'company_name',
        ]
