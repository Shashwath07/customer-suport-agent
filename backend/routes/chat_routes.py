# backend/routes/chat_routes.py
from flask import Blueprint, jsonify, request
from backend.services import chat_service

chat_bp = Blueprint("chat", __name__)

def _payload():
    data = request.get_json(silent=True) or {}
    return data.get("customer_id"), data.get("message")

@chat_bp.route("/chat", methods=["POST"])
def chat():
    cid, msg = _payload()
    if not cid or not msg:
        return jsonify(error="customer_id and message required"), 400
    return jsonify(chat_service.handle_chat(cid, msg)), 200

@chat_bp.route("/review", methods=["POST"])
def review():
    cid, msg = _payload()
    if not cid or not msg:
        return jsonify(error="customer_id and message required"), 400
    return jsonify(chat_service.add_review(cid, msg)), 200

@chat_bp.route("/insights", methods=["GET"])
def insights():
    cid = request.args.get("customer_id")
    if not cid:
        return jsonify(error="customer_id required"), 400
    return jsonify(chat_service.get_insights(cid)), 200
