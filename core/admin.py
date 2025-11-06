from django.contrib import admin
from .models import Device, Telemetry, Alert

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("device_id", "name", "location", "is_online", "last_seen")
    search_fields = ("device_id", "name", "location")
    list_filter = ("is_online",)
    readonly_fields = ("last_seen",)

@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "metric", "value", "ts")
    search_fields = ("device__device_id", "metric")
    list_filter = ("metric",)
    readonly_fields = ("ts", "raw")
    ordering = ("-ts",)

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "severity", "message", "ts")
    search_fields = ("device__device_id", "message")
    list_filter = ("severity",)
    readonly_fields = ("ts",)
