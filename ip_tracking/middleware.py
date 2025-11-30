from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import RequestLog, BlockedIP
from ipware import get_client_ip
import logging
from django.core.cache import cache
from ipgeolocation import IPGeolocationAPI
import logging
import os

logger = logging.getLogger(__name__)

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        self.geolocation_api = IPGeolocationAPI(api_key=os.getenv('IPGEOLOCATION_API_KEY', ''))

    def __call__(self, request):
        
        # Get client IP address
        client_ip, is_routable = get_client_ip(request)
        
        if client_ip is None:
            client_ip = '0.0.0.0'
        
        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=client_ip).exists():
            logger.warning(f"Blocked request from blacklisted IP: {client_ip}")
            return HttpResponseForbidden("Access denied - IP blocked")
        
        # Process the request
        response = self.get_response(request)
        
        # Log the request
        try:
            RequestLog.objects.create(
                ip_address=client_ip,
                path=request.path,
                timestamp=timezone.now()
            )
        except Exception as e:
            logger.error(f"Failed to log request: {e}")
        
        return response
    
 def get_geolocation_data(self, ip_address):
        """Get geolocation data with caching"""
        if ip_address in ['127.0.0.1', 'localhost']:
            return None, None
        
        cache_key = f'ip_geolocation_{ip_address}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data.get('country'), cached_data.get('city')
        
        try:
            # Using ipinfo.io as an alternative (free tier available)
            import requests
            response = requests.get(f'https://ipinfo.io/{ip_address}/json', timeout=5)
            if response.status_code == 200:
                data = response.json()
                country = data.get('country', '')
                city = data.get('city', '')
                
                # Cache for 24 hours
                cache.set(cache_key, {'country': country, 'city': city}, 86400)
                return country, city
        except Exception as e:
            logger.error(f"Geolocation failed for {ip_address}: {e}")
        
        return None, None

    def __call__(self, request):
        # Get client IP address
        client_ip, is_routable = get_client_ip(request)
        
        if client_ip is None:
            client_ip = '0.0.0.0'
        
        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=client_ip).exists():
            logger.warning(f"Blocked request from blacklisted IP: {client_ip}")
            return HttpResponseForbidden("Access denied - IP blocked")
        
        # Get geolocation data
        country, city = self.get_geolocation_data(client_ip)
        
        # Process the request
        response = self.get_response(request)
        
        # Log the request with geolocation
        try:
            RequestLog.objects.create(
                ip_address=client_ip,
                path=request.path,
                timestamp=timezone.now(),
                country=country,
                city=city
            )
        except Exception as e:
            logger.error(f"Failed to log request: {e}")
        
        return response