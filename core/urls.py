from rest_framework import routers
from .views import DeviceViewSet, TelemetryViewSet, AlertViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"telemetry", TelemetryViewSet)
router.register(r"alerts", AlertViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
