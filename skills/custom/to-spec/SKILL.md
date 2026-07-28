---
name: to-spec
description: Explicitly turn one bounded settled-source packet into one verified durable parent specification; exclude ticket slicing and delivery.
---

# To Spec

Turn one bounded packet of settled source into one durable parent decision
contract through the configured tracker. Preserve source-owned commitments,
verify the publication, return a typed result, recommend `$to-tickets` only
after verified success, and stop without delivering the work.

The user and settled source own outcome, commitments, acceptance, scope,
exclusions, public and data contracts, security and privacy posture, and agreed
tradeoffs. Repository, domain, ADR, engineering, tracker, and relationship
owners retain their routed authority. `to-spec` owns faithful synthesis,
coverage judgment, one disposable draft, one parent publication, read-back,
recovery evidence, Return, and completion.

## Gates

### 1. Setup

Read the target repository's `AGENTS.md` and its routed tracker, labels, domain,
and engineering contracts. Verify the required inspect and read-back operations
before any draft. Before any create, verify that the configured parent-create
operation is compatible. When setup is missing or incompatible, return
`setup-precondition` with the evidence and unchanged state, recommend
`$repo-bootstrap`, and stop.

### 2. Trace settled source and state

Read the complete supplied packet and every decision-bearing pointer it names.
Accept a direct settled packet, a closed Wayfinder map with decisive
resolutions, or one verified selected improvement candidate with settled
direction and commitment boundary. Record one source owner, exact identity,
bound, and intended parent target. Confirm that the source settles the purpose,
boundaries, limitations, decisions and their owners, required behavioral,
migration, cutover, or retirement outcomes, and acceptance objectives that
apply. A missing, inaccessible, ambiguous, contradictory, or decision-changing
gap returns `source-gap` with affected contract fields, unchanged tracker
state, the exact return owner, and exactly one gap kind:
`user-decision`, `domain-decision`, `source-evidence`, `runnable-evidence`,
`stakeholder-evidence`, or `multi-decision-fog`. Preserve the source identity
and state the exact re-entry condition. Do not invoke or recommend a resolver.

Verify implementation-adjacent source claims against their exact code, caller,
test, configuration, or decision pointers. If a required current-state claim
has no verifiable pointer, return `source-gap`; do not replace source shaping
with an independent repository survey or architecture choice.

Inspect the relevant durable parent state before creation and distinguish
verified absence, exact matching state, divergent state, and unknown state.
Reuse only an exact match; otherwise create only from verified absence.
Updating or reconciling requires an explicitly identified target and explicit
authority; otherwise return `existing-state-conflict` with observed identity,
unchanged state, and the smallest needed authorization or source delta.

Preserve routed domain terms and ADR decisions and point to their owners;
change no domain truth. Load `$codebase-design` for shared design vocabulary.
When the source delegates internal technical design and one consequential
Responsibility, Interface, Seam, or Proof Seam must be settled for the
spec, apply Direct Design before drafting and fold its supported result into
the specification. Retain artifact and decision authority and create no
separate design packet. A `decision-needed` or `evidence-gap` result, new
public or ownership choice, or unsupported trade-off returns `source-gap`.

Build a bidirectional commitment ledger. Account once for every requirement,
exclusion, deferral, constraint, dependency, risk, and nonblocking open note,
and trace every specification commitment back to source authority. Do not
invent product choices, implementation results, or a ready child-ticket graph.
When the source supersedes behavior, carry each displaced surface and retained
compatibility path with its owner, reason, proof, and Removal Trigger.

### 3. Draft and cover

Draft one internally consistent parent specification containing Source Trace
with exact source identity and owner; problem and outcome; users and scenarios;
scope and non-goals; requirements and invariants; interfaces, data, and state;
edge and error behavior; security and privacy; compatibility, migration, and
rollback; operability; dependencies and risks; acceptance and proof; decisions,
deferrals, and residual gaps; and the downstream boundary. Headings and order
may fit the source. Include only source-triggered facts and omit empty or
ceremonial sections. Point to the Engineering Contract instead of copying its
generic practices.

Pair every commitment with observable acceptance and an honest proof authority.
Cover edge, error, and state branches where behavior materially varies. Name
structural proxies and their residual risk; claim no implementation proof that
was not run. Record settled or delegated-and-supported material
Responsibilities, Interfaces, Seams, Proof Seams, and state. Omit
incidental internal seams.

When state matters, cover only the material initial, reusable,
legacy-or-incompatible, access-path, variant, and lifecycle branches. Do not
replace judgment with a Cartesian checklist.

Write one ignored `.tmp/to-spec/<feature-slug>.md` draft only after the source
and coverage gates pass. Read back its exact bytes and correct synthesis
defects before durable publication. If the path is not safe and ignored, stop
without durable mutation.

Carry a path, current owner, reuse candidate, or Proof Seam only when it is a
binding source decision, supported design result, or evidence pointer. A
material Seam belongs in the spec when it affects caller contracts,
cross-ticket ownership, compatibility or migration, or test strategy. Paths
are evidence, not an implementation plan. Leave bounded repository grounding,
ticket slices, expected writes, concrete proof lanes and test owners,
dependency graph and ready frontier, execution profiles, parallel-safety
decisions, implementation technique, and default Repair budgets to
`$to-tickets` and delivery owners.

### 4. Publish, verify, and reconcile

For exact matching state, reuse the verified parent without mutation. Otherwise
delegate exactly one create operation to the configured GitHub issue, GitLab
issue, or Local Markdown `.scratch/<feature-slug>/SPEC.md` contract. Use the
frozen title and body. Add no child, label, source, domain, implementation,
Git, installation, or downstream mutation.

Refetch or reread the full created or reused parent, including body, location,
state, metadata, and affected relationships, and compare it with the frozen
draft. When publication fails, is partial, is indeterminate, or read-back
mismatches, return `publication-recovery` with applied and failed operations,
draft identity, observed durable state, affected relationships, and the safest
inspection or recovery action. Preserve the exact draft and never repeat a
create whose result is unknown.

After a verified create or exact reuse, remove the disposable draft and return
`ready-spec` with the durable pointer, source identity, coverage result,
publication-or-reuse proof, residual gaps, and `$to-tickets` as the one next
recommendation. Do not invoke `$to-tickets`.

## Completion

Complete only when the setup, source, target-state, commitment, draft,
publication-or-reuse, durable read-back, and cleanup-or-preservation gates all
resolve; every applicable commitment is accounted for; unrelated state is
preserved; and exactly one typed Return is supported by observed durable state.
Stop before source research, conversational shaping, ticket slicing,
implementation, review, installation, or Git delivery.
