# tools/publisher.py
import json, time, random, os, argparse
import paho.mqtt.publish as publish
import socket

parser = argparse.ArgumentParser()
parser.add_argument("--broker", default=os.getenv("MQTT_BROKER", "localhost"))
parser.add_argument("--port", type=int, default=int(os.getenv("MQTT_PORT", 1883)))
parser.add_argument("--device", default=os.getenv("DEVICE_ID", "dev001"))
parser.add_argument("--interval", type=float, default=5.0)
args = parser.parse_args()

BROKER = args.broker
PORT = args.port
DEV = args.device
TOPIC = f"iot/{DEV}/telemetry"

def can_connect(host, port, timeout=3):
    try:
        sock = socket.create_connection((host, port), timeout)
        sock.close()
        return True
    except Exception:
        return False

print(f"Publishing to broker={BROKER}:{PORT} topic={TOPIC}")

if not can_connect(BROKER, PORT):
    print(f"ERROR: cannot reach {BROKER}:{PORT}. Try using test.mosquitto.org or run a local broker.")
    print("Tip: In PowerShell: $env:MQTT_BROKER='test.mosquitto.org' ; python tools\\publisher.py")
    raise SystemExit(1)

while True:
    payload = {
        "temperature": round(24 + random.random() * 10, 2),
        "humidity": round(45 + random.random() * 20, 2),
        "battery": round(70 + random.random() * 30, 2)
    }
    try:
        publish.single(TOPIC, payload=json.dumps(payload), hostname=BROKER, port=PORT)
        print("Published:", payload)
    except Exception as e:
        print("Publish error:", e)
    time.sleep(args.interval)
