# Architecture

PayFlow keeps nine concepts distinct: intent, authority, compliance, economic evaluation, routing, execution, settlement, reconciliation and assurance. Route hard gates run before ranking. A missing critical compliance input or stale quote can cause abstention; a violated authority, beneficiary or corridor constraint causes no-go. A route recommendation is not an authorization to connect to real payment infrastructure.

`src/payflow/domain.py` owns deterministic typed inputs, constraints, cost, weighted rank, reservation ledger and simulated receipt. `api.py` exposes that model with FastAPI and stores decision payloads in a local SQLite ledger. `dashboard/` renders the five executive questions. `protocols/` contains small translation examples from machine payment-shaped payloads into the internal intent. The core has no dependency on those adapters.

Lifecycle state is represented as separate receipt fields. A successful simulated settlement may still fail reconciliation or assurance in a real system; this demo’s canonical receipt marks each state for illustration and the `analysis.reconcile` helper exposes mismatches.
