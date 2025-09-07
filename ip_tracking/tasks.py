from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ip_tracking.models import RequestLog, SuspiciousIP
from django.db import models

@shared_task
def detect_anomalies():
    # Define sensitive paths
    sensitive_paths = ['/admin', '/login', '/ip_tracking/login/anonymous/', '/ip_tracking/login/authenticated/']
    
    # Time window: last 1 hour
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Get IPs with request counts in the last hour
    ip_requests = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=models.Count('id')
    ).order_by('-request_count')
    
    # Check for excessive requests (>100 per hour)
    for entry in ip_requests:
        ip = entry['ip_address']
        count = entry['request_count']
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f"Excessive requests: {count} requests in the last hour"}
            )
    
    # Check for sensitive path access
    sensitive_requests = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').distinct()
    
    for entry in sensitive_requests:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults={'reason': f"Accessed sensitive path in the last hour"}
        )