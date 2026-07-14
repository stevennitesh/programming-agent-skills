# Mocking And Boundaries

Prefer real in-process code. Put a test double only at a real boundary adapter.

Use this order:

1. Real in-process code.
2. Local substitute: in-memory store, isolated `.tmp/` filesystem, test database, or local emulator.
3. Fake adapter preserving required behavior.
4. Stub for one controlled value or response.
5. Mock adapter when the external call contract is itself the behavior or risk.

## Boundary Fake

```python
class FakePaymentAdapter:
    def charge(self, *, order_id, amount, currency):
        return {"status": "paid", "transaction_id": "txn_test"}


def test_paid_order_is_confirmed():
    result = place_order(
        cart=cart_with_one_item(price=25),
        payment_adapter=FakePaymentAdapter(),
    )

    assert result.status == "confirmed"
    assert result.payment.transaction_id == "txn_test"
```

The fake replaces the payment boundary while owned order behavior remains real. Assert an interaction only when the adapter request is the contract under test.

## Fidelity Gate

Before adding a double, establish:

- the real seam it replaces;
- why real code or a local substitute is insufficient;
- the dependency behavior and side effects the test needs;
- every consumed contract field;
- whether the test survives internal movement.

Reconsider the seam when fidelity is unclear or double setup overwhelms the behavior. Keep transport and provider shapes behind a narrow domain-facing adapter. Put test-only setup, cleanup, and inspection in test utilities—not production interfaces.
