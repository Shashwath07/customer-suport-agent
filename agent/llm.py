import os

DEFAULT_MODEL = "llama-3.3-70b-versatile"
_client = None


class LLMError(Exception):
    pass


def _get_client():
    global _client
    if _client is None:
        from groq import Groq

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise LLMError("GROQ_API_KEY is missing. Add it to .env")
        _client = Groq(api_key=api_key)
    return _client


def generate(messages):
    try:
        completion = _get_client().chat.completions.create(
            model=os.getenv("GROQ_MODEL", DEFAULT_MODEL),
            messages=messages,
            temperature=0.3,
            max_tokens=500,
        )
        return completion.choices[0].message.content
    except LLMError:
        raise
    except Exception as e:
        raise LLMError(f"The AI service is unavailable right now: {e}") from e