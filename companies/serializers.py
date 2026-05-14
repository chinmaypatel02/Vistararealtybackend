from rest_framework import serializers
from .models import Company


class CompanyVerifySerializer(serializers.Serializer):
    company_code = serializers.CharField(max_length=20)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Company
        fields = ['code', 'name', 'logo_url']
