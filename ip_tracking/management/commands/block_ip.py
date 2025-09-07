from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Add an IP address to the blacklist'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        try:
            # Validate and create BlockedIP entry
            BlockedIP.objects.get_or_create(ip_address=ip_address)
            self.stdout.write(self.style.SUCCESS(f'Successfully blacklisted IP: {ip_address}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error blacklisting IP {ip_address}: {str(e)}'))