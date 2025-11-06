from django.db import models

class Device(models.Model):
    device_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=120, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.device_id} ({'online' if self.is_online else 'offline'})"

class Telemetry(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="telemetry")
    ts = models.DateTimeField(auto_now_add=True)
    metric = models.CharField(max_length=40)
    value = models.FloatField()
    raw = models.JSONField(default=dict)

    class Meta:
        ordering = ["-ts"]

class Alert(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="alerts")
    ts = models.DateTimeField(auto_now_add=True)
    severity = models.CharField(max_length=10, choices=(("info","info"),("warn","warn"),("crit","crit")))
    message = models.CharField(max_length=300)
