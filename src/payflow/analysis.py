from dataclasses import replace
from datetime import UTC, datetime

from .domain import ROUTES, PaymentIntent, evaluate_routes


def liquidity_sensitivity(
    intent: PaymentIntent, *, costs_bps: tuple[float, ...] = (0, 10, 20, 30, 40)
) -> list[dict[str, object]]:
    """Compare route decisions as every candidate's liquidity cost changes."""
    now = datetime(2026, 10, 26, 12, tzinfo=UTC)
    output = []
    for bps in costs_bps:
        candidates = [
            replace(r, liquidity_cost_bps=bps)
            for r in ROUTES
            if r.fx_rate
            == {"EUR-BRL": 5.45, "USD-BRL": 5.62, "USD-MXN": 17.1}.get(
                f"{intent.source_currency}-{intent.destination_currency}"
            )
        ]
        result = evaluate_routes(intent, routes=candidates, now=now)
        output.append(
            {
                "liquidity_cost_bps": bps,
                "decision": str(result["decision"]),
                "recommended_route": result["recommended_route"],
            }
        )
    return output


def reconcile(expected: dict[str, object], actual: dict[str, object]) -> dict[str, object]:
    """Compare critical settlement fields; unknown or mismatching state never matches."""
    keys = ("payment_id", "beneficiary_id", "amount", "currency", "route_id")
    mismatches = [
        key
        for key in keys
        if key not in expected or key not in actual or expected[key] != actual[key]
    ]
    return {"status": "MATCHED" if not mismatches else "MISMATCH", "mismatches": mismatches}
