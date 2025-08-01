import os
import logging
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.env'))
BROKER_URL = os.getenv("BROKER_URL")
BROKER_PORT = int(os.getenv("BROKER_PORT", "1883"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_client(client_id: str) -> mqtt.Client:
    client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(BROKER_URL, BROKER_PORT)
    return client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker.")
    else:
        logger.error(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    logger.info("Disconnected from MQTT broker (rc=%s)", rc)
