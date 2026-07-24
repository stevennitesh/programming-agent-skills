---
name: to-spec
description: Explicitly turn one bounded settled-source packet into one verified durable parent specification; exclude ticket slicing and delivery.
---

# To Spec

Turn one bounded packet of settled source into one durable parent specification
through the configured tracker. Preserve source-owned commitments, verify the
publication, return a typed result, recommend `$to-tickets` only after verified
success, and stop without delivering the work.

The user and settled source own outcome, commitments, acceptance, scope,
exclusions, public and data contracts, security and privacy posture, and agreed
tradeoffs. Repository, domain, ADR, engineering, tracker, and relationship
owners retain their routed authority. `to-spec` owns faithful synthesis,
coverage judgment, one disposable draft, one parent publication, read-back,
recovery evidence, Return, and completion.

## Gates

### 1. Setup

Read the target repository's `AGENTS.md` and its routed tracker, labels, domain,
and engineering contracts. Verify that the configured parent-create operation
and required read-back are compatible before any draft or tracker mutation.
When setup is missing or incompatible, return `setup-precondition` with the
evidence and unchanged state, recommend `$repo-bootstrap`, and stop.

### 2. Trace settled source and state

Read the complete supplied packet and every decision-bearing pointer it names.
Accept a direct settled packet, a closed Wayfinder map with decisive
resolutions, or one verified selected improvement candidate with settled
direction and commitment boundary. Record one source owner, exact identity,
bound, and intended parent target. A missing, inaccessible, ambiguous,
contradictory, or decision-changing gap returns `source-gap` with affected
contract fields, unchanged tracker state, and the exact decision owner.

Inspect the relevant durable parent state before creation and distinguish
verified absence, matching state, divergent state, and unknown state. Create
only from verified absence. Updating or reconciling requires an explicitly
identified target and explicit authority; otherwise return
`existing-state-conflict` with observed identity, unchanged state, and the
smallest needed authorization or source delta.

Preserve routed domain terms and ADR decisions and point to their owners;
change no domain truth. Load `$codebase-design` only for module, interface,
seam, adapter, depth, leverage, and locality vocabulary whose meaning is
already settled. Retain artifact and decision authority; when a new public or
ownership choice is required, return `source-gap`.

Build a bidirectional commitment ledger. Account once for every requirement,
exclusion, deferral, constraint, dependency, risk, and nonblocking open note,
and trace every specification commitment back to source authority. Do not
invent product choices, implementation results, or a ready child-ticket graph.

### 3. Draft and cover

Draft one internally consistent parent specification containing source identity
and owner; problem and outcome; users and scenarios; scope and non-goals;
requirements and invariants; interfaces, data, and state; edge and error
behavior; security and privacy; compatibility, migration, and rollback;
operability; dependencies and risks; acceptance and proof; decisions,
deferrals, and residual gaps; and the downstream boundary. Headings and order
may fit the source.

Make the parent recoverable without conversation memory: introduce unfamiliar
terms and relied-on premises before use or provide a sharp stable pointer to
their durable owner. Do not copy normative domain or ADR truth. Confirm that a
fresh reader can recover outcome, users, commitments, acceptance, exclusions,
owners, and proof from the parent and its authoritative pointers.

Use source-visible actor-and-value scenarios for real users. Keep architecture,
security, migration, internal constraints, and other non-story commitments in
the same bidirectional ledger without inventing personas or dropping
constraints.

Pair every commitment with observable acceptance, edge or error cases, and an
honest proof authority. Choose adequate caller-facing or public proof points
and a scope-matched portfolio without coupling proof to private helpers. A new
public seam remains a source-owned decision. Name structural proxies and their
residual risk; claim no implementation proof that was not run.

When state matters, cover only the material initial, reusable,
legacy-or-incompatible, access-path, variant, and lifecycle branches. Do not
replace judgment with a Cartesian checklist.

Consider quality, security and privacy, compatibility, state, migration and
rollback, and operability against source-visible triggers. Include only
applicable obligations; omit ceremonial boilerplate; return `source-gap`
rather than inventing a triggered commitment.

For sensitive data, credentials, generated identifiers, external integrations,
migration, or cross-boundary configuration, trace each authoritative value
from source and sensitivity through boundary, destination, consumer,
lifecycle, and verification. Expose no secret literal and invent no missing
configuration.

Record each retained nonblocking deferral with its source owner, present
consequence, and `defer until <observable trigger>`. A choice that can change
current acceptance is a `source-gap`, not a deferral; do not add speculative
future design.

Write one ignored `.tmp/to-spec/<feature-slug>.md` draft only after the source
and coverage gates pass. Read back its exact bytes and correct synthesis
defects before durable publication. If the path is not safe and ignored, stop
without durable mutation.

Before publication, scan the read-back draft once for ambiguity,
contradiction, placeholders, scope drift, missing source or acceptance,
implementation leakage, and invented content. Repair supported drafting
defects or return `source-gap` for a source-owned defect. Style preferences and
nonblocking notes do not block publication; add no reviewer or approval loop.

### 4. Publish, verify, and reconcile

Delegate exactly one create operation to the configured GitHub issue, GitLab
issue, or Local Markdown `.scratch/<feature-slug>/SPEC.md` contract. Use the
frozen title and body. Add no child, label, source, domain, implementation,
Git, installation, or downstream mutation.

Refetch or reread the full created parent, including body, location, state,
metadata, and affected relationships, and compare it with the frozen draft.
When publication fails, is partial, is indeterminate, or read-back mismatches,
return `publication-recovery` with applied and failed operations, draft
identity, observed durable state, affected relationships, and the safest
inspection or recovery action. Preserve the exact draft and never repeat a
create whose result is unknown.

After a verified match, remove the disposable draft and return
`published-spec` with the durable pointer, source identity, coverage result,
mutation read-back, residual gaps, and `$to-tickets` as the one next
recommendation. Do not invoke `$to-tickets`.

## Completion

Complete only when the setup, source, target-state, commitment, draft,
publication, durable read-back, and cleanup-or-preservation gates all resolve;
every applicable commitment is accounted for; every triggered H1 check above
passes; unrelated state is preserved; and exactly one typed Return is
supported by observed durable state. Stop before source research,
conversational shaping, ticket slicing, implementation, review, installation,
or Git delivery.
