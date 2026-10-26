import json

from .domain import corridor_model, evaluate_routes, sample_intent, simulate_payment


def scenarios():
    intents = [
        sample_intent(),
        sample_intent(
            id="pay_merchant_001",
            amount=250_000,
            source_currency="USD",
            payment_type="MERCHANT_SETTLEMENT",
            deadline_seconds=3600,
        ),
        sample_intent(
            id="pay_remit_001",
            amount=1_000,
            source_currency="USD",
            destination_currency="MXN",
            destination_country="MX",
            payment_type="REMITTANCE",
            deadline_seconds=900,
        ),
        sample_intent(
            id="pay_agent_001", amount=2_500, payment_type="AGENTIC_PAYMENT", deadline_seconds=300
        ),
    ]
    return [
        evaluate_routes(
            i,
            now=__import__("datetime").datetime(
                2026, 10, 26, 12, tzinfo=__import__("datetime").timezone.utc
            ),
        )
        for i in intents
    ]


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Run deterministic PayFlow synthetic payment demos"
    )
    parser.add_argument(
        "command", choices=["demo", "evaluate", "economics"], nargs="?", default="demo"
    )
    parser.add_argument("--amount", type=float, default=100_000)
    args = parser.parse_args()
    if args.command == "demo":
        result = simulate_payment()
    elif args.command == "economics":
        result = [corridor_model(v, 60, 35) for v in (10_000_000, 50_000_000, 100_000_000)]
    else:
        result = evaluate_routes(
            sample_intent(amount=args.amount),
            now=__import__("datetime").datetime(
                2026, 10, 26, 12, tzinfo=__import__("datetime").timezone.utc
            ),
        )
    print(json.dumps(result, default=str, indent=2))


if __name__ == "__main__":
    main()
