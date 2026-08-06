# Wayfinder Current Runtime Synthesis

Status: current ownership and relationship reference. Runtime procedure remains
in `skills/custom/wayfinder/`.

The former broader Resume/Reopen, multi-budget, closure-generation proposal is
preserved as [inactive design history](wayfinder-state-machine-proposal.md). It
is not compatibility behavior, routing authority, or an extraction target.

## Outcome And Boundary

Wayfinder resolves one finite tracker-backed route from a bounded foggy
destination to a coherent settled source or terminal decision. It owns map
orientation, resolver classification, consequence reconciliation, fog and
finite growth, map claims, closure coherence, and the terminal packet.

Tickets own one sharp decision or prerequisite. Resolver skills own their local
admission, evidence or judgment, mutation boundary, and Return. Wayfinder
normalizes the intact Return and remains the sole owner of map state and the
next operation.

Wayfinder never delivers implementation. The successful chain is:

```text
$wayfinder -> recommend and stop -> $to-spec
$to-spec -> recommend and stop -> $to-tickets
$to-tickets -> recommend and stop -> $implement | $parallel-implement
```

A terminal decision stops at Wayfinder. Closed maps never route directly to
ticketing or implementation.

## Runtime Authority

- `skills/custom/wayfinder/SKILL.md`: gates, operations, resolver normalization,
  reconciliation, completion, and Return.
- `skills/custom/wayfinder/MAP-FORMAT.md`: durable map, ticket, fog, resolution,
  growth, and closing fields.
- `skills/custom/wayfinder/agents/openai.yaml`: explicit-only invocation.
- configured tracker `Wayfinding representation`: provider objects, labels,
  relationships, claim storage, close primitives, and Mutation read-back.
- `docs/synthesis/skill-context-relationships.md` and the embedded contract in
  `docs/synthesis/skill-pack.md`: cross-skill verbs and handoff ownership.

No other Wayfinder package is runnable or manifest-tracked.

## Gate And Operation Spine

Every invocation begins at Orient and derives one operation or safe Return from
current identity, integrity, frontier, liveness, blocker, closure, and terminal
evidence.

```text
Orient
├─ no map -> Chart
├─ frontier or answer-bearing return -> Advance one ticket
├─ deterministic drift or liveness change -> Maintain
├─ coherent supported destination -> Closure
├─ owner-confirmed unsuccessful terminal state -> Terminate
└─ waiting | blocked | incompatible | closed -> Return
```

Chart, Advance, and Maintain use the shared Mutation Gate and Reconcile owner.
Closure prepares Gather, Coherence, and Domain Modeling without a claim, then
claims only for the drift-checked Seal. Terminate requires destination-owner
confirmation and bypasses successful closure and To Spec.

Closed maps are immutable. Material later gaps require a successor Chart with
an explicit predecessor pointer and explicit decision/evidence imports. Claims,
frontier, growth, and lifecycle never transfer.

## Fog And Convergence

Fog is legal only while the question remains unsharp and the map records a
finite sharpening source, owner, observable trigger, fallback, and affected
tickets. Every affected fog item is retained, graduated, resolved, or excluded
during Reconcile.

Chart approves one finite allowance for tickets created after Chart. Each new
ticket consumes one. Exhaustion or destination change cannot silently widen the
campaign; it returns for a new finite approval, Terminate, or successor.

The allowance is the only campaign budget. Outcome, correction, Reopen, and
multi-counter compatibility machinery are deliberately absent.

## Resolver Composition

| Ticket | Relationship and boundary |
| --- | --- |
| Research | Invoke `$research`; pass the map use, scope, exact state, note path/write mode, Source Trace, and return owner. |
| Prototype | Invoke `$prototype` with the complete resolver packet owned by `MAP-FORMAT.md`. |
| Diagnosis | Return `diagnosis-required` and Wait. Diagnosis remains separately explicit; its attributable Return later re-enters Wayfinder. |
| Grilling | Invoke `$grilling` for a conversation-only user decision or `$grill-with-docs` while domain capture is active. A nested Route gap returns to active Wayfinder without a self-recommendation. |
| Questionnaire | Invoke `$to-questionnaire` only after exact packet approval. A verified artifact becomes Waiting; missing approval is an incomplete Wayfinder Return with no callee execution. |
| Task | Inspect one objectively bounded repository or operational fact without durable mutation. |

Wayfinder maps supported answers to `resolved`, attributable external or human
returns to `waiting`, exact gaps to `blocked`, governing scope evidence to `out
of scope`, and malformed, unauthorized, mismatched, or non-admitted Returns to
`incomplete` without shared mutation.

## Handoff Rules

- Upstream skills recommend Wayfinder and stop; the user explicitly starts it.
- Missing tracker capability recommends Repo Bootstrap and stops.
- Resolver Returns always come back to Wayfinder; they never select another map
  operation.
- To Questionnaire may recommend Repo Bootstrap for a missing ignored artifact
  root. Nested under Wayfinder, that intact setup gap returns for map
  classification.
- Domain Modeling runs only for an unaccounted durable consequence during
  Closure and returns its complete Domain Delta.
- Successful Closure recommends To Spec and stops.

## Deterministic Versus Judgment Ownership

Provider and validator surfaces may check section schema, exact identity,
frontier and dependency state, claim acquisition/release, UUID and timestamp
shape, revision equality, allowance arithmetic, and mutation read-back. They
return evidence only.

Wayfinder retains judgment over destination admission, sharp question versus
fog, participation and resolver choice, evidence applicability, outcome
normalization, consequence scope, coherence, termination, successor imports,
and permission to close.

## Proof Surface

Structural proof should parse the embedded relationship contract, compare its
Wayfinder-involved edges with the human index, validate persisted map fields,
and ensure Wayfinding tracker fields occur inside their named section. Practical
cases should cover:

- duplicate-map refusal and map-first Chart creation;
- fog sharpening and growth exhaustion;
- Waiting and Blocked re-entry;
- nested Grilling Route gap without a self-cycle;
- questionnaire approval and setup failure;
- commit-point drift with resolver evidence preserved;
- independently selected Closure with route-closing evidence;
- owner-confirmed Terminate; and
- no direct delivery edge.

Historical transcripts and the inactive proposal are provenance, not fresh
behavioral efficacy evidence.
