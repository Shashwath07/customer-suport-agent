# agent/response.py
import re
import os
import sys

# Ensure agent module imports resolve cleanly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import llm
import prompts

FALLBACK = (
    "I'm sorry, I couldn't generate a reply just now. "
    "Please try again, or ask for a human agent."
)

def format_response(text, max_chars=1500):
    if not text or not text.strip():
        return FALLBACK
    text = re.sub(r"^(support agent|agent)\s*:\s*", "", text.strip(), flags=re.I)
    text = re.sub(r"\n{3,}", "\n\n", text)
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] + "..."
    return text

def generate_agent_reply(query, memories, profile=None, history=None):
    """Integrates prompts -> llm -> response formatting."""
    try:
        messages = prompts.build_messages(query, memories, profile=profile, history=history)
        raw_reply = llm.generate(messages)
        return format_response(raw_reply)
    except Exception:
        return FALLBACK
