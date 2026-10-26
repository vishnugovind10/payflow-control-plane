from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class Decision(StrEnum):
    ROUTE = "ROUTE"
    ABSTAIN = "ABSTAIN"
    NO_GO = "NO_GO"


@dataclass(frozen=True)
class PaymentIntent:
    id: str
    payer_id: str
    beneficiary_id: str
    amount: float
    source_currency: str
    destination_currency: str
    source_country: str
    destination_country: str
    payment_type: str
    purpose: str
    deadline_seconds: int
    agent_id: str = "agent_demo"
    mandate_id: str = "mandate_demo"
    maximum_cost: float = 10_000
    maximum_risk: float = 0.35
    created_at: str = "2026-01-01T00:00:00+00:00"


@dataclass(frozen=True)
class PaymentMandate:
    id: str
    principal_id: str
    agent_id: str
    max_transaction_amount: float
    cumulative_spend_limit: float
    cumulative_spend_used: float = 0
    allowed_currencies: tuple[str, ...] = ("EUR", "USD", "BRL", "MXN")
    allowed_corridors: tuple[str, ...] = ("EUR-BRL", "USD-BRL", "USD-MXN")
    allowed_beneficiaries: tuple[str, ...] = ("beneficiary_demo",)
    allowed_payment_types: tuple[str, ...] = (
        "B2B_PAYOUT",
        "MERCHANT_SETTLEMENT",
        "REMITTANCE",
        "AGENTIC_PAYMENT",
    )
    allowed_rails: tuple[str, ...] = ("BANK", "EVM", "SOLANA", "HYBRID")
    expires_at: str = "2030-01-01T00:00:00+00:00"


@dataclass(frozen=True)
class Route:
    route_id: str
    name: str
    source_rail: str
    settlement_asset: str
    destination_rail: str
    settlement_time_seconds: int
    fx_spread_bps: float
    provider_fee_bps: float
    network_fee: float
    liquidity_cost_bps: float
    off_ramp_cost_bps: float
    failure_probability: float
    counterparty_risk: float
    prefunding_requirement: float
    capital_locked: float
    available_liquidity: float
    stablecoin_exposure: float = 0
    compliance_status: str = "APPROVE"
    fx_rate: float = 1.0
    fx_as_of: str = "2026-10-26T09:00:00+00:00"
    fx_expires_at: str = "2026-10-27T09:00:00+00:00"


@dataclass
class RouteEvaluation:
    route_id: str
    name: str
    eligible: bool
    rejection_reasons: list[str]
    total_cost: float
    expected_loss: float
    contribution_margin: float
    margin_pct: float
    settlement_seconds: int
    score: float | None
    risk: float
    treasury_impact: dict[str, float]


ROUTES = [
    Route(
        "bank_eur_brl",
        "Bank / local payout",
        "BANK",
        "FIAT",
        "BANK",
        10_800,
        24,
        18,
        2.5,
        8,
        12,
        0.004,
        0.12,
        0,
        12_000,
        4_000_000,
        fx_rate=5.45,
    ),
    Route(
        "evm_eur_brl",
        "EVM stablecoin",
        "EVM",
        "USDC",
        "BANK",
        840,
        12,
        15,
        18,
        22,
        28,
        0.018,
        0.23,
        80_000,
        80_000,
        1_500_000,
        0.82,
        fx_rate=5.45,
    ),
    Route(
        "sol_eur_brl",
        "Solana stablecoin",
        "SOLANA",
        "USDC",
        "PIX_SIM",
        120,
        15,
        12,
        3,
        28,
        25,
        0.009,
        0.18,
        65_000,
        65_000,
        900_000,
        0.78,
        fx_rate=5.45,
    ),
    Route(
        "hybrid_eur_brl",
        "Hybrid treasury route",
        "HYBRID",
        "USDC",
        "BANK",
        1_200,
        18,
        14,
        5,
        18,
        19,
        0.006,
        0.14,
        55_000,
        55_000,
        1_200_000,
        0.35,
        fx_rate=5.45,
    ),
    Route(
        "bank_usd_brl",
        "Bank / local payout",
        "BANK",
        "FIAT",
        "BANK",
        14_400,
        20,
        16,
        2,
        8,
        10,
        0.005,
        0.12,
        0,
        9_000,
        5_000_000,
        fx_rate=5.62,
    ),
    Route(
        "sol_usd_brl",
        "Solana stablecoin",
        "SOLANA",
        "USDC",
        "PIX_SIM",
        150,
        16,
        14,
        3,
        25,
        22,
        0.009,
        0.18,
        60_000,
        60_000,
        1_000_000,
        0.8,
        fx_rate=5.62,
    ),
    Route(
        "hybrid_usd_brl",
        "Hybrid treasury route",
        "HYBRID",
        "USDC",
        "BANK",
        1_500,
        17,
        13,
        5,
        16,
        18,
        0.006,
        0.13,
        50_000,
        50_000,
        1_400_000,
        0.32,
        fx_rate=5.62,
    ),
    Route(
        "bank_usd_mxn",
        "Bank / local payout",
        "BANK",
        "FIAT",
        "BANK",
        9_000,
        18,
        16,
        2,
        7,
        9,
        0.004,
        0.1,
        0,
        5_000,
        2_000_000,
        fx_rate=17.1,
    ),
    Route(
        "sol_usd_mxn",
        "Solana stablecoin",
        "SOLANA",
        "USDC",
        "SPEI_SIM",
        100,
        14,
        12,
        3,
        22,
        19,
        0.008,
        0.17,
        12_000,
        12_000,
        500_000,
        0.8,
        fx_rate=17.1,
    ),
]

