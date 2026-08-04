---
name: to-tickets
description: Explicitly create or repair a verified dependency-ordered implementation ticket graph when one settled source has several valuable delivery slices or durable coordination needs; route one bounded implementation directly to Implement.
---

# To Tickets

Run only when the user explicitly selects `to-tickets` to create, repair, or
order implementation tickets from one settled bounded source. Do not admit
implicit discovery, raw intake, one already selected Ready-for-agent item, or
delivery of an existing graph.

## Admit

Read the target repository's `AGENTS.md` and its routed tracker, label, domain,
and engineering contracts. Before tracker mutation, verify that the configured
tracker can create recoverable non-ready items or one equivalently safe atomic
graph, represent parent and blocking relationships, map roles and
Ready-for-agent state and, when applicable, Ready-for-human state, inspect
claims and both frontiers, and read every mutation back. Otherwise return
`setup-precondition`, name the missing or incompatible surface, recommend
`$repo-bootstrap`, and preserve state. For GitHub, consume the configured
parent/child and dependency modes and resolve their operation and read-back
routes once before the first create. When the connector does not expose native
relationship mutations, use the bundled
[GitHub relationship helper](scripts/github_issue_relationships.py) to perform
at most one requested mutation and return normalized bidirectional read-back.
Preflight proves that configured operations exist, are authorized, and have
read-back routes; only the first real mutation proves live behavior.

Accept one exact identity-bearing settled source whose remaining work is
implementation slicing: a verified parent specification; a direct settled packet
with commitment authority; a verified selected improvement whose direction,
boundary, and multi-slice need are settled; a verified audit finding or cohesive
cluster with settled remediation intent; or an exhaustive consumer repair packet
reconciled with its original source. Read every decision-bearing pointer. If
identity, access, authority, commitment, acceptance, dependency meaning,
supported state, or another source-owned fact is missing, ambiguous, or
contradictory, return `source-gap` with the affected fields and owner and leave
tracker state unchanged.

If the settled source is already one bounded implementation with one useful
proof path and no durable coordination need, return `direct-item` with a compact
Implement handoff and recommend `$implement`. Create no graph or tracker state.

The user and settled source retain outcome, commitments, acceptance, scope,
exclusions, supported states, public and data contracts, security and privacy
posture, compatibility, migration, rollback, and agreed tradeoffs. `to-tickets`
owns coverage, slicing, ticket boundaries, dependency order,
proof-responsibility mapping, execution profiles, the frozen publication packet,
configured tracker publication, read-back, recovery evidence, Return, and
completion. Tracker, engineering, domain, ADR, setup, triage, and delivery
owners retain their foreign contracts.

Classify the requested operation as create or repair. Repair authority exists
only for an explicit user-selected repair, a verified `$parallel-implement`
graph-defect packet, or a post-publication implementation invalidation that
names the landed predecessor or commit, before-and-after evidence, invalidated
graph fields, and affected tickets. Repair does not settle a source-owned fact.
Admit repair only while the underlying source commitments remain settled.

Change only configured tracker state, including configured Local Markdown
tracker files. Do not mutate source or domain truth, code, implementation,
review, unrelated worktree paths, the Git index, `HEAD`, remotes, installation,
or delivery.

## Shape

Inspect the exact target parent, related children, relationships, roles, claims,
open or closed state, and ready frontier before design. Distinguish verified
absence, an exact semantic match, verified unclaimed divergence, and unknown
state. Create only after verified absence. Reuse only an exact semantic match.
Repair frozen mismatches only under the admitted repair authority. A claim,
partial authorship, ambiguous identity, unauthorized divergence, or
indeterminate prior mutation returns `existing-state-conflict` with observed
identities and the smallest needed authority or source delta.

Only when graph work remains, inspect enough code to ground the affected
tickets: the current behavior owner, representative callers and entry paths,
Proof Seams, tests, configuration, Repository Reuse, and repository constraints.
Treat paths as evidence, not ticket boundaries or implementation technique.

Treat source-owned Responsibilities, Interfaces, and Seams as fixed. Map each
applicable Proof Seam to its concrete proof lane and canonical test owner; do
not create or move a Seam, or turn a ticket boundary into architecture. A
missing consequential design decision returns `source-gap`.

