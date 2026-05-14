from django.db import models


class Company(models.Model):
    code        = models.CharField(max_length=20, unique=True)
    name        = models.CharField(max_length=200)
    address     = models.TextField(blank=True)
    phone       = models.CharField(max_length=20, blank=True)
    email       = models.EmailField(blank=True)
    logo_url    = models.URLField(blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return f'{self.code} — {self.name}'
