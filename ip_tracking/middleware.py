from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django_ipgeolocation.utils import get_ip_geolocation
from .models import RequestLog, BlockedIP
import logging

# Set up logging for debugging
logger = logging.getLogger(__name__)

class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        
        # Check if IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied: Your IP is blacklisted.")
        
        # Check cache for geolocation data
        cache_key = f"geolocation_{ip_address}"
        geo_data = cache.get(cache_key)
        
        if not geo_data:
            try:
                response = get_ip_geolocation(ip_address)
                geo_data = {
                    'country': response.get('country_name', '') or '',
                    'city': response.get('city', '') or ''
                }
                # Cache for 24 hours (86400 seconds)
                cache.set(cache_key, geo_data, timeout=86400)
            except Exception as e:
                logger.error(f"Geolocation API error for IP {ip_address}: {str(e)}")
                geo_data = {'country': '', 'city': ''}  # Fallback for API errors
        
        # Log the request details
        path = request.path
        try:
            RequestLog.objects.create(
                ip_address=ip_address,
                path=path,
                country=geo_data['country'],
                city=geo_data['city']
            )
        except Exception as e:
            logger.error(f"Error logging request for IP {ip_address}: {str(e)}")
        
        return None