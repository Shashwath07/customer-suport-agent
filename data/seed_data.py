# data/seed_data.py
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from data.data_service import CUSTOMERS, TICKETS
from memory import memory_service as ms

def seed():
    for cid, profile in CUSTOMERS.items():
        ms.save_customer_profile(cid, profile)

    for t in TICKETS:
        cid = t["customer_id"]
        ticket_summary = f"Ticket {t['ticket_id']}: {t['issue']}. Attempted solution: {t['solution_attempted']}. Outcome: {t['result']}."
        ms.save_customer_memory(cid, ticket_summary, context="Support ticket history")

if __name__ == "__main__":
    seed()
