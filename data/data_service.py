# data/data_service.py
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_json(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

CUSTOMERS = {c["customer_id"]: c for c in _load_json("customers.json")}
TICKETS = _load_json("tickets.json")

def get_customer(customer_id: str):
    return CUSTOMERS.get(customer_id.upper())

def get_customer_tickets(customer_id: str):
    cid = customer_id.upper()
    return [t for t in TICKETS if t.get("customer_id") == cid]
