# CONTEXT.md Format

`CONTEXT.md` is the project's domain glossary. It records resolved domain language only. It is not a spec, plan, scratchpad, implementation note, or issue tracker.

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

- Record only resolved domain language. If a term is still fuzzy or disputed, surface it in the conversation instead of writing it.
- Be opinionated. Pick the canonical term and list rejected synonyms under `_Avoid_`.
- Keep definitions tight: one or two sentences.
- Define what the term is, not what it does or how it is implemented.
- Before adding a term, ask: is this concept specific to this domain context, or just a general programming concept? Only domain-context concepts belong.
- Group terms under subheadings when natural clusters emerge. A flat list is fine when the terms belong to one cohesive area.

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

Use `CONTEXT-MAP.md` to choose the relevant context. If a topic crosses contexts, update each relevant `CONTEXT.md`. If the right context is unclear, ask.
