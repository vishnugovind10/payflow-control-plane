# PayFlow Control Plane

**Economic and operational control infrastructure for stablecoin and agentic cross-border payments.**

PayFlow evaluates a payment intent across bounded authority, compliance evidence, FX, liquidity, routing and treasury consequence. It treats payment execution as an economic decision, not just a transaction broadcast.

> **All rates, routes, liquidity and balances are synthetic and illustrative. This repository does not process, execute or settle real payments.**

## See the decision

```text
Payment intent → mandate and policy gates → route economics → weighted ranking
               → simulated execution → settlement → reconciliation → treasury impact
```

Quick start (Python 3.11+):

```powershell
python -m pip install -e ".[dev]"
pytest -q
ruff check .
python -m payflow.cli demo
```

Run the API and dashboard in two terminals:

```powershell
uvicorn payflow.api:app --reload
cd dashboard
npm install
npm run dev
```

Open <http://localhost:5173>. API docs are at <http://localhost:8000/docs>.

## Canonical demo: €100,000 EUR → BRL

The engine applies hard constraints first, then ranks eligible synthetic routes using an explicit payment-type weighted score. The sample uses a 60 bps illustrative customer take rate and calculates route cost, expected failure loss, capital cost, contribution, settlement time and treasury impact. The API’s `POST /api/payment/evaluate` returns every candidate and its exclusions. `POST /api/payment/execute` simulates only when a route is eligible.

Route score components are normalized cost, risk, liquidity scarcity, settlement time, failure probability, capital usage and counterparty risk. See [routing methodology](docs/routing-methodology.md). Changing assumptions can change the winner; stablecoin routes are not presumed superior.

## What is included

- Typed intents, bounded mandates, synthetic route data and payment-type weights
- Deterministic route evaluation for EUR → BRL, USD → BRL and USD → MXN
- Hard gates for mandate, beneficiary, corridor, compliance evidence, stale FX, liquidity, deadline, risk and maximum cost
- Concurrent spend reservations for pending agent payments
- Simulated receipt with distinct authorized, executed, settled, reconciled and assured states
- Treasury impact, reconciliation comparison, unit economics, seeded Monte Carlo cost bands and sensitivity analysis
- Small FastAPI API, SQLite decision ledger and five-panel React dashboard
- Protocol-neutral MPP-like and x402-like payload adapters; no live protocol dependencies

## API

`GET /api/health`, `/api/routes`, `/api/scenarios`, `/api/treasury`, `/api/ledger`, `/api/agents/{id}`; `POST /api/payment/evaluate` and `/api/payment/execute`; `GET /api/payment/{id}`. SQLite is created locally at repository-root `payflow.sqlite3` only when API ledger endpoints are used.

## Executive views

The dashboard answers five questions: can this payment be served; which rail; which corridor; what it costs; and what changes in treasury. It is an operator-facing illustration, not a payment terminal.

## Architecture and limits

The system uses deterministic in-memory synthetic fixtures and SQLite only for the local decision ledger. No production custody, blockchain RPC, banks, FX providers, compliance screening, real-time liquidity, or external payment execution is connected. The reference model is not regulatory advice or a production security claim.

See [architecture](docs/architecture.md), [payment economics](docs/payment-economics.md), [treasury model](docs/treasury-model.md), [agentic payments](docs/agentic-payments.md), [corridors](docs/corridor-model.md) and [threat model](docs/threat-model.md).

## Related public work

This project connects bounded agent authority and settlement/assurance ideas to payment routing economics: [Agent Trust Probe](https://github.com/vishnugovind10/agent-trust-probe), [Agentic Financial Consequence](https://github.com/vishnugovind10/agentic-financial-consequence), [Institutional Settlement State Machine](https://github.com/vishnugovind10/institutional-settlement-state-machine), and [Institutional Digital Asset Assurance](https://github.com/vishnugovind10/institutional-digital-asset-assurance). These links describe conceptual lineage, not shared deployment or integrations.

## License

MIT. See [LICENSE](LICENSE).
