# Agentic payments

The mandate bounds principal/agent authority by transaction size, cumulative usage, allowed currencies, corridors, beneficiaries, payment types, rails and expiry. `SpendReservations` atomically checks pending plus settled exposure against the mandate limit; successful settlement moves pending to settled, while failure can release a reservation. The API sample uses a static mandate fixture. Protocol adapters only normalize request fields into `PaymentIntent`; no MPP or x402 SDK or settlement provider is contacted.
