"""
Customer memory service domain interface.
"""
from typing import List, Optional
import os
import sys

# Ensure memory folder is in sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from hindsight_client import (
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
        # Standard SDK recall
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
