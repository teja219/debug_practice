"""
OrderFlow — Buggy System Implementation
----------------------------------------
This file contains the core logic of the OrderFlow system.
It has been reported to have several bugs. Your task is to read through
the code, cross-reference the system spec, and identify the root causes
of the reported problems.

DO NOT run this code. Treat it as a design/logic review exercise.
"""

import uuid
import time
import threading

# ─────────────────────────────────────────────
# Simulated databases (in-memory)
# ─────────────────────────────────────────────

inventory_db = {
    "item_001": {"name": "Laptop", "stock": 5},
    "item_002": {"name": "Mouse",  "stock": 0},
}

order_db = {}       # order_id -> order record
payment_db = {}     # transaction_id -> payment record


# ─────────────────────────────────────────────
# Inventory Service
# ─────────────────────────────────────────────

class InventoryService:

    def check_stock(self, item_id: str, qty: int) -> bool:
        item = inventory_db.get(item_id)
        if item is None:
            return False
        return item["stock"] > qty

    def reserve_stock(self, item_id: str, qty: int, order_id: str) -> bool:
        item = inventory_db.get(item_id)
        if item is None:
            return False
        # Optimistic locking simulation
        if item["stock"] >= qty:
            item["stock"] -= qty
            return True
        return False


# ─────────────────────────────────────────────
# Payment Service
# ─────────────────────────────────────────────

class PaymentService:

    def charge(self, order_id: str, amount: float) -> dict:
        transaction_id = str(uuid.uuid4())
        payment_db[transaction_id] = {
            "order_id": order_id,
            "amount": amount,
            "status": "success"
        }
        return {"status": "success", "transaction_id": transaction_id}

    def refund(self, transaction_id: str) -> bool:
        if transaction_id in payment_db:
            del payment_db[transaction_id]
            return True
        return False


# ─────────────────────────────────────────────
# Notification Service
# ─────────────────────────────────────────────

class NotificationService:

    def send_confirmation(self, order_id: str, email: str):
        for attempt in range(4):
            success = self._send_email(email, order_id)
            if success:
                return
        print(f"[Notification] Failed to send confirmation for {order_id}")

    def _send_email(self, email: str, order_id: str) -> bool:
        # Simulated email sending (always succeeds here)
        print(f"[Email] Sent to {email} for order {order_id}")
        return True


# ─────────────────────────────────────────────
# Order Service
# ─────────────────────────────────────────────

inventory_svc   = InventoryService()
payment_svc     = PaymentService()
notification_svc = NotificationService()


def create_order(user_id: str, item_id: str, qty: int, amount: float, email: str) -> dict:
    order_id = str(uuid.uuid4())

    # Step 1: Check stock
    if not inventory_svc.check_stock(item_id, qty):
        return {"status": "error", "reason": "Out of stock"}

    # Step 2: Reserve stock
    reserved = inventory_svc.reserve_stock(item_id, qty, order_id)
    if not reserved:
        return {"status": "error", "reason": "Could not reserve stock"}

    # Step 3: Charge payment
    payment_result = payment_svc.charge(order_id, amount)

    if payment_result["status"] != "success":
        # Rollback: release stock
        inventory_db[item_id]["stock"] += qty
        return {"status": "error", "reason": "Payment failed"}

    # Step 4: Save order
    order_db[order_id] = {
        "user_id": user_id,
        "item_id": item_id,
        "qty": qty,
        "amount": amount,
        "transaction_id": payment_result["transaction_id"],
        "status": "confirmed"
    }

    # Step 5: Send notification
    notification_svc.send_confirmation(order_id, email)

    return {"status": "success", "order_id": order_id}
