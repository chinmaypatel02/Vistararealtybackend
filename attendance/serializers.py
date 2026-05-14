from rest_framework import serializers
from .models import AttendanceRecord, LeaveBalance


class AttendanceRecordSerializer(serializers.ModelSerializer):
    in_time  = serializers.SerializerMethodField()
    out_time = serializers.SerializerMethodField()
    total    = serializers.SerializerMethodField()
    day      = serializers.SerializerMethodField()

    class Meta:
        model  = AttendanceRecord
        fields = ['date', 'day', 'in_time', 'out_time', 'total']

    def _fmt_time(self, t):
        if t is None:
            return '00:00'
        return t.strftime('%H:%M')

    def _fmt_hours(self, hours):
        if not hours:
            return '00:00'
        h = int(hours)
        m = int((float(hours) - h) * 60)
        return f'{h:02d}:{m:02d}'

    def get_in_time(self, obj):
        return self._fmt_time(obj.in_time)

    def get_out_time(self, obj):
        return self._fmt_time(obj.out_time)

    def get_total(self, obj):
        return self._fmt_hours(obj.total_hours)

    def get_day(self, obj):
        return obj.date.strftime('%a')


class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = LeaveBalance
        fields = ['available', 'utilised']
