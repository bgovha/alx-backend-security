from django.db import models
from django.utils import timezone

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['path']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    reason = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Blocked IP"
        verbose_name_plural = "Blocked IPs"

    def __str__(self):
        return self.ip_address

class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField()
    detected_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Suspicious IP"
        verbose_name_plural = "Suspicious IPs"

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"