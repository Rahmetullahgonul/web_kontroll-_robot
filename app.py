from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_command = None
latest_status = {
    "distance": None,
    "light": None
}

@app.route("/")
def home():
    return "Robot API çalışıyor!"

@app.route("/set-command", methods=["POST"])
def set_command():
    global latest_command
    data = request.get_json()
    latest_command = data.get("command")
    return jsonify({"status": "OK", "command": latest_command})

@app.route("/get-command", methods=["GET"])
def get_command():
    global latest_command
    cmd = latest_command
    latest_command = None  # komut alındıktan sonra sıfırla
    return jsonify({"command": cmd})

@app.route("/set-status", methods=["POST"])
def set_status():
    global latest_status
    data = request.get_json()
    latest_status["distance"] = data.get("distance")
    latest_status["light"] = data.get("light")
    return jsonify({"status": "OK", "data": latest_status})

@app.route("/status", methods=["GET"])
def get_status():
    return jsonify(latest_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
