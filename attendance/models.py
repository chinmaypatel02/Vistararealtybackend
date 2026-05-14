from django.db import models
from django.conf import settings


class AttendanceRecord(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    date        = models.DateField()
    in_time     = models.TimeField(null=True, blank=True)
    out_time    = models.TimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.user_code} - {self.date}'


class LeaveBalance(models.Model):
    user      = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_balance')
    available = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    utilised  = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)

    def __str__(self):
        return f'{self.user.user_code} - Leave Balance'
