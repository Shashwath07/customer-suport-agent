# backend/services/chat_service.py
import os
import sys

# Ensure agent directory is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../agent")))
from response import generate_agent_reply
from backend.services import hindsight_service as hs

def handle_chat(customer_id, message):
    # 1. Recall relevant past context for this customer from memory
    memories = hs.recall(customer_id, message)
    
    # 2. Generate contextual response using the agent pipeline (LLM + prompts + response formatting)
    reply = generate_agent_reply(query=message, memories=memories)
    
    # 3. Store conversation interaction in memory for future context
    hs.retain(customer_id, f"Customer: {message} | Agent: {reply}")
    
    return {"reply": reply, "recalled_memories": memories}

def add_review(customer_id, text):
    hs.retain(customer_id, text)
    return {"status": "stored"}

def get_insights(customer_id):
    return {"insights": hs.reflect(customer_id, "What problems keep recurring?")}
