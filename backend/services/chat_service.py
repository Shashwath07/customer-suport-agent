# backend/services/chat_service.py
import sys
import os

# Ensure the agent directory is accessible for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../agent")))

from response import generate_agent_reply
from backend.services import hindsight_service as hs


def handle_chat(customer_id, message):
    # 1. Fetch relevant past interactions from memory
    memories = hs.recall(customer_id, message)

    # 2. Invoke the agent pipeline (prompts -> llm -> response format)
    reply = generate_agent_reply(query=message, memories=memories)

    # 3. Store conversation turn to memory for future recall
    hs.retain(customer_id, f"Customer: {message} | Agent: {reply}")

    return {"reply": reply, "recalled_memories": memories}


def add_review(customer_id, text):
    hs.retain(customer_id, text)
    return {"status": "stored"}


def get_insights(customer_id):
    return {"insights": hs.reflect(customer_id, "What problems keep recurring?")}
