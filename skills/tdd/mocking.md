# Mocking And Boundaries

This skill is classicist by default: prefer real in-process code and local substitutes. Use fakes, stubs, or mocks only at a real **seam**, usually through an **adapter**.

Do not mock owned modules behind the interface you are testing. If testing through the public interface is painful, treat that as design feedback: the interface may be too shallow, too coupled, or at the wrong seam.

Prefer this order:

1. Real in-process code.
2. Local substitute: in-memory store, temp filesystem, test database, or local service emulator.
3. Fake adapter that preserves the behavior needed by the test.
4. Stub for one controlled value or response.
5. Mock adapter for a true external system when the call contract itself is the behavior or risk.

Use test doubles for:

- third-party APIs
- time
- randomness
- network
- email
- payments
- filesystem or database only when no local substitute is practical

Do not mock:

- owned modules
- private helpers
- internal collaborators
- the behavior under test

## Fake, Stub, Or Mock

Use the smallest test double that preserves the behavior you need.

- **Fake**: working local implementation of an adapter, such as an in-memory payment adapter or repository.
- **Stub**: fixed response for one scenario, such as a clock returning a known time.
- **Mock**: interaction assertion against an adapter call.

Prefer fakes when the test is proving domain behavior. Use mocks only when the adapter's request or interaction contract is the thing being proven.

## Good Boundary Fake

```python
class FakePaymentAdapter:
    def __init__(self):
        self.charges = []

    def charge(self, *, order_id, amount, currency):
        self.charges.append(
            {"order_id": order_id, "amount": amount, "currency": currency}
        )
        return {"status": "paid", "transaction_id": "txn_test"}


def test_paid_order_is_confirmed():
    payments = FakePaymentAdapter()

    result = place_order(
        cart=cart_with_one_item(price=25),
        payment_adapter=payments,
    )

    assert result.status == "confirmed"
    assert result.payment.transaction_id == "txn_test"
```

Why this is good:

- The fake sits at the payment seam.
- The order behavior is real.
- The fake preserves the adapter behavior the test needs.
- The test asserts the observable order outcome, not just that `charge` was called.

## Acceptable Mock Assertion

Mock call assertions are implementation-coupled unless the interaction crosses a real system seam. Use them only when the adapter contract itself is the risk being proven.

```python
def test_payment_adapter_receives_the_order_id_and_authorized_amount(mocker):
    payment_adapter = mocker.Mock()
    payment_adapter.charge.return_value = {
        "status": "paid",
        "transaction_id": "txn_test",
    }

    place_order(
        cart=cart_with_one_item(price=25),
        payment_adapter=payment_adapter,
    )

    payment_adapter.charge.assert_called_once_with(
        order_id=mocker.ANY,
        amount=25,
        currency="USD",
    )
```

This is acceptable only if the payment seam's request contract is the behavior under test. Otherwise, prefer asserting the resulting order behavior.

## Bad Mocked Internal Collaborator

```python
def test_checkout_calls_inventory_reserver(mocker):
    reserve_inventory = mocker.patch("orders.reserve_inventory")

    checkout(cart_with_one_item())

    reserve_inventory.assert_called_once()
```

This is bad because `reserve_inventory` is owned code behind the checkout interface. The test couples to implementation and can fail during a harmless refactor.

## Better Behavior Test

```python
def test_checkout_reserves_inventory_for_confirmed_order():
    store = create_test_store(
        inventory=[{"sku": "COURSE-TS", "available": 2}]
    )

    result = checkout(store, cart_with_item("COURSE-TS"))

    assert result.status == "confirmed"
    assert get_inventory(store, "COURSE-TS").available == 1
```

This proves the behavior through the checkout interface. The inventory reserver remains an implementation detail.

## Mocking Checklist

Before adding a fake, stub, or mock, answer:

- What seam is this test double replacing?
- Is the dependency truly external, slow, flaky, nondeterministic, or unsafe to call?
- What behavior from the real dependency does this test rely on?
- Would real in-process code or a local substitute be clearer?
- Does the fake, stub, or mock response match the real contract closely enough?
- Would this test still matter if the implementation behind the interface changed?

If you cannot answer these, run the test with the real dependency or a local substitute first.

## Anti-Patterns

### Mocking Owned Modules

Do not mock owned modules for convenience. Test through the interface that owns the behavior.

### Testing Mock Existence

Do not assert that a mocked child, fake element, or placeholder exists unless that placeholder is product behavior.

### Test-Only Production Methods

Do not add methods, flags, or visibility to production modules solely for tests. Put setup, cleanup, and inspection in test utilities unless they are real public interface behavior.

### Mocking Without Understanding

Do not mock a high-level method before understanding what behavior it hides. Mock the external operation, not the owned behavior.

### Incomplete Test Doubles

Fake, stub, and mock responses should match the real contract, including fields downstream code may consume.

### Over-Complex Test Doubles

If test-double setup is longer than the behavior being tested, reconsider the seam. A higher-level integration test or a simpler interface may be better.
