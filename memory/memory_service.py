"""
Customer memory service domain interface.
"""
from typing import List, Optional
import os
import sys

# Ensure project root is available in sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from memory.hindsight_client import (
    ensure_customer_bank,
    get_hindsight_client,
)

DEFAULT_RECALL_LIMIT = 5

def get_customer_memories(
    customer_id: str,
    query: str,
    limit: int = DEFAULT_RECALL_LIMIT
) -> List[str]:
    if not customer_id or not query:
        return []

    bank_id = ensure_customer_bank(customer_id)
    client = get_hindsight_client()

    try:
        if hasattr(client, "recall"):
            result = client.recall(bank_id=bank_id, query=query.strip())
        else:
            return []

        memories = []
        for memory in getattr(result, "results", []):
            text = getattr(memory, "text", None) or (memory.get("text") if isinstance(memory, dict) else str(memory))
            if text:
                memories.append(text.strip())
            if len(memories) >= limit:
                break
        return memories
    except Exception:
        return []

def save_customer_memory(customer_id: str, memory: str, context: Optional[str] = None) -> bool:
    if not customer_id or not memory:
        return False

    bank_id = ensure_customer_bank(customer_id)
    client = get_hindsight_client()

    try:
        kwargs = {"bank_id": bank_id, "content": memory.strip()}
        if context:
            kwargs["context"] = context.strip()
        client.retain(**kwargs)
        return True
    except Exception:
        return False

def save_customer_profile(customer_id: str, profile: dict) -> bool:
    """Formats structured customer profile dictionary into natural language for memory storage."""
    if not customer_id or not isinstance(profile, dict):
        return False

    profile_lines = []
    for key, value in profile.items():
        if value is None:
            continue
        readable_key = str(key).replace("_", " ").title()
        if isinstance(value, list):
            val_str = ", ".join(str(v) for v in value)
        else:
            val_str = str(value)
        profile_lines.append(f"{readable_key}: {val_str}")

    if not profile_lines:
        return False

    memory_text = "Customer Profile:\n" + "\n".join(f"- {line}" for line in profile_lines)
    return save_customer_memory(customer_id=customer_id, memory=memory_text, context="Customer profile")

def save_customer_conversation(customer_id: str, customer_message: str, assistant_response: str) -> bool:
    conversation = f"Customer: {customer_message.strip()}\nSupport Agent: {assistant_response.strip()}"
    return save_customer_memory(customer_id, conversation, context="Customer support conversation")

def get_customer_insights(customer_id: str, prompt: str = "What problems keep recurring?") -> str:
    bank_id = ensure_customer_bank(customer_id)
    client = get_hindsight_client()
    try:
        if hasattr(client, "reflect"):
            res = client.reflect(bank_id=bank_id, query=prompt)
            return getattr(res, "text", str(res))
    except Exception:
        pass
    return "No recurring patterns detected yet."
