"""
URL configuration for email_api app
"""
from django.urls import path
from .views import ServiceInfoView, HealthCheckView, SendEmailView

app_name = 'email_api'

urlpatterns = [
    # Root endpoint
    path('', ServiceInfoView.as_view(), name='service-info'),
    
    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # Email endpoints
    path('v1/send-email/', SendEmailView.as_view(), name='send-email'),
]



