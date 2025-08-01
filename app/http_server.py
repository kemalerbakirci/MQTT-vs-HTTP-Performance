from flask import Flask, request, jsonify
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)

@app.route("/data", methods=["POST"])
def receive_data():
    """Receive JSON sensor data via HTTP POST."""
    data = request.json
    if not data:
        logging.warning("Received empty or invalid request.")
        return jsonify({"status": "error", "message": "No JSON data"}), 400

    logging.info(f"[HTTP-SERVER] Received: {data}")
    return jsonify({"status": "ok", "received_at": time.time()}), 200

if __name__ == "__main__":
    # Change port to avoid conflicts (use 5050 instead of 5000)
    app.run(host="0.0.0.0", port=5050, debug=True)
