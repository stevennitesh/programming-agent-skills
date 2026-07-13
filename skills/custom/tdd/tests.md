# Test Taste

Use these contrasts when test shape, oracle, or seam remains unclear. Prove behavior through the highest useful public **interface** or **seam**.

## Test Shape

1. Arrange meaningful domain state.
2. Act through the public interface or seam.
3. Assert observable outcomes from an independent oracle.

One test may have several assertions when they observe one outcome. Split unrelated outcomes.

## Tracer Bullet

```python
def test_confirmed_order_reserves_inventory_and_exposes_receipt():
    store = create_test_store(inventory={"COURSE-TS": 2})

    result = place_order(store, sku="COURSE-TS", quantity=1)

    assert result.status == "confirmed"
    assert result.receipt.items == [{"sku": "COURSE-TS", "quantity": 1}]
    assert get_inventory(store, "COURSE-TS") == 1
```

This crosses one public interface and proves one vertical outcome. It does not allocate separate tests to pricing, reservation, persistence, and receipt helpers.

## Behavioral RED

Apply the bug ownership gate in [SKILL.md](SKILL.md) before using a regression test.

Good RED proves missing behavior:

```text
Expected {'status': 'rejected', 'reason': 'email-required'}, got {'status': 'created'}
```

Setup failure is not RED:

```text
ModuleNotFoundError: No module named 'tests.fixtures.account'
```

Repair setup before changing production behavior.

## Public Behavior

Private implementation:

```python
def test_normalize_email_lowercases_input():
    assert _normalize_email("A@EXAMPLE.COM") == "a@example.com"
```

Caller-visible behavior:

```python
def test_registered_accounts_use_canonical_email_addresses():
    account = register_account(email="A@EXAMPLE.COM")

    assert sign_in(email="a@example.com").account_id == account.id
```

A focused module test is appropriate when the module exposes a stable behavioral contract; test through that contract, not its private helpers.

## Independent Oracle

Tautology:

```python
expected = sum(line["price"] for line in lines)
assert calculate_total(lines) == expected
```

Independent expectation:

```python
assert calculate_total([{"price": 10}, {"price": 5}]) == 15
```

Derive expectations from the specification, a known-good literal, a fixture, or a worked result rather than repeating the implementation.

## Names And Red Flags

Use domain behavior names such as `test_confirmed_order_reserves_inventory`. Treat these as pressure to redesign the test:

- the name describes calls, helpers, layers, or storage;
- a snapshot is the only oracle where semantic assertions are available;
- setup is larger than the behavior being proved;
- many data variants or horizontal-layer tests repeat one behavior.
