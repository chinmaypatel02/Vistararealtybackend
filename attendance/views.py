from datetime import date, timedelta
from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import AttendanceRecord, LeaveBalance
from .serializers import AttendanceRecordSerializer


def _fmt_hours(hours):
    if not hours:
        return '00:00'
    h = int(hours)
    m = int((float(hours) - h) * 60)
    return f'{h:02d}:{m:02d}'


def _get_week_range(today):
    """Returns Monday to Saturday of the current week."""
    monday = today - timedelta(days=today.weekday())  # weekday(): Mon=0
    return [monday + timedelta(days=i) for i in range(6)]  # Mon–Sat


class DashboardView(APIView):
    """
    GET /api/attendance/dashboard/
    Returns all data needed for the home screen.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user  = request.user
        today = date.today()

        # ── User info ──────────────────────────────────────────────
        user_data = {
            'name':         user.name,
            'designation':  user.designation,
            'role':         user.role,
            'user_code':    user.user_code,
            'department':   user.department,
            'organisation': user.company.name if user.company else '',
            'avatar_url':   user.avatar_url,
        }

        # ── Today's attendance ─────────────────────────────────────
        try:
            today_record = AttendanceRecord.objects.get(user=user, date=today)
            work_today   = _fmt_hours(today_record.total_hours)
        except AttendanceRecord.DoesNotExist:
            work_today = '00:00'

        # ── Weekly stats ───────────────────────────────────────────
        week_dates   = _get_week_range(today)
        week_records = AttendanceRecord.objects.filter(user=user, date__in=week_dates)
        total_week   = sum(r.total_hours for r in week_records) or Decimal('0.00')
        worked_this_week = _fmt_hours(total_week)

        # ── Leave balance ──────────────────────────────────────────
        try:
            lb = LeaveBalance.objects.get(user=user)
            leaves_available = float(lb.available)
            leaves_utilised  = float(lb.utilised)
        except LeaveBalance.DoesNotExist:
            leaves_available = 0.0
            leaves_utilised  = 0.0

        # ── Weekly attendance table ────────────────────────────────
        record_map = {r.date: r for r in week_records}
        weekly_attendance = []
        for d in week_dates:
            if d in record_map:
                rec = record_map[d]
                weekly_attendance.append({
                    'date':     d.strftime('%d %b'),
                    'day':      d.strftime('%a'),
                    'in_time':  rec.in_time.strftime('%H:%M') if rec.in_time else '00:00',
                    'out_time': rec.out_time.strftime('%H:%M') if rec.out_time else '00:00',
                    'total':    _fmt_hours(rec.total_hours),
                })
            else:
                weekly_attendance.append({
                    'date':     d.strftime('%d %b'),
                    'day':      d.strftime('%a'),
                    'in_time':  '00:00',
                    'out_time': '00:00',
                    'total':    '00:00',
                })

        return Response({
            'user': user_data,
            'stats': {
                'work_today':        work_today,
                'worked_this_week':  worked_this_week,
                'leaves_available':  leaves_available,
                'leaves_utilised':   leaves_utilised,
            },
            'weekly_attendance': weekly_attendance,
        })
