import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# these get set when the docker image is built in the CD pipeline
APP_VERSION = os.getenv("APP_VERSION", "dev")
GIT_COMMIT = os.getenv("GIT_COMMIT", "unknown")

MODEL_VERSION = "model-6"


@app.route("/")
def home():
    return jsonify({
        "service": "mlops-demo",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "application_version": APP_VERSION,
        "model_version": MODEL_VERSION,
        "git_commit": GIT_COMMIT,
        "status": "healthy"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    value = float(data["value"])

    # Dummy ML prediction for teaching
    prediction = value * 2

    return jsonify({
        "input": value,
        "prediction": prediction,
        "model_version": MODEL_VERSION
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
