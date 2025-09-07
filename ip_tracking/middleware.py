from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog

class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        path = request.path
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path
        )
        return None