# Deepening

Use this branch when dependency shape changes the seam, substitute, test migration, or validation strategy.

[SKILL.md](SKILL.md) owns vocabulary and taste gates. [DIRECT-DESIGN.md](DIRECT-DESIGN.md) owns Source Trace, the direct pass, and final design packet. This file owns dependency classification, seam discipline, adapter strategy, coverage parity, and the bounded migration.

Cluster -> dependency category -> real seam -> coverage parity -> bounded migration.

## Contents

- [Process](#process)
- [Deepening Packet](#deepening-packet)
- [Dependency Categories](#dependency-categories)
- [Seam Discipline](#seam-discipline)
- [Testing Strategy](#testing-strategy-replace-dont-layer)
- [Completion Criteria](#completion-criteria)

## Process

1. Name the shallow cluster and spread behavior or decision.
2. Name the deeper module and caller-facing interface.
3. Classify every dependency behind or across the seam.
4. Choose the narrowest real seam and adapter or substitute strategy.
5. Establish coverage parity through the deeper interface.
6. Classify each old test as add, rewrite, keep, or delete.
7. Name the migration and validation proof.
8. Stop at the bounded-slice edge.

## Deepening Packet

Contribute these fields to the parent design packet:

- shallow cluster and spread behavior;
- deeper module and interface;
- every dependency category;
- seam, adapters, and substitutes;
- tests to add, rewrite, keep, or delete;
- coverage-parity evidence;
- bounded migration path;
- validation command or proof;
- stop boundary and follow-ups.

## Dependency Categories

Classify dependencies by what they need from tests and runtime.

### 1. In-Process

Pure computation and in-memory state need no adapter. Move the decision into the module that owns it and prove behavior through the deeper interface.

Use focused internal tests only for dense rules that are independently meaningful.

### 2. Local-Substitutable

Dependencies with realistic local substitutes: in-memory stores, isolated `.tmp/` filesystems, local service emulators, SQLite/PGLite, fake clocks, or deterministic queues.

Keep the deeper module's external interface small and test it with the local substitute. Add dependency injection to the external contract only when the dependency is a real caller concern or keeps I/O at the edge.

Behavior proof:

```python
store = create_test_store(
    inventory=[{"sku": "COURSE-TS", "available": 2}]
)

receipt = checkout.place_order(
    store=store,
    cart=cart_with_item("COURSE-TS"),
    payment_adapter=FakePaymentAdapter(status="paid"),
)

assert receipt.status == "confirmed"
assert store.inventory.available("COURSE-TS") == 1
```

The test proves checkout behavior through the checkout interface while using a local store substitute. Inspecting `store.inventory` is fixture inspection rather than a caller-facing production interface.

Call-sequence wiring:

```python
checkout = Checkout(
    inventory_reader=MockInventoryReader(),
    inventory_writer=MockInventoryWriter(),
    order_writer=MockOrderWriter(),
    event_writer=MockEventWriter(),
)
```

This exposes implementation seams and turns the test into wiring verification.

Validation: run behavior tests through the deeper interface using the local substitute. Keep separate substitute tests only when the substitute has meaningful contract risk.

### 3. Remote But Owned

Your own services across a network boundary: internal APIs, queues, workers, or microservices.

Define an interface at the seam where transport varies. Keep domain logic in the deep module. Production uses an HTTP, gRPC, or queue adapter; tests use an in-memory or fake adapter.

Recommendation shape:

> Define an interface at the shipment quote seam. Keep quote selection and fallback behavior in the shipping module. Use an HTTP adapter for production and an in-memory adapter for tests, so transport varies but the domain decision stays local.

The seam is real because production and tests use different adapters, and the owned remote service can be represented locally.

Validation: prove domain behavior through the deep module with a fake adapter. Add production-adapter contract checks when the remote contract carries meaningful risk.

### 4. True External

Third-party systems outside your control: payments, email, SMS, carrier APIs, hosted LLMs, analytics, or external identity providers.

Place an adapter seam at the external dependency. The deep module owns domain behavior; the adapter owns third-party request and response translation.

Use the smallest test double that proves the risk:

- **Fake** for realistic external outcomes that drive domain behavior.
- **Stub** for one fixed external response.
- **Mock** for an adapter call contract that is itself the behavior or risk.

Adapter contract proof:

```python
def test_stripe_adapter_sends_authorized_amount(stripe_client):
    adapter = StripePaymentAdapter(stripe_client)

    adapter.authorize(order_id="order_123", amount=Decimal("25.00"), currency="USD")

    stripe_client.PaymentIntent.create.assert_called_once_with(
        amount=2500,
        currency="usd",
        metadata={"order_id": "order_123"},
    )
```

Keep vendor translation inside the adapter and domain decisions inside the deep module.

Validation: pair domain behavior tests with adapter contract tests when both risks exist. Use live smoke tests only when the repo already supports them safely.

## Seam Discipline

A seam earns its place through locality, dependency isolation, domain ownership, or real variation.

- Keep dependency injection at a caller-facing contract or I/O edge that genuinely varies.
- Treat production plus a fake, local substitute, emulator, or second integration as evidence of a real seam.
- Keep internal seams inside the implementation.
- Test an internal module directly only when it owns independently meaningful behavior.
- Treat a patch point requested only by tests as interface pressure, then redesign the caller-facing surface.

## Testing Strategy: Replace, Don't Layer

Establish **coverage parity** before removing shallow tests.

- Add behavior tests through the deeper interface first.
- Rewrite tests whose behavior matters but whose surface is obsolete.
- Keep tests for dense rules, adapter contracts, regression cases, or behavior not yet covered through the deeper interface.
- Delete tests that assert only pass-through calls, internal ordering, or behavior now proved better through the deeper interface.
- Assert observable outcomes through the same interface callers use.

A test that changes only because implementation changed is testing past the interface.

## Completion Criteria

Complete only when every dependency is classified; seam, adapter, and substitute choices match those categories; the proposed interface is smaller and useful; coverage parity accounts for every affected test; validation proof is named; the migration fits the bounded slice; and the next move beyond that boundary is recorded as a follow-up.
