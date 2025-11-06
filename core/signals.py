from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Telemetry
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import TelemetrySerializer

@receiver(post_save, sender=Telemetry)
def publish_telemetry(sender, instance, created, **kwargs):
    if not created:
        return
    data = TelemetrySerializer(instance).data
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "telemetry", {"type": "telemetry_event", "data": data}
    )
