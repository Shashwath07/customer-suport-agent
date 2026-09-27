from flask import Flask, jsonify, request
from flask_cors import CORS

# If your Memory Lead created a file named memory.py, import it like this:
# from memory import get_memory

app = Flask(__name__)
CORS(app)


# Temporary fallback implementation until the Memory Lead's file is plugged in:
def get_memory(customer_id: str) -> list[str]:
    # Mock data store
    sample_memories = {
        "cust_001": [
            "Sept 10: recurring task duplication, fixed by disabling auto-repeat",
            "Aug 15: reported login delay after password reset",
        ],
        "cust_002": [
            "July 04: requested upgrade to pro tier",
        ],
    }
    return sample_memories.get(customer_id, [])


@app.route("/chat", methods=["POST", "GET"])
def chat():
    # 1. Parse incoming request
    data = request.get_json(silent=True) or {}
    customer_id = data.get("customer_id")
    message = data.get("message")

    # 2. Wire in Memory Retrieval as the first step
    recalled_memories = get_memory(customer_id) if customer_id else []

    # 3. Construct response using the retrieved memories
    response = {
        "reply": f"Processing message for {customer_id}: '{message}'",
        "recalled_memories": recalled_memories,
    }

    return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)