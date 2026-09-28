from backend.services import hindsight_service as hs


def handle_chat(customer_id, message):
    memories = hs.recall(customer_id, message)
    reply = hs.reflect(customer_id, message)
    return {"reply": reply, "recalled_memories": memories}


def add_review(customer_id, text):
    hs.retain(customer_id, text)
    return {"status": "stored"}


def get_insights(customer_id):
    return {"insights": hs.reflect(customer_id, "What problems keep recurring?")}