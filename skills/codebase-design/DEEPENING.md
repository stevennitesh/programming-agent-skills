# Deepening

Deepen a cluster of shallow modules safely once dependency shape matters.

Use this with [SKILL.md](SKILL.md). `SKILL.md` defines the vocabulary and taste: **module**, **interface**, **implementation**, **depth**, **seam**, **adapter**, **leverage**, and **locality**. This file explains how dependency shape changes the deepening move and the validation strategy.

A deepening move should increase **depth**, **leverage**, or **locality** without widening the current bounded slice. If the move is behavior-preserving but unlocks later tracer bullets, treat it as a support slice.

## Process

1. Name the shallow cluster and the behavior or decision currently spread across it.
2. Name the deeper module and the interface callers should use.
3. Classify each dependency behind or across the seam.
4. Choose the narrowest seam and adapter/substitute strategy that proves the behavior.
5. Move tests toward the deeper interface with coverage parity.
6. Keep, rewrite, or delete old tests based on what behavior they still prove.

A good deepening recommendation includes:

- current shallow shape
- proposed deeper module
- interface contract
- dependency category
- seam placement
- adapter or local substitute strategy
- tests to add, rewrite, keep, or delete
- migration path
- validation command or proof

## Dependency Categories

Classify dependencies by what they need from tests and runtime.

### 1. In-Process

Pure computation, in-memory state, no I/O.

Best move: merge shallow modules or move the decision into the module that owns the domain concept. No adapter is needed.

Test through the deeper module's interface.

Good:

```python
total = price_cart(cart, discounts=discounts, tax_region=customer.region)
```

The pricing module owns line totals, discounts, taxability, rounding, and currency rules.

Bad:

```python
line_total = calculate_line_total(line)
discounted = apply_discount(line_total, discount)
tax = calculate_tax(discounted, customer.region)
total = add_tax(discounted, tax)
```

This may be fine inside the pricing implementation. It is shallow when every caller must know the sequence.

Validation: behavior tests through the deeper interface, plus focused module tests only for dense rules that are real behavior in their own right.

### 2. Local-Substitutable

Dependencies with realistic local substitutes: in-memory stores, temp filesystems, local service emulators, SQLite/PGLite, fake clocks, or deterministic queues.

Best move: keep the deeper module's external interface small and test it with the local substitute. Do not expose extra seams just so the substitute can be injected unless injecting that dependency is part of the real module contract or keeps I/O at the edge.

Good:

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

The test proves checkout behavior through the checkout interface while using a local store substitute. Inspecting `store.inventory` is test fixture inspection, not a caller-facing production interface.

Bad:

```python
checkout = Checkout(
    inventory_reader=MockInventoryReader(),
    inventory_writer=MockInventoryWriter(),
    order_writer=MockOrderWriter(),
    event_writer=MockEventWriter(),
)
```

This exposes implementation seams and turns the test into call-sequence wiring.

Validation: run behavior tests through the deeper interface using the local substitute. Keep separate substitute tests only when the substitute has meaningful contract risk.

### 3. Remote But Owned

Your own services across a network boundary: internal APIs, queues, workers, or microservices.

Best move: define an interface at the seam where transport varies. Keep domain logic in the deep module. Production uses an HTTP/gRPC/queue adapter. Tests use an in-memory or fake adapter.

Recommendation shape:

> Define an interface at the shipment quote seam. Keep quote selection and fallback behavior in the shipping module. Use an HTTP adapter for production and an in-memory adapter for tests, so transport varies but the domain decision stays local.

Good:

```python
class QuoteGateway(Protocol):
    def quote(self, request: QuoteRequest) -> QuoteResponse:
        ...


class HttpQuoteGateway:
    ...


class FakeQuoteGateway:
    ...


quote = shipping.quote(
    parcel=parcel,
    destination=destination,
    gateway=FakeQuoteGateway([express_quote, economy_quote]),
)
```

The seam is real because production and tests use different adapters, and the owned remote service can be represented locally.

Validation: behavior tests through the deep module with a fake adapter, plus contract checks for the production adapter when the remote contract is risky. Contract checks do not replace behavior tests.

### 4. True External

Third-party systems you do not control: payments, email, SMS, carrier APIs, hosted LLMs, analytics, or external identity providers.

Best move: put an adapter seam at the external dependency. The deep module owns domain behavior. The adapter owns third-party request/response translation.

Use the smallest test double that proves the behavior:

- **Fake** when domain behavior needs realistic external outcomes.
- **Stub** when one fixed external response is enough.
- **Mock** only when the adapter call contract itself is the behavior or risk.

Good domain behavior test:

```python
payments = FakePaymentAdapter(
    result=PaymentResult(status="paid", transaction_id="txn_123")
)

receipt = checkout.place_order(
    cart=cart_with_item("COURSE-TS"),
    payment_adapter=payments,
)

assert receipt.status == "confirmed"
assert receipt.transaction_id == "txn_123"
```

Good adapter contract test:

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

This test belongs around the Stripe adapter. It is acceptable because the request contract to Stripe is the behavior under test.

Bad:

```python
def test_checkout_calls_stripe(mocker):
    stripe_charge = mocker.patch("stripe.PaymentIntent.create")

    checkout.place_order(cart_with_item("COURSE-TS"))

    stripe_charge.assert_called_once()
```

This leaks the external vendor call into checkout behavior. Checkout should depend on a payment adapter, not Stripe directly.

Validation: behavior tests through the deep module with fake/stub adapters, adapter contract tests around third-party translation, and live smoke tests only when the repo already supports them safely.

## Seam Discipline

A seam is a real design point, not a test hook.

Introduce or keep a seam when it improves **locality**, isolates a real dependency, captures domain ownership, or supports real variation.

Do not introduce a seam only because a test wants to patch something.

One adapter usually means a hypothetical seam. Two adapters usually means a real seam: production plus fake, local substitute, emulator, in-memory adapter, or a second production integration.

Internal seams are real design seams inside the implementation. Do not expose them through the external interface, and do not create private hooks just for tests. Test an internal module directly only when it owns behavior worth specifying in its own right.

## Testing Strategy: Replace, Don't Layer

Move tests toward the deeper interface.

Do not keep old shallow-module tests just because they exist. Do not delete them blindly either.

Use coverage parity:

- Add behavior tests through the deeper interface first.
- Rewrite old tests when they describe behavior that still matters but through the wrong surface.
- Keep old tests when they cover dense rules, adapter contracts, regression cases, or behavior not yet covered through the deeper interface.
- Delete old tests when they only assert implementation details, pass-through calls, or behavior now covered better through the deeper interface.

Tests should assert observable outcomes through the interface, not internal state or call order.

If a test must change when implementation changes but behavior does not, it is testing past the interface.

## Stop Conditions

Stop deepening when the deeper module has a smaller useful interface, behavior is proven through that interface, and the next move would widen the bounded slice.

If the next improvement needs a different dependency category, migration step, or product behavior, record it as a follow-up support slice or tracer bullet.
