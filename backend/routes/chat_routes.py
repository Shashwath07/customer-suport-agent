"""
Chat API routes.

This module receives requests from the frontend and passes them
to the backend service layer.
"""

from flask import (
    Blueprint,
    jsonify,
    request
)

from backend.services.chat_service import (
    process_chat
)


# ============================================================
# BLUEPRINT
# ============================================================

chat_bp = Blueprint(
    "chat",
    __name__
)


# ============================================================
# POST /api/chat
# ============================================================

@chat_bp.post("")
def chat():
    """
    Process a customer-support message.

    Expected JSON:

    {
        "customer_id": "CUST001",
        "message": "My payment failed again"
    }
    """

    # --------------------------------------------------------
    # Read JSON body
    # --------------------------------------------------------

    data = request.get_json(
        silent=True
    )


    if not isinstance(data, dict):

        return jsonify({
            "success": False,
            "customer_id": "",
            "response": "",
            "used_memory": [],
            "error": "Request body must contain valid JSON."
        }), 400


    # --------------------------------------------------------
    # Extract values
    # --------------------------------------------------------

    customer_id = data.get(
        "customer_id"
    )

    message = data.get(
        "message"
    )


    # --------------------------------------------------------
    # Validate customer ID
    # --------------------------------------------------------

    if not isinstance(
        customer_id,
        str
    ):

        return jsonify({
            "success": False,
            "customer_id": "",
            "response": "",
            "used_memory": [],
            "error": "customer_id must be a string."
        }), 400


    customer_id = (
        customer_id
        .strip()
        .upper()
    )


    if not customer_id:

        return jsonify({
            "success": False,
            "customer_id": "",
            "response": "",
            "used_memory": [],
            "error": "customer_id is required."
        }), 400


    # --------------------------------------------------------
    # Validate message
    # --------------------------------------------------------

    if not isinstance(
        message,
        str
    ):

        return jsonify({
            "success": False,
            "customer_id": customer_id,
            "response": "",
            "used_memory": [],
            "error": "message must be a string."
        }), 400


    message = message.strip()


    if not message:

        return jsonify({
            "success": False,
            "customer_id": customer_id,
            "response": "",
            "used_memory": [],
            "error": "message cannot be empty."
        }), 400


    # Prevent unnecessarily large requests.
    if len(message) > 2000:

        return jsonify({
            "success": False,
            "customer_id": customer_id,
            "response": "",
            "used_memory": [],
            "error": "Message is too long. Maximum length is 2000 characters."
        }), 400


    # --------------------------------------------------------
    # Process request
    # --------------------------------------------------------

    try:

        result = process_chat(
            customer_id=customer_id,
            message=message
        )


        return jsonify(
            result
        ), 200


    except ValueError as error:

        return jsonify({
            "success": False,
            "customer_id": customer_id,
            "response": "",
            "used_memory": [],
            "error": str(error)
        }), 400


    except Exception as error:

        print(
            f"[CHAT ERROR] {error}"
        )


        return jsonify({
            "success": False,
            "customer_id": customer_id,
            "response": "",
            "used_memory": [],
            "error": "Unable to process the customer request."
        }), 500
