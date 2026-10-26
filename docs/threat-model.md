# Threat model and public demo boundary

The demo has no credentials, custody, external RPC, customer data or live provider connections. Its principal risks are incorrect assumptions in illustrative economics, misuse of fixture outputs as quotes, and confusion between simulated and actual execution. The UI and API label the environment synthetic and explicitly indicate that no live rail is connected.

A production system would need authenticated principals, signed/immutable mandates, replay protection, idempotency, concurrent transactional reservation storage, evidence provenance and expiry, access control, key management, privacy controls, provider isolation, settlement finality rules, operational monitoring and independent security review. None is claimed here.