Account exactly once for every in-scope
requirement, exclusion, deferral, dependency, risk, and proof obligation. Map
each proof obligation to one canonical responsibility: its existing test surface
or proof lane, one owning ticket or graph-level fence, and every dependent
consumer. Shared proof may serve several tickets, but shared test mutation needs
one owner or explicit serialization. The result must contain one or more
implementation tickets; omitted, duplicated, contradictory, or ownerless
commitments block publication. Keep the mapping in the ticket packets; add a
compact cross-ticket coverage table only when shared commitments or proof make
ticket-local mapping ambiguous. Create no second planning artifact. Distinguish a non-goal,
which is outside delivery scope, from prohibited behavior, which requires an
acceptance or proof obligation. Map every source-visible Change Closure
obligation, including displaced paths and intentionally retained compatibility,
to one ticket or graph-level fence.

Prefer independently completable vertical behavior slices. Admit a support or
migration slice only when it has observable value and proof and names the
behavior, compatibility obligation, or risk it unlocks. Reject file
choreography, speculative scaffolding, cross-owned slices, and arbitrary
microtasks; split only where separate proof, authority, rollback, dependency
unlock, permission, state, migration, or ownership makes separate completion
valuable.

Give each ticket the smallest execution packet that lets a fresh implementer
act correctly:

- **Intent:** one bounded outcome, Source Trace, operational and observable
  acceptance, Commitment Boundary, and explicit non-goals.
- **Grounding:** current behavior owner, representative callers and entry
  paths, Repository Reuse, repository constraints, and source-owned
  prototype, research, domain, ADR, migration, or compatibility facts.
- **Correctness, when material:** applicable Invariants, Trust Boundaries, supported states,
  edge and error cases, failure and recovery behavior, compatibility and
  environmental constraints, observability or measured-claim obligations,
  and prohibited behavior with negative proof.
- **Scope and proof:** expected durable writes, scope fence, required authority
  prerequisites, source-owned Proof Seam, concrete proof lane, canonical proof
  responsibility and current test owner, and verification authority and
  evidence. State whether the ticket should reuse, extend, or add proof;
  adding a test requires a distinct responsibility.
- **Delivery:** dependency state, true blockers or `none`, stable tracker
  order, executor role, and known overlap or serial tripwires.
- **Closure, when material:** displaced surfaces and each retained compatibility path's owner,
  reason, proof, and Removal Trigger.

Before readiness, test every acceptance term governing a calculation,
threshold, comparison, equivalence, or state. Record its operational definition
or exact authoritative owner; otherwise return `source-gap` rather than delegate
meaning to implementation.

Keep each body semantically dense: state each execution-relevant fact once,
prefer sharp owner and evidence pointers to repeated source prose, and aim for
at most about 5,500 characters as a soft target. Exceed it only when required
authority, state, edge, proof, migration, or recovery detail cannot remain
implementation-ready when shorter.
Omit inapplicable optional sections. Do not add `N/A` padding. Identity,
acceptance, scope, proof lane, dependency state, executor, and ownership always
remain explicit.

Record one finite nonnegative graph-level Repair generation budget. Preserve an
explicit source or caller value; otherwise default exactly to `2`. Repeat it in
a ticket only when that ticket overrides the graph value.

Separate packet readiness from frontier eligibility. Ready-for-agent means the
agent execution packet is verified; unresolved blockers or claims keep it out
of the agent frontier without making the packet non-ready. When settled work
requires human access, permission, judgment in execution, or a cutover, create a
fully shaped Ready-for-human ticket with its executor, trigger, completion
evidence, and return condition. Mixed graphs may contain both states. Human
tickets never enter the agent frontier or an implementation recommendation, and
their unresolved edges block consumers normally. Do not use Ready-for-human to
defer an unsettled source or design decision; return `source-gap` instead.
A ticket missing the facts required for its mapped readiness remains non-ready;
correct locally or return `source-gap` when source authority is missing.

For a stateful ticket whose behavior materially changes by state, record the distinct supported absent or initial,
reusable, legacy or incompatible, public access-path, variant, lifecycle, and
high-risk branches needed for implementation and proof. Use a matrix only when
it is clearer than prose; never add Cartesian or stateless padding. If material
supported state is unsettled, return `source-gap`.

Freeze a complete acyclic dependency graph with explicit blockers and stable
tracker order. Dependency order is topological: blockers precede dependents and
stable tracker order breaks ties. Derive the Ready-for-agent and Ready-for-human
frontiers separately; their union is the actionable frontier and at least one
must be non-empty. Add a blocking edge only when the dependent consumes a
required predecessor outcome; tracker order and serial constraints are not
blockers. Correct cycles, orphans, false or hidden blockers, contradictory
order, and empty or false frontiers before publication, or return `source-gap`
when correction needs source authority.

