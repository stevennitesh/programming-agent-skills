# Document reconciliation

Use when current specs, domain records, ADRs, plans, or guidance conflict, or when
a durable update replaces, relocates, or retires an active source. Reconcile the
documents and consumers affected by the task; a wider context audit is not required.

## Establish current authority and useful ownership

Distinguish accepted decisions, proposals, current facts, and historical evidence.
Age alone does not establish obsolescence, and a new proposal does not supersede
accepted work. Resolve consequential contradictions from governing decisions or
their owner rather than silently choosing whichever document is newest.

Follow the repository's owners. These roles can help place meaning without
requiring separate files or a prescribed hierarchy:

| Role | What it preserves |
| --- | --- |
| Specification | Intended outcome, scope, behavior, constraints, and acceptance |
| Domain record | Shared language, relationships, and invariants |
| ADR | A consequential choice, rationale, consequences, and current applicability |
| Repository guidance | Local requirements, commands, and routes needed for work |
| Delivery plan | Remaining work and adaptable sequencing within accepted constraints |

Prefer updating a useful owner over creating a competing source. Consolidate,
correct, relocate, retire, or retain with clarified applicability as warranted.
A requirement should remain authoritative at a clear owner; other documents can
link to it instead of maintaining independent copies.

## Preserve meaning and the reading path

Before retiring a source, preserve still-governing commitments and useful decision
evidence at the surviving owner. Make the replacement readable before removing or
reclassifying its predecessor.

Inspect and update affected indexes, guidance, and other consumers within scope,
including when a conflict is corrected without removing a document. If a consumer
cannot yet be reconciled, keep a usable source with explicit applicability and
report the unresolved dependency rather than leaving an unexplained contradiction.

Preserve ADR rationale and mark supersession or partial replacement according to
repository conventions. Archive when policy or a concrete retention need warrants
it; historical evidence can remain searchable without being active authority.

Shaping owns coherence around the decisions it settles. Context-hygiene owns
broader maintenance of repository context and can use this reference for accepted
meaning and preservation. Neither authorizes unrelated policy or product changes.

## Verify the receiving path

Check that future agents can find the current meaning, see what has been
superseded, and follow relocated links. Preserve still-governing commitments and
identify unresolved owners, consumers, or publication effects. Choose verification
suited to the affected sources; no fixed reconciliation report is required.
