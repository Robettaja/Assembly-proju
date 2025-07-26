from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/start-race", methods=["POST"])
def start_race():
    print("Starting race...")

    # tähän kutsutaan funktio
    return jsonify({"status": "Race started"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)