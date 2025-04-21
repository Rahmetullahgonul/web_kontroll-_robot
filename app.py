from flask import Flask, request, jsonify

app = Flask(__name__)
latest_command = None

@app.route("/")
def home():
    return "Robot API Çalışıyor!"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
