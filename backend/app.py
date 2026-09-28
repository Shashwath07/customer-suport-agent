# backend/app.py
import sys
import os
from flask import Flask
from flask_cors import CORS

# Ensure root directory is on the path for package-level imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.routes.chat_routes import chat_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
