# Mocking And Boundaries

Prefer real in-process code and local substitutes. Put a test double at a real **seam**, usually through an **adapter**.

Use this order:

1. Real in-process code.
2. Local substitute: in-memory store, isolated `.tmp/` filesystem, test database, or local emulator.
3. Fake adapter preserving the behavior needed by the test.
4. Stub for one controlled value or response.
5. Mock adapter when a true external call contract is itself the behavior or risk.

Use the smallest double that preserves the contract:

- **Fake:** working local adapter implementation.
- **Stub:** fixed response for one scenario.
- **Mock:** interaction assertion at an external seam.

Inject a narrow, domain-facing adapter at an external seam. Keep transport machinery and provider shapes behind it.

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

The fake sits at the payment seam while the owned order behavior remains real. Mock a call only when the adapter request itself is the contract under test.

## Owned Behavior

Implementation coupling:

```python
reserve_inventory = mocker.patch("orders.reserve_inventory")
checkout(cart_with_one_item())
reserve_inventory.assert_called_once()
```

Behavior through the owning interface:

```python
store = create_test_store(inventory={"COURSE-TS": 2})

result = checkout(store, cart_with_item("COURSE-TS"))

assert result.status == "confirmed"
assert get_inventory(store, "COURSE-TS") == 1
```

Painful caller-facing tests are interface pressure: the interface may be shallow, coupled, or placed at the wrong seam.

## Checklist

Before adding a fake, stub, or mock, answer:

- What real seam does it replace?
- Why is real in-process code or a local substitute insufficient?
- Which behavior from the real dependency does the test rely on?
- Does the double match every consumed contract field?
- Would the test still matter if internals moved?

Reconsider the seam when contract fidelity is unclear or double setup overwhelms the behavior under test.
