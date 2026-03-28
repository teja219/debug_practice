# Reported Problems — OrderFlow System

These are real bug reports filed by QA and production monitoring.
Your task: identify the root cause of each reported problem by
examining the system spec and the code in `buggy_system.py`.

---

## Problem 1
**Title:** Orders failing for last item in stock

**Report:**
> When exactly 1 unit remains in inventory, customers receive
> "Out of stock" errors even though inventory shows stock > 0.

---

## Problem 2
**Title:** Oversell detected — stock went negative in production

**Report:**
> Under high load, we've seen inventory go to -1 or -2 for
> popular items, meaning more units were sold than available.

---

## Problem 3
**Title:** Customer charged twice for the same order

**Report:**
> When the client retried a failed request, some customers
> were charged twice. The payment service is supposed to be idempotent.

---

## Problem 4
**Title:** Refund records disappearing — finance team can't reconcile

**Report:**
> After issuing refunds, there's no trace of the original charge
> or refund in the payment database. Audits are failing.

---

## Problem 5
**Title:** Notification retry behavior inconsistent with spec

**Report:**
> The spec states notifications should retry up to 3 times.
> Monitoring shows 4 delivery attempts in logs for failed sends.

---

## Problem 6
**Title:** Order API response is slow when email delivery is delayed

**Report:**
> Order confirmation API calls sometimes take 3–5 seconds longer
> than expected. Notification failures seem correlated with slow responses.

---

*Good luck. Talk through each bug: what the symptom is, where in
the code the root cause lives, and what the correct fix would be.*
