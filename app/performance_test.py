import time
import json
import os
import requests
import threading
from app.mqtt_client import create_client
import matplotlib.pyplot as plt


# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "config", "settings.env"))

TOPIC_PUB = os.getenv("TOPIC_PUB", "sensors/performance")
TOPIC_SUB = os.getenv("TOPIC_SUB", "sensors/performance")
SERVER_URL = os.getenv("HTTP_SERVER_URL", "http://127.0.0.1:5000/data")

mqtt_results = []

def on_mqtt_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    end_time = time.time()
    latency = (end_time - data["timestamp"]) * 1000
    mqtt_results.append(latency)
    print(f"[MQTT] Received {data} | Latency: {latency:.2f} ms")

def test_mqtt(iterations=5):
    client = create_client("mqtt-perf-tester")
    client.on_message = on_mqtt_message
    client.subscribe(TOPIC_SUB)
    client.loop_start()

    for _ in range(iterations):
        payload = {
            "timestamp": time.time(),
            "value": round(20 + 10 * (os.urandom(1)[0] / 255), 2)
        }
        client.publish(TOPIC_PUB, json.dumps(payload))
        print(f"[MQTT] Sent {payload}")
        time.sleep(1)

    time.sleep(2)  # wait for last messages
    client.loop_stop()
    client.disconnect()
    return mqtt_results

def test_http(iterations=5):
    http_results = []
    for _ in range(iterations):
        payload = {
            "timestamp": time.time(),
            "value": round(20 + 10 * (os.urandom(1)[0] / 255), 2)
        }
        start = time.time()
        r = requests.post(SERVER_URL, json=payload)
        end = time.time()
        latency = (end - start) * 1000
        http_results.append(latency)
        print(f"[HTTP] Sent {payload} | Latency: {latency:.2f} ms")
        time.sleep(1)
    return http_results

def run_comparison(iterations=50):
    print("\n=== Running MQTT Test ===")
    mqtt_latencies = test_mqtt(iterations)

    print("\n=== Running HTTP Test ===")
    http_latencies = test_http(iterations)

    print("\n=== Results ===")
    print(f"MQTT Avg Latency: {sum(mqtt_latencies)/len(mqtt_latencies):.2f} ms")
    print(f"HTTP Avg Latency: {sum(http_latencies)/len(http_latencies):.2f} ms")


    # 📊 Plot Graph
    plt.figure(figsize=(8, 5))
    plt.plot(mqtt_latencies, label="MQTT Latency (ms)", marker="o")
    plt.plot(http_latencies, label="HTTP Latency (ms)", marker="x")
    plt.title("MQTT vs HTTP Latency Comparison")
    plt.xlabel("Message #")
    plt.ylabel("Latency (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
