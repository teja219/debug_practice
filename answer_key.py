"""
INTERVIEWER ANSWER KEY — DO NOT SHARE WITH CANDIDATE
======================================================
This file maps each reported problem to its root cause in buggy_system.py.
Use this to evaluate the candidate's responses.
"""

ANSWER_KEY = [
    {
        "problem": 1,
        "title": "Orders failing for last item in stock",
        "bug_location": "InventoryService.check_stock(), line: return item['stock'] > qty",
        "root_cause": (
            "Off-by-one error: uses strict greater-than (>) instead of >= . "
            "When stock == qty (exactly enough), the check returns False, "
            "incorrectly treating it as out of stock."
        ),
        "fix": "Change `item['stock'] > qty` to `item['stock'] >= qty`.",
        "score_hints": [
            "Candidate should spot the > vs >= distinction",
            "Bonus: mention this is a classic boundary condition bug",
        ]
    },
    {
        "problem": 2,
        "title": "Oversell — stock went negative",
        "bug_location": "InventoryService.reserve_stock() — no atomic lock",
        "root_cause": (
            "The check-then-act on stock is not atomic. Two concurrent requests "
            "can both pass the `if item['stock'] >= qty` check before either "
            "decrements the stock, causing a race condition / TOCTOU bug."
        ),
        "fix": (
            "Use a threading.Lock() or database-level row lock / compare-and-swap "
            "to make the check-and-decrement atomic."
        ),
        "score_hints": [
            "Should name the race condition / TOCTOU pattern",
            "Bonus: mention optimistic vs pessimistic locking strategies",
            "Bonus: note the spec mentions optimistic locking but it's not implemented",
        ]
    },
    {
        "problem": 3,
        "title": "Customer charged twice",
        "bug_location": "PaymentService.charge() — no idempotency check",
        "root_cause": (
            "The charge() method always creates a new transaction without checking "
            "if a payment for this order_id already exists. The spec requires "
            "idempotency using order_id as the key."
        ),
        "fix": (
            "Before charging, check if any existing payment_db entry has the same order_id. "
            "If found, return the existing transaction instead of creating a new one."
        ),
        "score_hints": [
            "Should identify missing idempotency guard",
            "Bonus: explain what idempotency means in payments context",
        ]
    },
    {
        "problem": 4,
        "title": "Refund records disappearing",
        "bug_location": "PaymentService.refund() — `del payment_db[transaction_id]`",
        "root_cause": (
            "The refund() method deletes the payment record entirely instead of "
            "updating its status to 'refunded'. This destroys the audit trail "
            "needed by the finance team."
        ),
        "fix": (
            "Instead of `del payment_db[transaction_id]`, update the record: "
            "`payment_db[transaction_id]['status'] = 'refunded'`."
        ),
        "score_hints": [
            "Should identify destructive delete vs status update",
            "Bonus: mention immutability / audit log best practices",
        ]
    },
    {
        "problem": 5,
        "title": "Notification retries inconsistent with spec",
        "bug_location": "NotificationService.send_confirmation() — `range(4)`",
        "root_cause": (
            "range(4) iterates 0,1,2,3 — that's 4 attempts total. "
            "The spec says retry up to 3 times (1 initial + 2 retries = 3 max, or 3 retries = 4 total). "
            "Either way, `range(4)` gives one more attempt than intended (spec says max 3 retries)."
        ),
        "fix": "Change `range(4)` to `range(3)` to match the spec's max-3-retry requirement.",
        "score_hints": [
            "Should catch the off-by-one in range()",
            "Bonus: clarify 'retry 3 times' ambiguity (3 attempts total vs 3 retries after first)",
        ]
    },
    {
        "problem": 6,
        "title": "Order API slow when notifications are delayed",
        "bug_location": "create_order() — notification called synchronously before return",
        "root_cause": (
            "notification_svc.send_confirmation() is called synchronously inside create_order(). "
            "The spec says notifications are async and non-blocking. Any delay in email delivery "
            "directly adds latency to the order API response."
        ),
        "fix": (
            "Run the notification in a background thread or push to an async queue "
            "before returning the response. Example: "
            "`threading.Thread(target=notification_svc.send_confirmation, args=(...)).start()`"
        ),
        "score_hints": [
            "Should identify sync vs async violation",
            "Bonus: mention queue-based approach (SQS, Celery, etc.) for production",
            "Bonus: note that the spec explicitly calls notifications 'non-blocking'",
        ]
    },
]


def run_debrief():
    """Print the full answer key for the interviewer."""
    print("=" * 60)
    print("ORDERFLOW DEBUGGING INTERVIEW — ANSWER KEY")
    print("=" * 60)
    for item in ANSWER_KEY:
        print(f"\n[Problem {item['problem']}] {item['title']}")
        print(f"  Location  : {item['bug_location']}")
        print(f"  Root Cause: {item['root_cause']}")
        print(f"  Fix       : {item['fix']}")
        print(f"  Hints     :")
        for h in item['score_hints']:
            print(f"    - {h}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_debrief()
