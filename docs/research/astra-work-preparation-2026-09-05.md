# Astra work preparation rewrite

This records the proposed replacement for the legacy grilling-with-docs,
to-spec, to-tickets pipeline. It is source-selection and review evidence, not
runtime guidance or proof of improved agent performance.

## Composition

`shape-work` combines evidence-informed clarification with optional durable
specification. A settled source can go directly to synthesis; an unresolved idea
can involve several dependent choices in one conversation. A local specification
does not require a tracker parent. Domain and ADR capture remains conditional on
durable value, repository conventions, and actual authority.

`to-tickets` preserves a distinct delivery-design task. It accepts a settled
conversation, spec, or audit result, creates the fewest useful boundaries, and
publishes only when requested. A single coherent outcome needs no graph, but an
explicit request for one tracker ticket remains valid. Missing tracker setup
does not prevent drafting. Existing authorization governs continuation; neither
planning nor ticket publication implicitly authorizes implementation or fanout.

The engineering contract is unchanged by this rewrite. It supplies shared coding
judgment. Codebase-design owns consequential architecture choices; prototype owns
runnable experiments. Neither is a mandatory detour or installation prerequisite.

## Local details retained

| Source | Retained judgment | Removed or qualified procedure |
| --- | --- | --- |
| Grilling | Inspect available facts; ask only material questions whose prerequisites are known; keep independent branches moving; distinguish choice, assumption, deferral, and unavailable authority. | One decision per invocation, fixed questioning format, repeated confirmation, and mandatory terminal routing. |
| Grill-with-docs and domain-modeling | Reconcile consequential domain collisions, preserve canonical meaning and invariants, distinguish implementation evidence from intended meaning, record durable decisions at their owner. | Automatic capture after every answer and setup as a prerequisite to drafting. Existing domain/ADR approval rules still apply. |
| To-spec | Preserve commitments, acceptance, public/data semantics, failure states, provenance, precedence, stopping conditions, evidence class, and residual gaps. Verify a named existing mechanism before freezing it as a capability. | Tracker-only specification, long catalogs, complete source-packet ceremony for simple conversation, and forced stops on resolvable technical questions. |
| To-tickets | Cohesive verifiable slices, real blockers, commitment ownership, producer-to-consumer acceptance, migration constraints, readiness, and recovery from uncertain publication. | Mandatory graphs, universal full-stack slices, hard-coded labels, repeated implementation recipes, and mandatory additional approval despite settled authorization. |

Detailed acceptance semantics live conditionally in shape-work's acceptance
reference. To-tickets' delivery reference preserves their implications for fresh
implementers: actual predecessor output, mixed success/failure, public meaning,
evidence qualifiers, and first useful integration verification. Repetition is
limited to the handoff where the receiving agent could otherwise lose meaning.

Tracker publication has a separate reference covering inspection, semantic reuse,
authorized repair, active claims, exact effects, configured representations,
non-ready intermediate publication, read-back, and partial/unknown outcomes.
Provider operations remain with repository tooling and policy rather than a
second copied GitHub adapter. The custom packages and their existing consumers
remain unchanged during Astra development.

## Upstream selection

Compared local snapshots, without fetching newer revisions:

| Source | Commit | Selection |
| --- | --- | --- |
| Matt Pocock | `3cca18b368ae95cdbdebbff572ccafa662551015` | Keep prerequisite-aware conversation, synthesis from settled context, verifiable slices, explicit blocking edges, and decision-rich prototype fragments. Reject relentless exhaustive questioning, automatic fanout, idealizing one test boundary, long required user-story lists, default ready labels, and mandatory prefactoring. |
| Pstack | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Keep useful verification boundaries and explicit migration end states. Reconcile per-edit-green and planned-breakage advice through actual delivery and compatibility constraints, not a universal rule. |
| Superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Keep independent deliverables, sufficient fresh-agent context, and checking plan coverage. Reject mandatory code-filled microsteps, TDD, commits, file decomposition, execution-worker selection, and approval gates. |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | Keep avoiding speculative work after understanding the requested outcome. Do not substitute a smaller product, collapse meaningful delivery boundaries for line count, or import persistent persona rules. |

## Challenger review

Three fresh-context, read-only reviewers examined a fixed draft. Their exclusive
scopes were custom quality-detail preservation, upstream method selection, and
workflow/authority composition. Accepted corrections:

- Keep canonical terminology scoped to a context; preserve independent meanings
  and describe translation where contexts interact.
- For dependent domain/ADR writes, establish readable replacement truth before
  removing old material, and stop to inspect attempted targets after uncertainty.
- Include learning-dependent work in the delivery-reference trigger so later
  ticket readiness cannot ignore the experimental result.
- Make explicit single-ticket drafting, publication, and repair discoverable.
- When the mechanism remains open, consider existing capabilities or a smaller
  change without weakening requirements or reopening the user's explicit choice.

The custom review explicitly checked composition, rejection and mixed-input
semantics, time meaning, precedence, stopping conditions, evidence qualifications,
migration, managed-target observation, and publication recovery. The upstream
review compared the listed methods; it did not inspect visual-companion machinery.
The workflow review tested settled-source capture, authorized continuation,
unresolved priorities, one-ticket requests, absent trackers, partial graphs,
active claims, drift, and learning-dependent delivery.

All three reviewers rechecked their corrections and passed their assigned scopes.
Both skill package checks, repository validation, local Markdown links, and
whitespace checks passed. No tracker effects or global installation were performed.

## Verification limits

These packages contain instructions and conditional references, not executable
publication tooling. Structure and link checks establish packaging integrity;
textual challenge can find lost obligations or contradictory instructions.
Neither demonstrates better interviews, specifications, or delivery plans than
the model baseline. That requires a separate behavioral comparison with realistic
ambiguity and fresh implementers.
