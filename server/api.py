# server/api.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/keystrokes', methods=['POST'])
def receive_keystrokes():
    data = request.json
    # TODO: Validate and store data
    return jsonify({"status": "success"}), 201

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    # TODO: Fetch alerts from DB
    return jsonify([])

if __name__ == "__main__":
    app.run(port=5001)
