# CONTEXT.md Format

`CONTEXT.md` is the project's glossary for resolved ubiquitous language.

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence definition of the term. Define what it is, not how it is implemented.}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Writing Rules

- **Resolve:** Record only terms whose canonical name, definition, owning context, and material conflicts are settled.
- **Canonicalize:** Pick one term and list rejected synonyms under `_Avoid_`.
- **Define:** Use one or two sentences describing what the concept is, independent of implementation.
- **Scope:** Include only concepts specific to the domain context.
- **Cluster:** Add subheadings when natural groups emerge; keep one cohesive area flat.

## Single vs Multi-Context Repos

Single-context repos use one root `CONTEXT.md`.

Multi-context repos use a root `CONTEXT-MAP.md` that points to each context's `CONTEXT.md`:

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) - receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) - generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md) - manages warehouse picking and shipping

## Relationships

- **Ordering -> Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking.
- **Fulfillment -> Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices.
- **Ordering <-> Billing**: Shared types for `CustomerId` and `Money`.
```

Use `CONTEXT-MAP.md` to route terms and record resolved context relationships. Create or update it when a context boundary or relationship resolves. Update every relevant glossary when a term crosses contexts. Keep unclear ownership unresolved and surface it in the domain delta.
