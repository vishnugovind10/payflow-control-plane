# Routing methodology

The scorer is deterministic and configurable by payment type. After the hard gates, each eligible candidate receives a weighted sum:

`score = w_cost*C + w_risk*R + w_liquidity*L + w_settlement*T + w_failure*F + w_capital*K + w_counterparty*P`

Lower scores rank first. Cost is normalized against 10% of payment principal; risk combines failure, counterparty and stablecoin exposure; liquidity reflects available liquidity relative to a 5x payment reference; settlement time is relative to deadline; capital is relative to principal. Components are capped to [0,1]. Payment-specific weights are visible in `WEIGHTS` in `src/payflow/domain.py` and sum to 1 for each built-in payment type.

This is an explainable illustrative ranking function, not calibrated market advice. Hard constraints always override score. Sensitivity helper `liquidity_sensitivity` sweeps liquidity cost assumptions to show route changes.
