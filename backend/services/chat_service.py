"""
Core customer-support orchestration service.

This is the bridge between:

Frontend
   ↓
Backend API
   ↓
Memory
   ↓
AI Agent
   ↓
Memory update
   ↓
Backend
   ↓
Frontend

This module coordinates the different parts of the system.
"""

import json
from pathlib import Path
from typing import Dict, Any


from memory.memory_service import (
    get_customer_memories,
    save_customer_conversation
)

from agent.response import (
    generate_response
)


# ============================================================
# PROJECT PATHS
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parents[1]

PROJECT_ROOT = BACKEND_DIR.parent

CUSTOMERS_FILE = (
    PROJECT_ROOT
    / "data"
    / "customers.json"
)


# ============================================================
# CUSTOMER DATA
# ============================================================

def load_customers() -> list:
    """
    Load synthetic customer data from customers.json.
    """

    if not CUSTOMERS_FILE.exists():

        raise RuntimeError(
            "customers.json was not found."
        )


    try:

        with open(
            CUSTOMERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )


    except json.JSONDecodeError as error:

        raise RuntimeError(
            f"customers.json contains invalid JSON: {error}"
        ) from error


    if not isinstance(
        data,
        list
    ):

        raise RuntimeError(
            "customers.json must contain a list of customers."
        )


    return data


# ============================================================
# FIND CUSTOMER
# ============================================================

def get_customer(
    customer_id: str
) -> Dict[str, Any]:
    """
    Find a customer using the customer ID.

    Returns:
        Customer dictionary.
    """

    customer_id = (
        customer_id
        .strip()
        .upper()
    )


    customers = load_customers()


    for customer in customers:

        stored_id = str(
            customer.get(
                "customer_id",
                ""
            )
        ).strip().upper()


        if stored_id == customer_id:

            return customer


    raise ValueError(
        f"Customer '{customer_id}' was not found."
    )


# ============================================================
# MAIN CHAT PIPELINE
# ============================================================

def process_chat(
    customer_id: str,
    message: str
) -> Dict[str, Any]:
    """
    Execute the complete customer-support pipeline.

    Pipeline:

    1. Validate customer.
    2. Retrieve relevant memories.
    3. Send query + memories to AI Agent.
    4. Generate response.
    5. Store conversation as memory.
    6. Return response to frontend.
    """

    # --------------------------------------------------------
    # Step 1: Validate customer
    # --------------------------------------------------------

    customer = get_customer(
        customer_id
    )


    # --------------------------------------------------------
    # Step 2: Retrieve customer memory
    # --------------------------------------------------------

    memories = get_customer_memories(
        customer_id=customer_id,
        query=message,
        limit=5
    )


    # --------------------------------------------------------
    # Step 3: Generate AI response
    # --------------------------------------------------------

    ai_response = generate_response(
        customer_query=message,
        customer_memories=memories
    )


    # --------------------------------------------------------
    # Step 4: Save conversation
    # --------------------------------------------------------

    memory_saved = False


    try:

        memory_saved = save_customer_conversation(
            customer_id=customer_id,
            customer_message=message,
            assistant_response=ai_response
        )


    except Exception as error:

        # The customer should still receive the response even
        # if saving the new memory fails.

        print(
            f"[MEMORY SAVE WARNING] {error}"
        )


    # --------------------------------------------------------
    # Step 5: Return unified response
    # --------------------------------------------------------

    return {
        "success": True,

        "customer_id": customer_id,

        "response": ai_response,

        "used_memory": memories,

        "customer_name": customer.get(
            "name",
            ""
        ),

        "memory_saved": memory_saved
    }
