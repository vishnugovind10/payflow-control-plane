from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .cli import scenarios
from .domain import (
    ROUTES,
    PaymentIntent,
    evaluate_routes,
    sample_mandate,
    simulate_payment,
)

DB_PATH = Path(__file__).resolve().parents[2] / "payflow.sqlite3"
app = FastAPI(
    title="PayFlow Control Plane",
    version="0.1.0",
    description="Synthetic deterministic payment route evaluation.",
)


class IntentInput(BaseModel):
    id: str = "pay_api"
    payer_id: str = "payer_demo"
    beneficiary_id: str = "beneficiary_demo"
    agent_id: str = "agent_demo"
    amount: float = Field(gt=0)
    source_currency: str
    destination_currency: str
    source_country: str = "NL"
    destination_country: str = "BR"
    payment_type: str = "B2B_PAYOUT"
    purpose: str = "synthetic demo"
    deadline_seconds: int = Field(default=1800, gt=0)
    mandate_id: str = "mandate_demo"
    maximum_cost: float = 10_000
    maximum_risk: float = 0.35
    created_at: str = "2026-01-01T00:00:00+00:00"


def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "CREATE TABLE IF NOT EXISTS decision_ledger (id INTEGER PRIMARY KEY, payment_id TEXT, decision TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, payload TEXT NOT NULL)"
    )
    con.commit()
    return con


def record(payment_id: str, decision: str, payload: dict[str, Any]):
    with closing(db()) as con:
        con.execute(
            "INSERT INTO decision_ledger (payment_id, decision, payload) VALUES (?, ?, ?)",
            (payment_id, str(decision), json.dumps(payload, default=str)),
        )
        con.commit()


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "synthetic", "live_rails": False}


@app.get("/api/routes")
def get_routes():
    return [asdict(r) for r in ROUTES]


@app.get("/api/scenarios")
def get_scenarios():
    return scenarios()


@app.get("/api/treasury")
def treasury():
    return {
        "label": "SYNTHETIC / ILLUSTRATIVE",
        "balances": {"EUR": 2_400_000, "USDC": 800_000, "BRL": 4_100_000, "MXN": 1_200_000},
        "reserved_liquidity": 200_000,
        "pending_settlements": 3,
        "capital_locked": 145_000,
        "utilization_pct": 34.6,
    }


@app.get("/api/ledger")
def ledger():
    with closing(db()) as con:
        rows = con.execute(
            "SELECT payment_id, decision, created_at, payload FROM decision_ledger ORDER BY id DESC LIMIT 100"
        ).fetchall()
    return [
        {"payment_id": r[0], "decision": r[1], "created_at": r[2], "payload": json.loads(r[3])}
        for r in rows
    ]


@app.post("/api/payment/evaluate")
def evaluate(data: IntentInput):
    intent = PaymentIntent(**data.model_dump())
    result = evaluate_routes(intent, sample_mandate(), now=datetime(2026, 10, 26, 12, tzinfo=UTC))
    record(intent.id, result["decision"], result)
    return result


@app.post("/api/payment/execute")
def execute(data: IntentInput):
    intent = PaymentIntent(**data.model_dump())
    result = evaluate_routes(intent, sample_mandate(), now=datetime(2026, 10, 26, 12, tzinfo=UTC))
    if not result["recommended_route"]:
        record(intent.id, result["decision"], result)
        raise HTTPException(
            409, detail={"decision": result["decision"], "reasoning": result["reasoning"]}
        )
    result = simulate_payment(intent)
    record(intent.id, result["decision"], result)
    return result


@app.get("/api/payment/{payment_id}")
def get_payment(payment_id: str):
    with closing(db()) as con:
        row = con.execute(
            "SELECT payload FROM decision_ledger WHERE payment_id=? ORDER BY id DESC LIMIT 1",
            (payment_id,),
        ).fetchone()
    if not row:
        raise HTTPException(404, "payment not found")
    return json.loads(row[0])


@app.get("/api/agents/{agent_id}")
def agent(agent_id: str):
    if agent_id != "agent_demo":
        raise HTTPException(404, "agent not found")
    return {
        "agent_id": agent_id,
        "mandate": asdict(sample_mandate()),
        "spend_used": 3_000,
        "pending_spend": 4_000,
        "remaining_authority": 993_000,
    }
