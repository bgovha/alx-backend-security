from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    """
    Celery task to detect suspicious IP activity
    Runs hourly to flag IPs with abnormal behavior
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Detect IPs with excessive requests (>100 per hour)
    high_volume_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=Count('id')
    ).filter(
        request_count__gt=100
    )
    
    for ip_data in high_volume_ips:
        ip_address = ip_data['ip_address']
        count = ip_data['request_count']
        
        SuspiciousIP.objects.update_or_create(
            ip_address=ip_address,
            defaults={
                'reason': f'High request volume: {count} requests in 1 hour',
                'is_active': True
            }
        )
        print(f"Flagged IP {ip_address} for high volume: {count} requests")
    
    # Detect access to sensitive paths
    sensitive_paths = ['/admin/', '/login/', '/api/auth/', '/dashboard/']
    
    for path in sensitive_paths:
        suspicious_access = RequestLog.objects.filter(
            timestamp__gte=one_hour_ago,
            path__startswith=path
        ).values('ip_address').annotate(
            access_count=Count('id')
        ).filter(
            access_count__gt=10  # More than 10 accesses to sensitive paths
        )
        
        for access_data in suspicious_access:
            ip_address = access_data['ip_address']
            count = access_data['access_count']
            
            SuspiciousIP.objects.update_or_create(
                ip_address=ip_address,
                defaults={
                    'reason': f'Excessive access to sensitive path {path}: {count} accesses in 1 hour',
                    'is_active': True
                }
            )
            print(f"Flagged IP {ip_address} for suspicious path access: {path}")
    
    return f"Anomaly detection completed. Found {len(high_volume_ips)} high-volume IPs."

@shared_task
def cleanup_old_logs():
    """Clean up logs older than 30 days for privacy compliance"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    deleted_count, _ = RequestLog.objects.filter(
        timestamp__lt=thirty_days_ago
    ).delete()
    
    print(f"Cleaned up {deleted_count} old log entries")
    return f"Cleaned up {deleted_count} old log entries"