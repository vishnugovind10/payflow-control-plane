"""Protocol-neutral example adapter: translate an MPP-like paid-resource request."""

from payflow.domain import PaymentIntent


def to_intent(request: dict) -> PaymentIntent:
    return PaymentIntent(
        id=request["payment_id"],
        payer_id=request["principal_id"],
        agent_id=request.get("agent_id"),
        beneficiary_id=request["merchant_id"],
        amount=float(request["amount"]),
        source_currency=request["currency"],
        destination_currency=request.get("destination_currency", request["currency"]),
        source_country=request.get("source_country", "US"),
        destination_country=request.get("destination_country", "US"),
        payment_type="AGENTIC_PAYMENT",
        purpose=request.get("resource", "machine payment"),
        deadline_seconds=int(request.get("deadline_seconds", 60)),
    )
