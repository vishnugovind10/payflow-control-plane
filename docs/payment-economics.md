# Payment economics

For each route, synthetic variable cost includes FX, provider, liquidity and off-ramp basis-point charges, fixed network fee, expected failure loss and time-scaled capital cost. Contribution is modeled customer revenue at an illustrative 60 bps take rate less modeled route cost. `corridor_model` provides an independent monthly venture view: volume × take rate minus variable cost and optional fixed monthly cost, with contribution margin and contribution per $1m volume. The figures are educational fixtures and do not represent quotes, realized revenue, or a commercial forecast.

`monte_carlo_cost` uses a fixed seed by default for reproducibility. It varies base cost by a bounded uniform fee factor and models a simple failure-cost shock; it is a demonstration harness, not a calibrated risk model.
