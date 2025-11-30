from django.contrib import admin
from .models import RequestLog, BlockedIP, SuspiciousIP

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'path', 'timestamp', 'country', 'city']
    list_filter = ['timestamp', 'country', 'path']
    search_fields = ['ip_address', 'path']
    readonly_fields = ['timestamp']

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'created_at', 'reason']
    search_fields = ['ip_address']

@admin.register(SuspiciousIP)
class SuspiciousIPAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'reason', 'detected_at', 'is_active']
    list_filter = ['is_active', 'detected_at']
    search_fields = ['ip_address']