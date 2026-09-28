# backend/services/chat_service.py
import os
import sys

# Add project root to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from agent.response import generate_agent_reply
from memory import memory_service as ms

def handle_chat(customer_id: str, message: str):
    # 1. Fetch relevant long-term memories via memory domain
    memories = ms.get_customer_memories(customer_id, message)

    # 2. Generate grounded response using agent pipeline (prompts + Groq LLM + formatting)
    reply = generate_agent_reply(query=message, memories=memories)

    # 3. Persist conversation turn back into memory
    ms.save_customer_conversation(customer_id, message, reply)

    return {"reply": reply, "recalled_memories": memories}

def add_review(customer_id: str, text: str):
    ms.save_customer_memory(customer_id, text, context="Customer review")
    return {"status": "stored"}

def get_insights(customer_id: str):
    return {"insights": ms.get_customer_insights(customer_id)}
