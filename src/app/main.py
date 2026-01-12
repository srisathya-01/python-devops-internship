import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

app = Flask(__name__)

@app.route("/")
def home():
    env = os.getenv("ENV", "development")
    logging.info(f"Home endpoint accessed | ENV={env}")
    return jsonify(
        service="python-devops-demo",
        environment=env,
        status="running"
    ), 200

@app.route("/health")
def health():
    logging.info("Health check successful")
    return jsonify(status="UP"), 200

if __name__ == "__main__":
    logging.info("Application started")
    app.run(host="0.0.0.0", port=5000)
