"""
Hindsight Cloud client configuration.

This module creates and manages the single Hindsight client used
by the Customer Support AI Agent.

Hindsight is used for:
- Storing customer memories
- Recalling relevant customer memories
"""

import os

from dotenv import load_dotenv
from hindsight_client import Hindsight


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# HINDSIGHT CONFIGURATION
# ============================================================

HINDSIGHT_BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

HINDSIGHT_API_KEY = os.getenv(
    "HINDSIGHT_API_KEY"
)


# ============================================================
# CLIENT
# ============================================================

_client = None


def get_hindsight_client() -> Hindsight:
    """
    Return the shared Hindsight client.

    A single client instance is reused throughout the application
    instead of creating a new client for every request.
    """

    global _client

    if _client is not None:
        return _client

    if not HINDSIGHT_API_KEY:
        raise RuntimeError(
            "HINDSIGHT_API_KEY is not configured. "
            "Add your Hindsight API key to the .env file."
        )

    try:

        _client = Hindsight(
            base_url=HINDSIGHT_BASE_URL,
            api_key=HINDSIGHT_API_KEY,
            timeout=30.0
        )

        return _client

    except Exception as error:

        raise RuntimeError(
            f"Failed to initialize Hindsight client: {error}"
        ) from error


def get_customer_bank_id(customer_id: str) -> str:
    """
    Convert a customer ID into the Hindsight memory-bank ID.

    Each customer gets an isolated memory bank.

    Example:
        CUST001
        ->
        customer-cust001
    """

    if not isinstance(customer_id, str):
        raise TypeError(
            "customer_id must be a string."
        )

    customer_id = customer_id.strip().lower()

    if not customer_id:
        raise ValueError(
            "customer_id cannot be empty."
        )

    return f"customer-{customer_id}"


def ensure_customer_bank(customer_id: str):
    """
    Create/configure the Hindsight memory bank for a customer.

    Hindsight memory banks provide isolation between customers,
    so memories for one customer are not mixed with another.
    """

    client = get_hindsight_client()

    bank_id = get_customer_bank_id(
        customer_id
    )

    try:

        client.create_bank(
            bank_id=bank_id,
            name=f"Customer Support - {customer_id}",
            mission=(
                "Store and retrieve useful customer-specific "
                "information, support history, preferences, "
                "issues, actions, and relevant conversation context."
            ),
            disposition={
                "skepticism": 3,
                "literalism": 3,
                "empathy": 4
            }
        )

        return bank_id

    except Exception as error:

        raise RuntimeError(
            f"Failed to initialize memory bank "
            f"for customer {customer_id}: {error}"
        ) from error
