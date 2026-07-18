# Test Taste

Use these contrasts when test shape, oracle, or seam remains unclear. Apply the bug ownership gate in [SKILL.md](SKILL.md) before using a regression test.

## Tracer Bullet

Arrange meaningful domain state, act through the highest useful public interface or seam, and prove one acceptance behavior from an independent oracle through its observable effects. Several assertions may jointly prove that behavior.

```python
def test_confirmed_order_reserves_inventory_and_exposes_receipt():
    store = create_test_store(inventory={"COURSE-TS": 2})

    result = place_order(store, sku="COURSE-TS", quantity=1)

    assert result.status == "confirmed"
    assert result.receipt.items == [{"sku": "COURSE-TS", "quantity": 1}]
    assert get_inventory(store, "COURSE-TS") == 1
```

This proves one acceptance behavior through its observable effects rather than splitting pricing, reservation, persistence, and receipt into horizontal tests.

## Public Behavior

Implementation-coupled:

```python
def test_normalize_email_lowercases_input():
    assert _normalize_email("A@EXAMPLE.COM") == "a@example.com"
```

Caller-visible:

```python
def test_registered_accounts_use_canonical_email_addresses():
    account = register_account(email="A@EXAMPLE.COM")

    assert sign_in(email="a@example.com").account_id == account.id
```

A focused module test is appropriate when the module exposes a stable behavioral contract; test through that contract, not private helpers.

## Independent Oracle

Implementation-derived:

```python
expected = sum(line["price"] for line in lines)
assert calculate_total(lines) == expected
```

Independent:

```python
assert calculate_total([{"price": 10}, {"price": 5}]) == 15
```

Trace expectations to a specification, known-good literal, fixture, or worked result—not the production implementation.

## Async Waiting

Wait for the observable condition or event with a bounded timeout and useful failure diagnostic.

```python
wait_for(
    lambda: job.status == "complete",
    timeout=5,
    description="job to complete",
)
```

Use elapsed delay only when time is the behavior. Observe the trigger first, derive the duration from the contract, and state why that duration proves it.

```python
wait_for(lambda: events.contains("DEBOUNCE_STARTED"), timeout=1)
advance_clock(DEBOUNCE_INTERVAL)
assert events.contains("SEARCH_REQUESTED")
```

## Red Flags

- the name describes calls, helpers, layers, or storage;
- a snapshot replaces available semantic assertions;
- setup is larger than the behavior being proved;
- semantically equivalent data variants repeat an already-proved behavior and oracle, or horizontal-layer tests split one acceptance behavior.