Record only the static execution facts implementation needs: semantic owner,
expected writes, proof owner, blockers, and known overlap or serial tripwires.
`$parallel-implement` decides live concurrency from the current graph and
checkout state. Treat uncertain independence conservatively as serial; never
infer it from filenames alone.

For protected data, permissions, trust boundaries, irreversible state,
migrations, or cutovers, put one production-path tracer before dependent work
and require retry, rollback, and partial-state proof. For a non-atomic
interface, schema, client, or data change, use expand-migrate-contract and
contract only after old usage ends and compatibility proof passes. Do not
parallelize or defer unresolved high-risk proof.

## Publish

Freeze the exact source identity, ticket titles and bodies,
symbolic child identities, roles, expected relationships, dependency order,
predicted frontier, applicable cross-ticket proof ownership, and publication
operation templates before durable mutation. Bind
each returned tracker identity to its symbolic child through immediate
read-back before any dependent mutation. Verify that the invocation or an
explicit follow-up authorizes that exact configured tracker transition. A
read-only request, changed plan, or unclear mutation scope leaves state
unchanged and returns `existing-state-conflict` with the exact authority needed.

Create verified-missing children in dependency order and a recoverable non-ready
state, or use one configured atomic graph operation with equivalent proof.
Immediately refetch each unique create, attach and read back its frozen parent
relationship, and attach every now-resolvable blocking edge before creating the
next child. The first authorized child and its read-back prove live
parent/child behavior without a disposable probe; the first applicable blocking
edge and read-back likewise prove live dependency behavior. When the tracker
lacks a safe route, return
`setup-precondition` before creation. Never repeat an indeterminate create.

A missing endpoint or partial or mismatched relationship stops the run with
`publication-recovery`; preserve created items as non-ready. Never switch the
frozen relationship representation during publication.

Only after every body and relationship verifies, apply source-authorized roles
and activate each ticket's mapped Ready-for-agent or Ready-for-human state in
dependency order, reading back each transition. Do not invent a category role.
A claim, unverified packet or edge, or partial activation returns
`publication-recovery` with the exact exposed frontiers.

Refetch the complete affected graph and every affected dependent. Compare bodies
by the tracker-owned exact-byte or normalized-semantic rule and verify
relationships, roles, claims, comments, assignees, open or closed status,
mapped readiness state, and the derived agent and human frontiers against the
frozen plan. Any stale, partial, indeterminate, or mismatched observation returns
`publication-recovery` and cannot support success.

On the first unsafe, failed, or indeterminate transition, stop further mutation.
Return `publication-recovery` with the frozen graph identity, every applied and
failed operation, exact observed items and relationships, current agent and
human frontiers, and the safest configured recovery action. Do not invent
rollback, compensation, atomic success, or a duplicate create.

## Return

For a verified graph with a non-empty agent frontier and without a qualified
parent-delivery request, recommend `$implement` with the first agent ticket in
tracker order. Do not recommend implementation before graph proof or select a
blocked, human-owned, or later ticket. When only the human frontier is non-empty,
recommend its first ticket to the named human owner and do not recommend an
implementation skill.

Recommend `$parallel-implement` only when the user explicitly requested a
top-level parent-delivery run and the verified graph is parent-backed,
exhaustive, entirely Ready-for-agent, has a non-empty agent frontier, and
contains at least two substantial tickets that may be independent enough for
concurrency or whose coordinated delivery is otherwise worthwhile. A direct graph, mixed human/agent graph, delegated request, generic
preference for concurrency, incomplete graph, or missing explicit delivery
request uses the single-frontier route above instead.

Return exactly one of `direct-item`, `setup-precondition`, `source-gap`,
`existing-state-conflict`, `publication-recovery`, or `ready-graph`. An
`existing-state-conflict` covers an existing claim or divergence and missing or
unclear authority for the frozen tracker transition; source-owned ambiguity
remains `source-gap`. A
`ready-graph` reports source and parent identities, graph identity, ordered
ticket pointers, dependency edges, agent and human frontiers,
compact cross-ticket proof-owner and serialization summaries, publication or
reuse read-back, residual gaps, and exactly one unstarted next recommendation.
Ticket bodies remain authoritative for static execution facts and applicable
state coverage;
successors refetch their pointers instead of receiving repeated packet prose.
Complete only when the selected branch's setup and source authority resolve;
every commitment maps; every ticket, proof responsibility, applicable state
coverage, edge, order, frontier, and
authorized transition verifies; no duplicate or false-ready item remains;
unrelated state is preserved; one typed Return is supported by observed state;
and no successor starts.
