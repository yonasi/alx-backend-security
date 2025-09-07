from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']