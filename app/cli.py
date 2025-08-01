from app.mqtt_publisher import publish_sensor_data
from app.http_client import send_sensor_data
from app.performance_test import run_comparison

MENU = """
==== MQTT vs HTTP Performance ====
1) Test MQTT Publisher
2) Test HTTP Client
3) Run MQTT vs HTTP Comparison
4) Exit
Choose an option: """

def main():
    while True:
        choice = input(MENU).strip()
        if choice == "1":
            publish_sensor_data()
        elif choice == "2":
            send_sensor_data()
        elif choice == "3":
            run_comparison()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option, try again.")
