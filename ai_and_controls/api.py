from flask import Flask, request, jsonify

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Controls_test.race_main import start_race


app = Flask(__name__)

@app.route("/start-race", methods=["POST"])
def start_race_route():
    try:
        print("Starting race...")
        start_race()
        # tähän kutsutaan funktio
        
        return jsonify({"status": "Race started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)