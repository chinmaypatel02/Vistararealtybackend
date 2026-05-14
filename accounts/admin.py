from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display   = ['email', 'user_code', 'name', 'company', 'role', 'is_active']
    search_fields  = ['email', 'user_code', 'name']
    list_filter    = ['company', 'is_active', 'is_staff']
    ordering       = ['email']
    fieldsets      = (
        (None,          {'fields': ('email', 'password')}),
        ('Personal',    {'fields': ('name', 'phone', 'avatar_url')}),
        ('Work',        {'fields': ('company', 'user_code', 'role', 'department', 'designation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets  = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'name', 'company', 'user_code', 'password1', 'password2'),
        }),
    )
