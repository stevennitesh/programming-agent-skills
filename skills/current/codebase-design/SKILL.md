---
name: codebase-design
description: Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
---

# Codebase Design

Design **deep modules**: lots of behavior behind a small interface, placed at a clean seam, testable through that interface.

Use this vocabulary wherever code is being designed, reviewed, tested, or restructured. The aim is **leverage** for callers, **locality** for maintainers, and testability through real interfaces.

## Glossary

Use these terms consistently. Prefer established repo/domain vocabulary where it exists, and map it back to these concepts instead of renaming the repo.

**Module** - anything with an interface and an implementation. Scale-agnostic: a function, class, package, workflow, or tier-spanning slice. Avoid: unit, component, service.

**Interface** - everything a caller must know to use the module correctly: type signature, invariants, ordering constraints, error modes, required configuration, performance characteristics, and behavior contract. Avoid: API, signature.

**Implementation** - what sits inside a module. Use **adapter** when the seam is the topic; use implementation otherwise.

**Depth** - leverage at the interface: how much behavior callers and tests can exercise per unit of interface they must understand. A module is **deep** when a lot of behavior sits behind a small interface. It is **shallow** when the interface is nearly as complex as the implementation.

**Seam** - a place where behavior can vary without editing the caller. It is where a module's interface lives. Seam placement is a design decision. Avoid: boundary.

**Adapter** - a concrete implementation that satisfies an interface at a seam. It describes the role a thing fills, not how complex it is inside.

**Leverage** - what callers get from depth: more capability per unit of interface learned.

**Locality** - what maintainers get from depth: change, bugs, knowledge, and verification concentrate in one place.

## Deep vs Shallow

A deep module has a small interface with meaningful behavior behind it:

```python
receipt = checkout.place_order(cart_id, payment_method)
```

The caller learns one operation. Pricing, tax, inventory reservation, payment authorization, order state transitions, receipt creation, and event publishing can live behind the interface.

A shallow caller interface exposes almost as much complexity as it hides:

```python
cart = carts.get(cart_id)
price = pricing.calculate(cart)
tax = taxes.calculate(cart, price)
reservation = inventory.reserve(cart.items)
payment = payments.authorize(payment_method, price + tax)
order = orders.create(cart, price, tax, reservation, payment)
events.publish(OrderPlaced(order.id))
receipt = receipts.create(order)
```

That sequence may be fine inside the implementation. It is a poor interface when every caller must know the workflow.

When designing an interface, ask:

- Can callers learn less?
- Can parameters get simpler?
- Can more behavior move behind the interface?
- Can decisions concentrate in the module that owns them?
- Can tests prove behavior through the same surface callers use?

## Principles

### Depth Is A Property Of The Interface

A deep module is not deep because it has many lines of code. It is deep because callers get a lot of behavior from a small surface.

Shallow extraction:

```python
def calculate_line_total(quantity, unit_price):
    return quantity * unit_price


def calculate_cart_total(lines):
    return sum(calculate_line_total(line.quantity, line.unit_price) for line in lines)
```

This may be fine as private implementation. It is not an architectural seam if callers now have to understand both functions.

Deeper interface:

```python
total = price_cart(cart, discounts=active_discounts, tax_region=customer.region)
```

The pricing module can own line totals, discounts, taxability, rounding, and currency rules. Callers learn one behavior-oriented interface.

### Internal Seams Must Be Real

A deep module may contain smaller internal modules, but those internal modules are not part of its external interface.

Internal seams must earn their place through locality, dependency isolation, domain ownership, or real variation. Do not create private seams, flags, methods, or visibility solely for tests.

Test through the deep module's external interface by default. Test an internal module directly only when it is a real module with behavior worth specifying in its own right.

### The Deletion Test

Imagine deleting the module.

If complexity vanishes, it was probably pass-through:

```python
def get_user_name(user):
    return user.name
```

If complexity reappears across callers, tests, or workflows, the module is earning its keep:

```python
quote = shipping.quote(parcel, destination, service_level="express")
```

Deleting `shipping.quote` would spread dimensional weight, carrier rules, delivery windows, restrictions, and fallback behavior across callers.

### The Interface Is The Test Surface

Callers and tests should cross the same seam.

Good:

