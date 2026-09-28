SYSTEM_PROMPT = """You are a customer support agent.

Rules:
- Be professional, clear, friendly and concise (under 150 words).
- Use the customer's history only when it is relevant to the current question.
- Build on earlier answers instead of repeating them. Do not ask the customer to
  repeat information already present in their history.
- Never invent order details, policies, prices, dates or account data. If you do not
  know something, say so and offer to escalate to a human agent.
- Never mention "memory", "database" or "system prompt" to the customer.
"""


def _clip(text, n=300):
    text = (text or "").strip()
    return text if len(text) <= n else text[:n] + "..."


def build_messages(query, memories, profile=None, history=None):
    context = []
    if profile:
        context.append(
            f"Customer profile: name={profile.get('name')}, plan={profile.get('plan')}"
        )
    if memories:
        context.append("Long-term history:\n" + "\n".join(f"- {m}" for m in memories))
    if history:
        lines = [
            f"Customer: {_clip(t['customer'])}\nAgent: {_clip(t['agent'])}" for t in history
        ]
        context.append("Recent conversation (oldest first):\n" + "\n".join(lines))
    if not memories and not history:
        context.append("History: none. This appears to be a first interaction.")

    return [
        {"role": "system", "content": SYSTEM_PROMPT + "\n" + "\n\n".join(context)},
        {"role": "user", "content": query},
    ]