# backend/services/chat_service.py
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from agent.response import generate_agent_reply
from memory import memory_service as ms
from data import data_service as ds

def handle_chat(customer_id: str, message: str):
    # 1. Fetch structured customer profile and ticket data
    profile = ds.get_customer(customer_id)
    tickets = ds.get_customer_tickets(customer_id)

    # 2. Fetch semantic memories from memory service
    memories = ms.get_customer_memories(customer_id, message)

    # 3. Generate response with profile and memories injected
    reply = generate_agent_reply(query=message, memories=memories, profile=profile)

    # 4. Save conversation back to memory
    ms.save_customer_conversation(customer_id, message, reply)

    return {
        "reply": reply,
        "recalled_memories": memories,
        "profile": profile,
        "tickets": tickets
    }

def get_customer_context(customer_id: str):
    """Returns profile and tickets to populate UI sidebar on load."""
    return {
        "profile": ds.get_customer(customer_id),
        "tickets": ds.get_customer_tickets(customer_id)
    }

def add_review(customer_id: str, text: str):
    ms.save_customer_memory(customer_id, text, context="Customer review")
    return {"status": "stored"}

def get_insights(customer_id: str):
    return {"insights": ms.get_customer_insights(customer_id)}
