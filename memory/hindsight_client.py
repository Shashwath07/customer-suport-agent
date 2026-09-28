"""
Hindsight Cloud client configuration.
"""
import os
from dotenv import load_dotenv

# Import SDK without colliding with current module namespace
try:
    import hindsight as _sdk
    Hindsight = _sdk.Hindsight
except (ImportError, AttributeError):
    try:
        from hindsight_sdk import Hindsight
    except ImportError:
        # Fallback to general SDK package name
        import importlib
        Hindsight = importlib.import_module("hindsight_client").Hindsight

load_dotenv()

HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "http://localhost:8888")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "mock_key")

_client = None

def get_hindsight_client():
    global _client
    if _client is not None:
        return _client

    try:
        _client = Hindsight(
            base_url=HINDSIGHT_BASE_URL,
            api_key=HINDSIGHT_API_KEY,
            timeout=30.0
        )
        return _client
    except Exception as error:
        raise RuntimeError(f"Failed to initialize Hindsight client: {error}") from error

def get_customer_bank_id(customer_id: str) -> str:
    if not isinstance(customer_id, str) or not customer_id.strip():
        raise ValueError("customer_id must be a non-empty string.")
    return f"customer-{customer_id.strip().lower()}"

def ensure_customer_bank(customer_id: str) -> str:
    client = get_hindsight_client()
    bank_id = get_customer_bank_id(customer_id)

    # If the client does not implement create_bank (e.g., in mock mode), return bank_id directly
    if not hasattr(client, "create_bank"):
        return bank_id

    try:
        client.create_bank(
            bank_id=bank_id,
            name=f"Customer Support - {customer_id}",
            background="Store and retrieve customer support history, preferences, and issues.",
            disposition={"skepticism": 3, "literalism": 3, "empathy": 4}
        )
    except Exception:
        # Bank already exists or server is mock mode; safe to proceed
        pass

    return bank_id




    
                
