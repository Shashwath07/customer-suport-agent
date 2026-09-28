# backend/services/chat_service.py
import os
import sys
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from agent.response import generate_agent_reply
from memory import memory_service as ms
from data import data_service as ds

def _extract_and_save_name(customer_id: str, message: str, profile: dict):
    """Detects if the user declared their name and persists it to memory and profile."""
    name_match = re.search(r"\b(?:my name is|i am|call me|name's)\s+([A-Z][a-z]+)", message, re.IGNORECASE)
    if name_match:
        extracted_name = name_match.group(1).capitalize()
        if not profile:
            profile = {"customer_id": customer_id, "name": extracted_name, "plan": "Standard"}
            ds.CUSTOMERS[customer_id] = profile
        else:
            profile["name"] = extracted_name

        # Store explicit identity memory in Hindsight
        ms.save_customer_memory(
            customer_id, 
            f"The customer's name is {extracted_name}.", 
            context="Customer Identity Statement"
        )
        return extracted_name, profile
    return None, profile

def handle_chat(customer_id: str, message: str):
    # 1. Fetch profile & check for name declaration
    profile = ds.get_customer(customer_id)
    new_name, profile = _extract_and_save_name(customer_id, message, profile)

    # 2. Fetch past memories from Hindsight
    memories = ms.get_customer_memories(customer_id, message)

    # 3. Generate response with profile and retrieved memories
    reply = generate_agent_reply(query=message, memories=memories, profile=profile)

    # 4. Save conversation turn to memory
    ms.save_customer_conversation(customer_id, message, reply)

    # 5. Fetch associated tickets
    tickets = ds.get_customer_tickets(customer_id)

    return {
        "reply": reply,
        "recalled_memories": memories,
        "profile": profile,
        "tickets": tickets
    }

def get_customer_context(customer_id: str):
    profile = ds.get_customer(customer_id)
    # If no local JSON profile exists, check if name was remembered in Hindsight
    if not profile:
        name_memories = ms.get_customer_memories(customer_id, "What is my name?")
        remembered_name = "Guest User"
        for m in name_memories:
            m_match = re.search(r"name is ([A-Z][a-z]+)", m, re.IGNORECASE)
            if m_match:
                remembered_name = m_match.group(1).capitalize()
                break
        profile = {"customer_id": customer_id, "name": remembered_name, "plan": "Standard"}

    return {
        "profile": profile,
        "tickets": ds.get_customer_tickets(customer_id)
    }

def add_review(customer_id: str, text: str):
    ms.save_customer_memory(customer_id, text, context="Customer review")
    return {"status": "stored"}

def get_insights(customer_id: str):
    return {"insights": ms.get_customer_insights(customer_id)}
