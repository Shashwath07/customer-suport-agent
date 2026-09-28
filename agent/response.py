import re

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