WEIGHTS: dict[str, dict[str, float]] = {
    "B2B_PAYOUT": {
        "cost": 0.28,
        "risk": 0.2,
        "liquidity": 0.15,
        "settlement": 0.12,
        "failure": 0.1,
        "capital": 0.1,
        "counterparty": 0.05,
    },
    "MERCHANT_SETTLEMENT": {
        "cost": 0.2,
        "risk": 0.12,
        "liquidity": 0.2,
        "settlement": 0.2,
        "failure": 0.15,
        "capital": 0.08,
        "counterparty": 0.05,
    },
    "REMITTANCE": {
        "cost": 0.22,
        "risk": 0.12,
        "liquidity": 0.1,
        "settlement": 0.22,
        "failure": 0.12,
        "capital": 0.08,
        "counterparty": 0.14,
    },
    "AGENTIC_PAYMENT": {
        "cost": 0.2,
        "risk": 0.12,
        "liquidity": 0.12,
        "settlement": 0.2,
        "failure": 0.18,
        "capital": 0.08,
        "counterparty": 0.1,
    },
}


def sample_mandate(**updates: Any) -> PaymentMandate:
    fields = asdict(PaymentMandate("mandate_demo", "payer_demo", "agent_demo", 500_000, 1_000_000))
    fields.update(updates)
    for key in (
        "allowed_currencies",
        "allowed_corridors",
        "allowed_beneficiaries",
        "allowed_payment_types",
        "allowed_rails",
    ):
        fields[key] = tuple(fields[key])
    return PaymentMandate(**fields)


def sample_intent(**updates: Any) -> PaymentIntent:
    fields = asdict(
        PaymentIntent(
            "pay_demo_001",
            "payer_demo",
            "beneficiary_demo",
            100_000,
            "EUR",
            "BRL",
            "NL",
            "BR",
            "B2B_PAYOUT",
            "supplier payout",
            1800,
        )
    )
    fields.update(updates)
    return PaymentIntent(**fields)


def _mandatory_reasons(
    intent: PaymentIntent, mandate: PaymentMandate, route: Route, now: datetime
) -> list[str]:
    reasons: list[str] = []
    corridor = f"{intent.source_currency}-{intent.destination_currency}"
    if (
        intent.payer_id != mandate.principal_id
        or intent.amount > mandate.max_transaction_amount
        or intent.amount + mandate.cumulative_spend_used > mandate.cumulative_spend_limit
    ):
        reasons.append("MANDATE_VIOLATION")
    if intent.beneficiary_id not in mandate.allowed_beneficiaries:
        reasons.append("BENEFICIARY_NOT_ALLOWED")
    if corridor not in mandate.allowed_corridors:
        reasons.append("CORRIDOR_NOT_SUPPORTED")
    if (
        intent.payment_type not in mandate.allowed_payment_types
        or route.source_rail not in mandate.allowed_rails
    ):
        reasons.append("MANDATE_VIOLATION")
    if datetime.fromisoformat(mandate.expires_at) <= now:
        reasons.append("MANDATE_EXPIRED")
    if route.compliance_status == "FAIL":
        reasons.append("COMPLIANCE_FAILURE")
    if route.compliance_status in {"MISSING", "ABSTAIN"}:
        reasons.append("COMPLIANCE_EVIDENCE_MISSING")
    if now >= datetime.fromisoformat(route.fx_expires_at):
        reasons.append("STALE_FX")
    if route.available_liquidity < intent.amount:
        reasons.append("INSUFFICIENT_LIQUIDITY")
    if route.settlement_time_seconds > intent.deadline_seconds:
        reasons.append("SETTLEMENT_DEADLINE_IMPOSSIBLE")
    if route.counterparty_risk > intent.maximum_risk:
        reasons.append("COUNTERPARTY_RISK_THRESHOLD")
    return reasons


