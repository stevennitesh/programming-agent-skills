---
name: to-spec
description: Explicitly turn settled source that benefits from a durable parent decision contract into one verified specification; return one bounded direct implementation to its caller without drafting.
---

# To Spec

Turn settled source into a durable parent decision contract only when that
artifact is useful for several slices, durable coordination, or a lasting
decision boundary. Preserve source-owned commitments, verify any publication,
return one typed result, and stop without delivering the work.

The user and settled source own outcome, commitments, acceptance, scope,
exclusions, public and data contracts, security and privacy posture, and agreed
tradeoffs. Repository, domain, ADR, engineering, tracker, and relationship
owners retain their routed authority. `to-spec` owns faithful synthesis,
coverage judgment, at most one disposable draft, one parent publication, read-back,
recovery evidence, Return, and completion.

## Gates

### 1. Trace settled source and choose the branch

Read the target repository's `AGENTS.md`, routed domain and engineering
contracts, the complete supplied packet, and every decision-bearing pointer it
names.
Accept a direct settled packet, a closed Wayfinder map with decisive
resolutions, or one verified selected improvement candidate with settled
direction and commitment boundary. Record one source owner, exact identity,
bound, and intended parent target. Confirm that the source settles the purpose,
boundaries, limitations, decisions and their owners, required behavioral,
migration, cutover, or retirement outcomes, and acceptance objectives that
apply. A missing, inaccessible, ambiguous, contradictory, or decision-changing
gap returns `source-gap` with affected contract fields, unchanged tracker state,
the exact return owner, and exactly one gap kind: `user-decision`,
`domain-decision`, `source-evidence`, `runnable-evidence`,
`stakeholder-evidence`, or `multi-decision-fog`. Preserve the source identity
and state the exact re-entry condition. Do not invoke or recommend a resolver.

When the settled source already describes one bounded implementation with
complete acceptance and authority and no useful durable parent contract, return
`not-needed` with its exact source and `$implement` as the one unstarted next
recommendation. Create no draft or tracker state.

### 2. Prepare the durable-parent branch

Only after the direct branch is excluded, load the routed tracker contract and
verify its required inspect and read-back operations. Before any create, verify
that the configured parent-create operation is compatible. When that setup is
missing or incompatible, return `setup-precondition` with the evidence and
unchanged state, recommend `$repo-bootstrap`, and stop.

Verify implementation-adjacent source claims against their exact code, caller,
test, configuration, or decision pointers. If a required current-state claim has
no verifiable pointer, return `source-gap`; do not replace source shaping with
an independent repository survey or architecture choice. When verification
corrects a source statement without changing a source-owned decision or
commitment, preserve the settled direction and record one Verified Source
Correction with the original statement, observed evidence pointer, corrected
current-state wording, and why the commitments are unchanged. A
decision-changing correction is a `source-gap`, not editorial license.

Preserve routed domain terms and ADR decisions and point to their owners; change
no domain truth. Load `$codebase-design` only when the source delegates one
consequential unresolved architecture question about ownership, data shape,
interface, state or failure policy, seam, or migration. Fold its recommendation,
retain judgment, or exact gap into the specification and create no separate
design artifact. A new public or ownership choice, missing evidence, or
unsupported trade-off returns `source-gap`.

Cover every applicable requirement, exclusion, deferral, constraint,
dependency, risk, and nonblocking open note and trace each specification
commitment back to source authority. Use a detailed bidirectional crosswalk only
for numerous, conflicting, or multi-source commitments. Do not invent product
choices, implementation results, or a ready child-ticket graph. When the source
supersedes behavior, carry each displaced surface and retained compatibility
path with its owner, reason, proof, and removal condition.

### 3. Freeze, compare, and draft when needed

Freeze one internally consistent title and parent body containing Source Trace
with exact source identity and owner; problem and outcome; users and scenarios;
scope and non-goals; requirements and invariants; interfaces, data, and state;
edge and error behavior; security and privacy; compatibility, migration, and
rollback; operability; dependencies and risks; acceptance and proof; decisions,
deferrals, and residual gaps; Verified Source Corrections when present; and the
downstream boundary. Headings and order may fit the source. Include only
source-triggered facts and omit empty or ceremonial sections, including the
correction section when none exists. Point to the Engineering Contract instead
of copying its generic practices.

Pair every commitment with observable acceptance and an honest proof authority.
Cover edge, error, and state branches where behavior materially varies. Name
structural proxies and their residual risk; claim no implementation proof that
was not run. Record settled or delegated-and-supported material
Responsibilities, Interfaces, Seams, Proof Seams, and state. Omit incidental
internal seams.

When state matters, cover only the material initial, reusable,
legacy-or-incompatible, access-path, variant, and lifecycle branches. Do not
replace judgment with a Cartesian checklist.

Inspect the intended durable parent target and compare it with the frozen title
and body. Distinguish verified absence, exact matching state, divergent state,
and unknown state. Reuse only an exact match; otherwise create only from
verified absence. Updating or reconciling requires an explicitly identified
target and explicit authority; otherwise return `existing-state-conflict` with
observed identity, unchanged state, and the smallest needed authorization or
source delta.

Write one ignored `.tmp/to-spec/<feature-slug>.md` draft only when a new or
updated durable publication is required and after the source and coverage gates
pass. Exact reuse creates no draft. Read back draft bytes and correct synthesis
defects before publication. If the path is not safe and ignored, stop without
durable mutation.

Carry a path, current owner, reuse candidate, or Proof Seam only when it is a
binding source decision, supported design result, or evidence pointer. A
material Seam belongs in the spec when it affects caller contracts, cross-ticket
ownership, compatibility or migration, or test strategy. Paths are evidence, not
an implementation plan. Leave bounded repository grounding, ticket slices,
expected writes, concrete checks and test owners, dependency graph and
ready frontier, static execution facts, live concurrency decisions, and
implementation technique to `$to-tickets` and delivery owners.

### 4. Publish, verify, and reconcile

For exact matching state, reuse the verified parent without mutation. Otherwise
perform exactly one configured create operation for the GitHub issue, GitLab
issue, or Local Markdown `.scratch/<feature-slug>/SPEC.md` contract. Use the
frozen title and body. Add no child, label, source, domain, implementation, Git,
installation, or downstream mutation.

Refetch or reread the full created or reused parent, including body, location,
state, metadata, and affected relationships, and compare it with the frozen
title and body. When publication fails, is partial, is indeterminate, or read-back
mismatches, return `publication-recovery` with applied and failed operations,
publication input identity, any draft identity, observed durable state, affected
relationships, and the safest inspection or recovery action. Preserve any exact
draft and never repeat a create whose result is unknown.

After a verified create or exact reuse, remove any disposable draft and return
`ready-spec` with the durable pointer, source identity, coverage result,
publication-or-reuse proof, and residual gaps. Recommend `$to-tickets` only
when several implementation slices or durable tracker coordination are useful;
otherwise recommend `$implement`. Invoke neither.

## Completion

Complete through the selected branch: `not-needed` requires verified direct
readiness and no mutation; `ready-spec` requires applicable setup, source,
target-state, coverage, publication-or-reuse, durable read-back, and
cleanup-or-preservation gates. Every applicable commitment is accounted for,
unrelated state is preserved, and exactly one typed Return is supported by
observed state.
Stop before source research, conversational shaping, ticket slicing,
implementation, review, installation, or Git delivery.
