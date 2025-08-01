import json
import time
import os
from app.mqtt_client import create_client

TOPIC_PUB = os.getenv("TOPIC_PUB", "sensors/performance")

def publish_sensor_data(iterations=5, interval=1.0):
    client = create_client("mqtt-publisher")
    client.loop_start()
    try:
        for _ in range(iterations):
            payload = {
                "timestamp": time.time(),
                "value": round(20 + 10 * (os.urandom(1)[0] / 255), 2)
            }
            client.publish(TOPIC_PUB, json.dumps(payload))
            print(f"[MQTT-PUBLISH] {payload}")
            time.sleep(interval)
    finally:
        client.loop_stop()
        client.disconnect()