def evaluate_routes(
    intent: PaymentIntent,
    mandate: PaymentMandate | None = None,
    routes: list[Route] | None = None,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    mandate = mandate or sample_mandate()
    now = now or datetime.now(UTC)
    routes = routes or ROUTES
    # Route IDs are synthetic; corridor membership is explicit via the configured FX pair.
    expected_rate = {"EUR-BRL": 5.45, "USD-BRL": 5.62, "USD-MXN": 17.1}.get(
        f"{intent.source_currency}-{intent.destination_currency}"
    )
    candidates = [r for r in routes if expected_rate is not None and r.fx_rate == expected_rate]
    if not candidates:
        return {
            "decision": Decision.ABSTAIN,
            "recommended_route": None,
            "reasoning": ["NO_ROUTE_OR_FX_EVIDENCE"],
            "routes": [],
        }
    weights = WEIGHTS.get(intent.payment_type, WEIGHTS["B2B_PAYOUT"])
    evaluations: list[RouteEvaluation] = []
    max_cost = max(intent.amount * 0.1, 1)
    for route in candidates:
        reasons = _mandatory_reasons(intent, mandate, route, now)
        proportional = (
            intent.amount
            * (
                route.fx_spread_bps
                + route.provider_fee_bps
                + route.liquidity_cost_bps
                + route.off_ramp_cost_bps
            )
            / 10_000
        )
        expected_loss = intent.amount * route.failure_probability * route.counterparty_risk
        capital_cost = (
            route.capital_locked * 0.12 * route.settlement_time_seconds / (365 * 24 * 3600)
        )
        cost = proportional + route.network_fee + expected_loss + capital_cost
        if cost > intent.maximum_cost:
            reasons.append("MAX_COST_EXCEEDED")
        revenue = intent.amount * 0.006
        margin = revenue - cost
        risk = min(
            1,
            route.failure_probability
            + route.counterparty_risk * 0.25
            + route.stablecoin_exposure * 0.08,
        )
        score = (
            weights["cost"] * min(cost / max_cost, 1)
            + weights["risk"] * risk
            + weights["liquidity"]
            * (1 - min(route.available_liquidity / max(intent.amount * 5, 1), 1))
            + weights["settlement"]
            * min(route.settlement_time_seconds / max(intent.deadline_seconds, 1), 1)
            + weights["failure"] * route.failure_probability
            + weights["capital"] * min(route.capital_locked / max(intent.amount, 1), 1)
            + weights["counterparty"] * route.counterparty_risk
        )
        evaluations.append(
            RouteEvaluation(
                route.route_id,
                route.name,
                not reasons,
                reasons,
                round(cost, 2),
                round(expected_loss, 2),
                round(margin, 2),
                round(margin / intent.amount * 100, 4),
                route.settlement_time_seconds,
                round(score, 5) if not reasons else None,
                round(risk, 4),
                {
                    "liquidity_consumed": round(
                        min(route.prefunding_requirement, route.available_liquidity), 2
                    ),
                    "capital_locked": round(route.capital_locked, 2),
                    "stablecoin_exposure": round(intent.amount * route.stablecoin_exposure, 2),
                    "prefunding_requirement": route.prefunding_requirement,
                },
            )
        )
    eligible = sorted(
        (e for e in evaluations if e.eligible), key=lambda e: (e.score, e.total_cost, e.route_id)
    )
    abstention_reasons = {"STALE_FX", "COMPLIANCE_EVIDENCE_MISSING"}
    hard_reasons = {
        "MANDATE_VIOLATION",
        "MANDATE_EXPIRED",
        "BENEFICIARY_NOT_ALLOWED",
        "CORRIDOR_NOT_SUPPORTED",
        "COMPLIANCE_FAILURE",
        "INSUFFICIENT_LIQUIDITY",
        "MAX_COST_EXCEEDED",
        "COUNTERPARTY_RISK_THRESHOLD",
    }
    all_reasons = {reason for evaluation in evaluations for reason in evaluation.rejection_reasons}
    unresolved_all_routes = all(
        evaluation.rejection_reasons
        and abstention_reasons.intersection(evaluation.rejection_reasons)
        for evaluation in evaluations
    )
    decision = (
        Decision.ROUTE
        if eligible
        else (
            Decision.NO_GO
            if hard_reasons.intersection(all_reasons)
            else Decision.ABSTAIN
            if unresolved_all_routes
            else Decision.NO_GO
        )
    )
    return {
        "decision": decision,
        "recommended_route": eligible[0].route_id if eligible else None,
        "reasoning": [
            f"Lowest weighted score among {len(eligible)} eligible synthetic routes"
            if eligible
            else "No route meets required evidence and hard constraints"
        ],
        "routes": [asdict(e) for e in evaluations],
        "weights": weights,
        "intent_id": intent.id,
    }


class SpendReservations:
    """Small deterministic in-memory reservation ledger for concurrent agent spend."""

    def __init__(self, mandate_limit: float, settled: float = 0):
        self.mandate_limit, self.settled = mandate_limit, settled
        self.pending: dict[str, float] = {}

    @property
    def available(self) -> float:
        return self.mandate_limit - self.settled - sum(self.pending.values())

    def reserve(self, payment_id: str, amount: float) -> bool:
        if amount <= 0 or payment_id in self.pending or amount > self.available:
            return False
        self.pending[payment_id] = amount
        return True

    def settle(self, payment_id: str) -> bool:
        amount = self.pending.pop(payment_id, None)
        if amount is None:
            return False
        self.settled += amount
        return True

    def release(self, payment_id: str) -> bool:
        return self.pending.pop(payment_id, None) is not None


def simulate_payment(intent: PaymentIntent | None = None) -> dict[str, Any]:
    intent = intent or sample_intent()
    result = evaluate_routes(intent, now=datetime(2026, 10, 26, 12, tzinfo=UTC))
    route = next(
        (r for r in result["routes"] if r["route_id"] == result["recommended_route"]), None
    )
    if not route:
        return {
            **result,
            "authorized": result["decision"] == Decision.NO_GO,
            "executed": False,
            "settled": False,
            "reconciled": False,
            "assured": False,
        }
    return {
        **result,
        "authorized": True,
        "executed": True,
        "settled": True,
        "reconciled": True,
        "assured": True,
        "receipt": {
            "payment_id": intent.id,
            "status": "SETTLED",
            "route": route["route_id"],
            "amount": intent.amount,
            "source_currency": intent.source_currency,
            "destination_currency": intent.destination_currency,
            "total_cost": route["total_cost"],
            "contribution_margin": route["contribution_margin"],
            "treasury_impact": route["treasury_impact"],
            "reconciliation": "MATCHED",
            "authorized": True,
            "executed": True,
            "settled": True,
            "reconciled": True,
            "assured": True,
        },
    }


def corridor_model(
    volume: float, take_rate_bps: float, variable_cost_bps: float, fixed_monthly_cost: float = 0
) -> dict[str, float]:
    revenue = volume * take_rate_bps / 10_000
    variable = volume * variable_cost_bps / 10_000
    margin = revenue - variable - fixed_monthly_cost
    return {
        "monthly_volume": volume,
        "gross_revenue": round(revenue, 2),
        "variable_cost": round(variable, 2),
        "contribution_margin": round(margin, 2),
        "contribution_margin_pct": round(margin / volume * 100, 4) if volume else 0,
        "contribution_per_1m": round(margin / volume * 1_000_000, 2) if volume else 0,
    }


def monte_carlo_cost(
    base_cost: float, failure_probability: float, *, runs: int = 1000, seed: int = 7
) -> dict[str, float]:
    import random

    if runs < 1 or not 0 <= failure_probability <= 1:
        raise ValueError("runs must be positive and probability must be between 0 and 1")
    rng = random.Random(seed)
    costs = sorted(
        base_cost * rng.uniform(0.97, 1.04)
        + (base_cost * 1.5 if rng.random() < failure_probability else 0)
        for _ in range(runs)
    )
    percentile = lambda p: costs[min(int((runs - 1) * p), runs - 1)]
    return {
        "expected_cost": round(sum(costs) / runs, 2),
        "p50": round(percentile(0.5), 2),
        "p90": round(percentile(0.9), 2),
        "p95": round(percentile(0.95), 2),
        "worst_case": round(costs[-1], 2),
    }
