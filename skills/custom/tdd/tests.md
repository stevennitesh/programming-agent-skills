# Test Taste

Use these contrasts when test shape, oracle, or seam remains unclear. Apply the
bug ownership gate in [SKILL.md](SKILL.md) before using a regression test.

## Tracer Bullet

Arrange meaningful domain state, act through the highest useful public interface
or seam, and prove one acceptance behavior from an independent oracle through
its observable effects. Several assertions may jointly prove that behavior.

```python
def test_confirmed_order_reserves_inventory_and_exposes_receipt():
    store = create_test_store(inventory={"COURSE-TS": 2})

    result = place_order(store, sku="COURSE-TS", quantity=1)

    assert result.status == "confirmed"
    assert result.receipt.items == [{"sku": "COURSE-TS", "quantity": 1}]
    assert get_inventory(store, "COURSE-TS") == 1
```

This proves one acceptance behavior through its observable effects rather than
splitting pricing, reservation, persistence, and receipt into horizontal tests.

## State And Behavior Verification

Prefer state verification through stable caller-facing behavior; use behavior
verification only when the interaction itself is contractual or provides
necessary failure isolation.

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

A focused module test is appropriate when the module exposes a stable behavioral
contract; test through that contract, not private helpers.

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

Trace expectations to a specification, known-good literal, fixture, or worked
result—not the implementation under test.

## Characterization Test

Use a characterization test only when actual legacy behavior must be recorded
while intended behavior is unavailable. It establishes actuality, not
correctness, cause, or a corrective RED. Keep it bounded to the behavior needed
for the current slice. When intended behavior is required to proceed, return
the unresolved decision through [SKILL.md](SKILL.md) instead of treating the
characterization test as TDD evidence.

## Property-Based Testing

Use property-based testing only when a stable property and independent oracle
range over a broad or combinatorial domain, credible generators and shrinking
exist, and generation discriminates better than examples or a small exhaustive
table. Define the valid input domain, property, generator constraints, and how
shrinking preserves valid cases. Otherwise prefer focused examples or an
exhaustive small table.

## Test Portfolio

Extend or parameterize an existing test when the same seam, oracle, and
outcome prove semantically equivalent inputs. Keep a separate test when it
owns a distinct behavior, Invariant, state or failure branch, risk, or useful
failure isolation.

```text
Weak:   one new test per ticket repeats the same setup, seam, and oracle
Strong: one behavior test or case table owns equivalent variants; distinct
        failure and lifecycle behavior stays independently diagnosable
```

Coverage and diagnostic clarity are floors. Test count is not a target.

## Red Flags

- the name describes calls, helpers, layers, or storage;
- the name records a ticket or change instead of durable behavior;
- a snapshot replaces available semantic assertions;
- setup is larger than the behavior being proved;
- semantically equivalent data variants repeat an already-proved behavior and
  oracle, horizontal-layer tests split one acceptance behavior, or expensive
  duplicate paths add no distinct proof responsibility.
