from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Device, Telemetry, Alert
from .serializers import DeviceSerializer, TelemetrySerializer, AlertSerializer
from django.shortcuts import get_object_or_404

class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = "device_id"
    lookup_value_regex = "[^/]+"

    @action(detail=True, methods=["get"])
    def telemetry(self, request, device_id=None):
        device = get_object_or_404(Device, device_id=device_id)
        metric = request.query_params.get("metric")
        limit = int(request.query_params.get("limit", 100))
        qs = device.telemetry.all()
        if metric:
            qs = qs.filter(metric=metric)
        serializer = TelemetrySerializer(qs[:limit], many=True)
        return Response(serializer.data)

class TelemetryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
