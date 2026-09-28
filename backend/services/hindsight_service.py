# backend/services/hindsight_service.py
import asyncio
import threading
import sys
import os

# Ensure memory/ folder is discoverable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../memory")))
from hindsight_client import Hindsight

_loop = asyncio.new_event_loop()
_thread = threading.Thread(target=_loop.run_forever, daemon=True)
_thread.start()

def _run_coro(coro):
    future = asyncio.run_coroutine_threadsafe(coro, _loop)
    return future.result()

client = Hindsight(base_url="http://localhost:8888")

def retain(customer_id: str, content: str):
    return _run_coro(client.aretain(bank_id=customer_id, content=content, context="customer review"))

def recall(customer_id: str, message: str):
    results = _run_coro(client.arecall(bank_id=customer_id, query=message))
    if hasattr(results, "results"):
        return [r.text for r in results.results]
    return []

def reflect(customer_id: str, query: str):
    res = _run_coro(client.areflect(bank_id=customer_id, query=query))
    return getattr(res, "text", str(res))
