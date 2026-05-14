from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display  = ['code', 'name', 'is_active', 'created_at']
    search_fields = ['code', 'name']
    list_filter   = ['is_active']
