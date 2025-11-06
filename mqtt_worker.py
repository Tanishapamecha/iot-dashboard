import os
import django
import json
import logging
import paho.mqtt.client as mqtt
from django.utils import timezone

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iotdash.settings")
django.setup()

from core.models import Device, Telemetry, Alert

# ---------------- MQTT Worker Configuration ----------------
logger = logging.getLogger("mqtt")
logger.setLevel(logging.INFO)

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC_TEL = "iot/+/telemetry"
TOPIC_STA = "iot/+/status"


# ---------------- MQTT Callbacks ----------------
def on_connect(client, userdata, flags, rc):
    logger.info("Connected to MQTT broker with result code %s", rc)
    client.subscribe(TOPIC_TEL)
    client.subscribe(TOPIC_STA)


def on_message(client, userdata, msg):
    try:
        topic = msg.topic.split('/')
        _, device_id, kind = topic[0], topic[1], topic[2]
    except Exception:
        logger.exception("Bad topic: %s", msg.topic)
        return

    # Decode payload
    raw = msg.payload.decode().strip()
    payload = {}

    try:
        # Try to load as JSON first
        payload = json.loads(raw or "{}")
    except Exception:
        # If it's plain text like 'online' or 'offline'
        if raw.lower() in ["online", "offline"]:
            payload = {"online": raw.lower() == "online"}
        else:
            print(f"⚠️ Unknown payload format: {raw}")
            return

    # ---------------- Process Message ----------------
    dev, _ = Device.objects.get_or_create(device_id=device_id)
    dev.last_seen = timezone.now()

    # Device status update
    if kind == "status":
        dev.is_online = payload.get("online", True)
        dev.save()
        return

    # Telemetry data ingestion
    if isinstance(payload, dict):
        for k, v in payload.items():
            try:
                value = float(v)
            except Exception:
                continue  # skip non-numeric metrics
            Telemetry.objects.create(
                device=dev,
                metric=k,
                value=value,
                raw=payload
            )
    dev.is_online = True
    dev.save()


# ---------------- Run the Worker ----------------
if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    logger.info(f" MQTT worker connected to {BROKER}:{PORT}")
    client.loop_forever()
