from rest_framework import serializers
from .models import Device, Telemetry, Alert

class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetry
        fields = ["id", "device", "metric", "value", "ts", "raw"]

class DeviceSerializer(serializers.ModelSerializer):
    latest = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ["id", "device_id", "name", "location", "last_seen", "is_online", "latest"]

    def get_latest(self, obj):
        latest = obj.telemetry.first()
        if not latest:
            return None
        return TelemetrySerializer(latest).data

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"
