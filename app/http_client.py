import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "config", "settings.env"))
SERVER_URL = os.getenv("HTTP_SERVER_URL", "http://127.0.0.1:5000/data")

def send_sensor_data(iterations=5, interval=1.0):
    for _ in range(iterations):
        payload = {
            "timestamp": time.time(),
            "value": round(20 + 10 * (os.urandom(1)[0] / 255), 2)
        }
        start = time.time()
        r = requests.post(SERVER_URL, json=payload)
        latency = (time.time() - start) * 1000
        print(f"[HTTP-POST] Sent {payload} | Latency: {latency:.2f} ms")
        time.sleep(interval)
