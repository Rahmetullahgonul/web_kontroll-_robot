# -*- coding: utf-8 -*-
from flask_cors import CORS
from flask import Flask, request
from gtts import gTTS
import pygame
import io
import threading

app = Flask(__name__)
CORS(app)

command = None
status_data = {"distance": None, "light": None}
vehicle_on = False

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

@app.route("/set-vehicle-status", methods=["POST"])
def set_vehicle_status():
    global vehicle_on
    data = request.get_json()
    vehicle_on = data.get("vehicle_on", False)
    return {"status": "ok", "vehicle_on": vehicle_on}

@app.route("/get-vehicle-status", methods=["GET"])
def get_vehicle_status():
    return {"vehicle_on": vehicle_on}

# >>> Text-to-Speech için yeni eklenen endpoint
@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return {"status": "error", "message": "Empty text"}

    threading.Thread(target=play_text_to_speech, args=(text,)).start()
    return {"status": "ok"}

def play_text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='tr')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        pygame.mixer.init()
        pygame.mixer.music.load(mp3_fp, 'mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue

    except Exception as e:
        print("Text-to-Speech error:", e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
