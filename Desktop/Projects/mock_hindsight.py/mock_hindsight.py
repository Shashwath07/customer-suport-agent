from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB = {}


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def catch_all(path):
  data = request.get_json(silent=True) or {}
  content = data.get("content") or data.get("text") or data.get("message")
  if content:
    DB.setdefault("cust1", []).append(content)

  return (
      jsonify({
          "success": True,
          "bank_id": "cust1",
          "items_count": 1,
          "async": False,
          "operation_id": "op_mock_001",
          "results": [{
              "id": "mem_001",
              "text": (
                  "Sept 10: recurring task duplicated, fixed by disabling"
                  " auto-repeat"
              ),
              "type": "observation",
              "entities": [],
              "context": "customer review",
          }],
          "text": (
              "Sept 10: recurring task duplicated, fixed by disabling"
              " auto-repeat"
          ),
          "memories": [
              (
                  "Sept 10: recurring task duplicated, fixed by disabling"
                  " auto-repeat"
              )
          ],
          "entities": {},
      }),
      200,
  )


if __name__ == "__main__":
  app.run(port=8888, debug=True)