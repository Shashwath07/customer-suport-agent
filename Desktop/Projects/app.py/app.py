import asyncio
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from hindsight_client import Hindsight

app = Flask(__name__)
CORS(app)

# 1. Start a single persistent event loop in a dedicated background thread
_loop = asyncio.new_event_loop()
_thread = threading.Thread(target=_loop.run_forever, daemon=True)
_thread.start()


# Helper to dispatch coroutines safely into the running background loop
def run_coro(coro):
    future = asyncio.run_coroutine_threadsafe(coro, _loop)
    return future.result()


# 2. Initialize Hindsight inside that loop so its aiohttp session never closes
def _init_client():
    return Hindsight(base_url="http://localhost:8888")


client = run_coro(asyncio.sleep(0)) or _init_client()


@app.route("/review", methods=["POST"])
def review():
    data = request.get_json(silent=True) or {}
    cid, msg = data.get("customer_id"), data.get("message")
    if not cid or not msg:
        return jsonify(error="customer_id and message required"), 400

    run_coro(client.aretain(bank_id=cid, content=msg, context="customer review"))
    return jsonify(status="stored"), 200


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    cid, msg = data.get("customer_id"), data.get("message")
    if not cid or not msg:
        return jsonify(error="customer_id and message required"), 400

    results = run_coro(client.arecall(bank_id=cid, query=msg))
    memories = [r.text for r in results.results]

    reflection = run_coro(client.areflect(bank_id=cid, query=msg))
    reply = reflection.text

    return jsonify(reply=reply, recalled_memories=memories), 200


@app.route("/insights", methods=["GET"])
def insights():
    cid = request.args.get("customer_id")
    if not cid:
        return jsonify(error="customer_id required"), 400

    r = run_coro(
        client.areflect(bank_id=cid, query="What problems keep recurring?")
    )
    return jsonify(insights=r.text), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)