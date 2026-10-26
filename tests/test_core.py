from datetime import UTC, datetime

from payflow.domain import (
    ROUTES,
    Decision,
    SpendReservations,
    corridor_model,
    evaluate_routes,
    monte_carlo_cost,
    sample_intent,
    simulate_payment,
)

NOW = datetime(2026, 10, 26, 12, tzinfo=UTC)


def test_canonical_eur_brl_routes_and_receipt():
    result = simulate_payment()
    assert result["decision"] == Decision.ROUTE
    assert result["receipt"]["reconciliation"] == "MATCHED"
    assert all(
        result["receipt"][k] for k in ("authorized", "executed", "settled", "reconciled", "assured")
    )
    assert result["receipt"]["treasury_impact"]["capital_locked"] > 0


def test_concurrent_reservations_enforce_mandate_limit():
    ledger = SpendReservations(10_000)
    assert ledger.reserve("a", 4_000)
    assert ledger.reserve("b", 3_000)
    assert ledger.reserve("c", 2_500)
    assert ledger.available == 500
    assert not ledger.reserve("d", 1_000)


def test_stale_fx_abstains_when_all_candidate_quotes_expired():
    stale = [r for r in ROUTES if r.fx_rate == 5.45]
    from dataclasses import replace

    result = evaluate_routes(
        sample_intent(),
        routes=[replace(r, fx_expires_at="2026-10-26T11:59:00+00:00") for r in stale],
        now=NOW,
    )
    assert result["decision"] == Decision.ABSTAIN
    assert all("STALE_FX" in r["rejection_reasons"] for r in result["routes"])


def test_beneficiary_substitution_is_hard_rejection():
    result = evaluate_routes(sample_intent(beneficiary_id="unexpected"), now=NOW)
    assert result["decision"] == Decision.NO_GO
    assert all("BENEFICIARY_NOT_ALLOWED" in r["rejection_reasons"] for r in result["routes"])


def test_insufficient_liquidity_blocks_route():
    from dataclasses import replace

    routes = [replace(r, available_liquidity=10) for r in ROUTES if r.fx_rate == 5.45]
    result = evaluate_routes(sample_intent(), routes=routes, now=NOW)
    assert result["decision"] == Decision.NO_GO
    assert all("INSUFFICIENT_LIQUIDITY" in r["rejection_reasons"] for r in result["routes"])


def test_missing_compliance_evidence_abstains():
    from dataclasses import replace

    routes = [replace(r, compliance_status="MISSING") for r in ROUTES if r.fx_rate == 5.45]
    result = evaluate_routes(sample_intent(), routes=routes, now=NOW)
    assert result["decision"] == Decision.ABSTAIN


def test_corridor_unit_economics_and_monte_carlo_are_deterministic():
    assert corridor_model(10_000_000, 60, 35)["contribution_margin"] == 25_000
    assert monte_carlo_cost(300, 0.01) == monte_carlo_cost(300, 0.01)


from payflow.analysis import liquidity_sensitivity, reconcile


def test_sensitivity_is_deterministic_and_explainable():
    output = liquidity_sensitivity(sample_intent())
    assert [row["liquidity_cost_bps"] for row in output] == [0, 10, 20, 30, 40]
    assert all("recommended_route" in row for row in output)


def test_reconciliation_detects_beneficiary_and_amount_mismatch():
    expected = {
        "payment_id": "p1",
        "beneficiary_id": "b1",
        "amount": 10,
        "currency": "BRL",
        "route_id": "r1",
    }
    actual = {**expected, "beneficiary_id": "b2", "amount": 9}
    assert reconcile(expected, actual) == {
        "status": "MISMATCH",
        "mismatches": ["beneficiary_id", "amount"],
    }
