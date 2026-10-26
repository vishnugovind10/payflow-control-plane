"""Protocol-neutral example adapter: normalize an x402-like payment payload."""

from payflow.domain import PaymentIntent


def to_intent(payload: dict) -> PaymentIntent:
    return PaymentIntent(
        id=payload["paymentId"],
        payer_id=payload["payer"],
        agent_id=payload.get("agent"),
        beneficiary_id=payload["payTo"],
        amount=float(payload["amount"]),
        source_currency=payload["asset"],
        destination_currency=payload.get("destinationCurrency", payload["asset"]),
        source_country=payload.get("sourceCountry", "US"),
        destination_country=payload.get("destinationCountry", "US"),
        payment_type="AGENTIC_PAYMENT",
        purpose=payload.get("resource", "HTTP 402 resource"),
        deadline_seconds=int(payload.get("deadlineSeconds", 60)),
    )
