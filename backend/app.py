# backend/app.py
import sys
import os
from flask import Flask, send_from_directory
from flask_cors import CORS

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

from backend.routes.chat_routes import chat_bp

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

app.register_blueprint(chat_bp)

# Serve index.html and assets directly
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0", use_reloader=False)
