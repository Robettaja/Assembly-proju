from flask import Flask, request, jsonify
import subprocess
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Controls_test.race_main import start_race

import shutil
print(shutil.which("ffmpeg"))

print("Working directory at start:", os.getcwd())

app = Flask(__name__)
race_thread = None

@app.route("/start-race", methods=["POST"])
def start_race_route():
    global race_thread
    if race_thread is not None and race_thread.is_alive():
        return jsonify({"status": "Race already running"}), 400
    
    try:
        print("Starting race in background thread...")
        race_thread = threading.Thread(target=start_race)
        race_thread.start()
        return jsonify({"status": "Race started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)