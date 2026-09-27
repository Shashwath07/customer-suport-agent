"""
Main Flask application for the Customer Support AI Agent.

Responsibilities:
- Start the Flask server
- Register API routes
- Serve the frontend
- Provide health-check endpoint
- Handle application-level errors
"""

from pathlib import Path

from flask import (
    Flask,
    jsonify,
    send_from_directory
)

from flask_cors import CORS
from dotenv import load_dotenv


# ============================================================
# PROJECT PATHS
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    PROJECT_ROOT / ".env"
)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__
)


# ============================================================
# CORS
# ============================================================

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*"
        }
    }
)


# ============================================================
# IMPORT API BLUEPRINT
# ============================================================

from backend.routes.chat_routes import chat_bp


# ============================================================
# REGISTER API ROUTES
# ============================================================

app.register_blueprint(
    chat_bp,
    url_prefix="/api/chat"
)


# ============================================================
# FRONTEND ROUTES
# ============================================================

@app.get("/")
def serve_frontend():
    """
    Serve the main frontend page.
    """

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.get("/style.css")
def serve_stylesheet():
    """
    Serve frontend CSS.
    """

    return send_from_directory(
        FRONTEND_DIR,
        "style.css"
    )


@app.get("/script.js")
def serve_javascript():
    """
    Serve frontend JavaScript.
    """

    return send_from_directory(
        FRONTEND_DIR,
        "script.js"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health_check():
    """
    Basic server health-check endpoint.
    """

    return jsonify({
        "success": True,
        "status": "online",
        "service": "Customer Support AI Agent"
    })


# ============================================================
# GLOBAL ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def handle_not_found(error):
    """
    Handle unknown routes.
    """

    return jsonify({
        "success": False,
        "error": "Endpoint not found."
    }), 404


@app.errorhandler(500)
def handle_server_error(error):
    """
    Handle unexpected server errors.
    """

    return jsonify({
        "success": False,
        "error": "Internal server error."
    }), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
