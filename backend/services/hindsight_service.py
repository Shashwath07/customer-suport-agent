import asyncio
import os
import threading

from hindsight_client import Hindsight

# One persistent event loop in a background thread (keeps aiohttp session alive)
_loop = asyncio.new_event_loop()
threading.Thread(target=_loop.run_forever, daemon=True).start()

client = Hindsight(base_url=os.getenv("HINDSIGHT_URL", "http://localhost:8888"))


def _run(coro):
    return asyncio.run_coroutine_threadsafe(coro, _loop).result()


def retain(customer_id, text):
    _run(client.aretain(bank_id=customer_id, content=text, context="customer review"))


def recall(customer_id, query):
    res = _run(client.arecall(bank_id=customer_id, query=query))
    return [r.text for r in res.results]


def reflect(customer_id, query):
    return _run(client.areflect(bank_id=customer_id, query=query)).text
