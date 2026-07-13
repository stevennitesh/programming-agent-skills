# Test Examples

Use these examples to calibrate test taste while running `$tdd`: behavior through the highest useful public **interface** or **seam**, not implementation shape.

A good test reads like a specification. It proves something a caller or user can observe. It should survive refactors that preserve behavior.

One behavior can have several assertions when they are observations of the same outcome. If the test name needs "and" to join unrelated outcomes, split it.

## Good Test Shape

1. Arrange meaningful domain state.
2. Act through the public interface or seam.
3. Assert observable outcomes.
4. Avoid private calls, helper names, internal order, and mock existence.

## Good Minimal Example

```python
def test_created_user_can_be_retrieved():
    user = create_user(name="Ada")

    retrieved = get_user(user.id)

    assert retrieved.name == "Ada"
```

This is good because it proves one observable behavior through the public interface without exposing storage, helper calls, or internal order.

## Good Feature Tracer Bullet

```python
def test_confirmed_order_reserves_inventory_and_exposes_receipt():
    store = create_test_store(
        inventory=[{"sku": "COURSE-TS", "available": 2}]
    )

    result = place_order(
        store,
        sku="COURSE-TS",
        quantity=1,
        payment_method=valid_payment_method(),
    )

    assert result.status == "confirmed"
    assert result.receipt.items == [{"sku": "COURSE-TS", "quantity": 1}]
    assert get_inventory(store, "COURSE-TS").available == 1
```

Why this is good:

- It crosses the public order interface.
- It proves caller-visible behavior end to end.
- It uses domain language: order, inventory, receipt.
- It does not assert which helper reserved inventory.
- The assertions are multiple observations of one confirmed order.

## Good Bug Regression Test

Apply the bug ownership gate in [SKILL.md](SKILL.md) before using this regression-test shape.

```python
def test_blank_email_is_rejected_before_account_creation():
    result = register_account(
        email="   ",
        password="correct-horse-battery-staple",
    )

    assert result == {
        "status": "rejected",
        "reason": "email-required",
    }
```

Run this before the fix. Good RED proves missing behavior:

```text
Expected {'status': 'rejected', 'reason': 'email-required'}, got {'status': 'created'}
```

Bad RED proves broken setup:

```text
ModuleNotFoundError: No module named 'tests.fixtures.account'
```

Fix broken setup before writing production code.

## Good Workflow Test

```python
def test_contact_import_reports_rejected_rows_without_writing_them(tmp_path):
    fixture = tmp_path / "contacts.csv"
    fixture.write_text(
        "email,name\n"
        "valid@example.com,Ada\n"
        "not-an-email,Grace\n"
    )

    result = run_cli(["contacts", "import", str(fixture)])

    assert result.exit_code == 1
    assert "1 imported" in result.stdout
    assert "1 rejected" in result.stderr
    assert list_contacts() == [
        {"email": "valid@example.com", "name": "Ada"}
    ]
```

Why this is good:

- It tests through the command interface.
- It proves visible import behavior.
- It avoids parser-helper coupling.
- It checks the durable contract: output, exit code, and stored result.

## Good Focused Module Test

Use a smaller test when dense logic needs more coverage than a tracer bullet should carry. Keep it behind a meaningful module interface.

```python
def test_volume_discount_applies_only_after_the_threshold_quantity():
    price = price_order(
        items=[{"sku": "COURSE-TS", "quantity": 10, "unit_price": 50}],
        discounts=[{"type": "volume", "threshold": 10, "percent_off": 20}],
    )

    assert price.total == 400
    assert price.applied_discounts == [{"type": "volume", "amount": 100}]
```

This is good because `price_order` is a meaningful pricing interface. The test proves pricing behavior without reaching into private calculation steps.

## Bad Private Helper Test

```python
def test_normalize_email_lowercases_input():
    assert _normalize_email("A@EXAMPLE.COM") == "a@example.com"
```

This is bad because it tests implementation instead of behavior. A refactor can break the test while preserving what callers need.

## Better Behavior Test

```python
def test_registered_accounts_use_canonical_email_addresses():
    account = register_account(
        email="A@EXAMPLE.COM",
        password="correct-horse-battery-staple",
    )

    signed_in = sign_in(email="a@example.com")

    assert signed_in.account_id == account.id
```

This proves the behavior callers care about: registration stores an address that can be used canonically later.

## Bad Layer Test

```python
def test_create_invoice_inserts_a_row_into_invoices_table(db):
    create_invoice(customer_id="cust_123", total=100)

    row = db.execute(
        "select * from invoices where customer_id = :customer_id",
        {"customer_id": "cust_123"},
    ).one()

    assert row.total == 100
```

This bypasses the public invoice interface to verify storage shape. It may be appropriate for a repository adapter contract, but it is a bad feature test.

## Better Interface Test

```python
def test_created_invoice_is_visible_in_the_customers_invoice_list():
    invoice = create_invoice(customer_id="cust_123", total=100)

    invoices = list_invoices_for_customer("cust_123")

    assert {
        "id": invoice.id,
        "total": 100,
        "status": "draft",
    } in invoices
```

This proves the behavior through the invoice interface. The database remains an implementation detail.

## Bad Tautological Test

```python
def test_calculate_total_sums_line_items():
    lines = [{"price": 10}, {"price": 5}]
    expected = sum(line["price"] for line in lines)

    assert calculate_total(lines) == expected
```

This is bad because the expected value is recomputed the same way as the implementation. It can pass even when the test teaches nothing.

## Better Independent Expectation

```python
def test_calculate_total_sums_line_items():
    assert calculate_total([{"price": 10}, {"price": 5}]) == 15
```

Use expected values from an independent source: the spec, a known-good literal, a fixture, or a worked example.

## Good Test Names

Good names describe behavior in domain language:

- `test_confirmed_order_reserves_inventory_and_exposes_receipt`
- `test_blank_email_is_rejected_before_account_creation`
- `test_paid_invoice_cannot_be_edited`
- `test_contact_import_reports_rejected_rows_without_writing_them`

Red flag names describe implementation:

- `test_calls_normalize_email`
- `test_uses_payment_service`
- `test_sets_is_valid_to_false`
- `test_renders_form_component`
- `test_saves_user_to_database`

Prefer names that a product owner, caller, or future maintainer would understand.

## Red Flags

- The test name says "calls", "invokes", "uses helper", or names an internal step.
- The assertion checks a private method, internal call count, or mock existence.
- The expected value is recomputed the same way as the implementation.
- A snapshot is the only oracle where specific semantic assertions are available.
- Tests are allocated per function or helper instead of per observable behavior.
- The test passes before production code changes.
- The setup is larger than the behavior being proven.
- Removing a mock changes the meaning of the test.
- The test breaks when behavior is unchanged but internals move.
- Many tests vary only data while proving the same behavior.
- A horizontal layer is tested instead of a vertical behavior.