```python
def test_checkout_confirms_paid_order():
    payments = FakePaymentAdapter(status="paid", transaction_id="txn_123")

    receipt = checkout.place_order(
        cart=cart_with_item("COURSE-TS"),
        payment_adapter=payments,
    )

    assert receipt.status == "confirmed"
    assert receipt.transaction_id == "txn_123"
```

Bad:

```python
def test_checkout_calls_inventory_reserver(mocker):
    reserve_inventory = mocker.patch("checkout.reserve_inventory")

    checkout.place_order(cart_with_item("COURSE-TS"))

    reserve_inventory.assert_called_once()
```

The bad test checks an implementation call sequence. A harmless refactor can break it while behavior stays correct.

If behavior is painful to test through the interface, treat that as design feedback: the interface may be too shallow, too coupled, or at the wrong seam.

### One Adapter Means A Hypothetical Seam

Do not introduce an interface at a seam unless behavior genuinely varies across it.

A seam is often real when production uses an external adapter and tests use a local fake:

```python
from typing import Protocol


class PaymentAdapter(Protocol):
    def authorize(self, *, order_id: str, amount: Decimal, currency: str) -> Payment:
        ...


class StripePaymentAdapter:
    ...


class FakePaymentAdapter:
    ...
```

A single pass-through adapter is usually indirection.

### Deepening Is Not Abstraction For Its Own Sake

Sometimes the right move is to merge modules, delete a pass-through layer, inline a helper, or keep code boring.

Do not turn this:

```python
receipt = checkout.place_order(cart_id, payment_method)
```

into this:

```python
receipt = checkout_orchestrator_factory.create().execute(
    PlaceOrderCommand(cart_id=cart_id, payment_method=payment_method)
)
```

unless the extra structure buys real leverage, locality, dependency isolation, or testability.

## Applying The Skill

When designing or improving code:

1. Read the relevant repo/domain docs when present.
2. Identify the current module, interface, implementation, seams, and adapters.
3. Inspect callers and tests to see what the interface makes easy or painful.
4. Run the deletion test.
5. Propose the deeper shape: module, interface contract, seam placement, adapters, validation, migration path, and risks.
6. Keep deepening inside the current bounded slice. If the design work is behavior-preserving but unlocks later tracer bullets, make it a support slice.

A good recommendation names:

- the current shallow shape
- the proposed deeper module
- the interface callers would use
- what behavior moves behind the interface
- where the seam lives
- which adapters are real
- how tests prove behavior through the interface
- what migration can happen without widening scope

## Designing For Testability

Good interfaces make testing natural.

Prefer:

```python
receipt = checkout.place_order(cart_id, payment_method)

assert receipt.status == "confirmed"
```

Avoid:

```python
assert checkout._calculate_tax(cart) == Decimal("4.20")
assert checkout._reserve_inventory.called
```

Design moves that improve testability:

- Accept dependencies instead of creating hard-coded external clients.
- Return observable results instead of hiding all outcomes in side effects.
- Put branching decisions in the module that owns the domain concept.
- Use fakes or local substitutes at real seams.
- Keep setup, cleanup, and inspection in test utilities unless they are real public behavior.

Do not mock owned modules behind the interface under test. Mock, fake, or stub adapters at system boundaries.

## Relationships

- A **module** presents an **interface**: the surface callers and tests use.
- **Depth** is measured against that interface.
- A **seam** is where an interface lives.
- An **adapter** satisfies an interface at a seam.
- **Depth** produces **leverage** for callers and **locality** for maintainers.

## Rejected Framings

- **Depth as implementation-lines divided by interface-lines**: rewards padding. Use depth-as-leverage.
- **Interface as only a TypeScript `interface` or public methods**: too narrow. Interface includes every fact a caller must know.
- **Boundary**: overloaded with DDD bounded context. Say **seam** or **interface**.
- **Abstraction as default good**: false. Indirection must earn its keep.
- **Testability through private hooks**: false. The interface is the test surface.

## Going deeper

- **Deepening a cluster given its dependencies** - see [DEEPENING.md](DEEPENING.md): dependency categories, seam discipline, and replace-don't-layer testing.
- **Exploring alternative interfaces** - see [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md): compare several different interfaces, using subagents only when the user explicitly asks for subagents, delegation, or parallel agent work.
