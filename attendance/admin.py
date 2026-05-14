from django.contrib import admin
from .models import AttendanceRecord, LeaveBalance

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display  = ['user', 'date', 'in_time', 'out_time', 'total_hours']
    list_filter   = ['date']
    search_fields = ['user__user_code', 'user__name']

@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display  = ['user', 'available', 'utilised']
    search_fields = ['user__user_code', 'user__name']
