from django.urls import path
from .views import VerifyCompanyView

urlpatterns = [
    path('verify/', VerifyCompanyView.as_view(), name='company-verify'),
]
