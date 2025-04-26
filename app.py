# -*- coding: utf-8 -*-
from flask_cors import CORS
from flask import Flask, request

app = Flask(__name__)
CORS(app)

command = None
status_data = {"distance": None, "light": None}
vehicle_on = False  # <<< YENİ EKLENDİ

@app.route("/set-command", methods=["POST"])
def set_command():
    global command
    data = request.get_json()
    command = data.get("command")
    return {"status": "ok"}

@app.route("/get-command", methods=["GET"])
def get_command():
    global command
    cmd = command
    command = None
    return {"command": cmd}

@app.route("/set-status", methods=["POST"])
def set_status():
    global status_data
    data = request.get_json()
    status_data["distance"] = data.get("distance")
    status_data["light"] = data.get("light")
    return {"status": "ok"}

@app.route("/status", methods=["GET"])
def get_status():
    return status_data

# >>>> YENİ EKLENDİ
@app.route("/set-vehicle-status", methods=["POST"])
def set_vehicle_status():
    global vehicle_on
    data = request.get_json()
    vehicle_on = data.get("vehicle_on", False)
    return {"status": "ok", "vehicle_on": vehicle_on}

@app.route("/get-vehicle-status", methods=["GET"])
def get_vehicle_status():
    return {"vehicle_on": vehicle_on}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
