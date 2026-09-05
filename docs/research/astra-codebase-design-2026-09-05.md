# Astra codebase-design rewrite assessment

This records source selection and challenger feedback for
`skills/astra/codebase-design/`. It is research evidence, not runtime guidance
or proof of improved coding performance.

## Direction

Keep codebase-design and prototype separate. Design resolves a consequential
question about ownership, interfaces, state, dependencies, or migration.
Prototype owns runnable experiments when observation can change that decision.
Neither is a prerequisite for straightforward implementation.

The candidate retains useful design methods from the custom skill while removing
its single-module framing, repeated vocabulary, and stops that prevented an
agent from making authorized technical decisions. A bounded question may cross
several systems. A design-only request still ends before product-code changes.

## Source selection

Inspected local upstream snapshots at these commits; this rewrite did not fetch
or claim to inspect newer upstream revisions.

| Source | Useful material | Treatment |
| --- | --- | --- |
| Matt Pocock `3cca18b368ae95cdbdebbff572ccafa662551015` | Codebase-design and improve-codebase-architecture: caller burden, implicit interface obligations, deletion test, evidence of recurring friction. | Retain these judgments. Reject forced vocabulary, automatic fanout and HTML reports, and treating implementation count as sufficient evidence against an interface. |
| Pstack `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Architect, redesign-from-first-principles, exhaust-the-design-space: usage before machinery, genuinely different options, reconsidering the affected design. | Compare credible alternatives against the smallest sound extension. Do not require an arena, a quota of options or prototypes, or permission to rewrite merely because a fresh design is attractive. |
| Superpowers `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Brainstorming: distinguish product uncertainty from feasibility and scale design work to its consequences. | Keep unresolved priorities visible. Reject a universal creative-work trigger, mandatory approval gates, and required spec or commit workflows. |
| Ponytail `974d940a1c5344210874150b98ff0d2c861fab6a` | Ponytail-audit: consider subtraction and existing capabilities. | Use removal as a design comparison. Reject line-count optimization, whole-repository audit scope, and file or implementation counts as proof of waste. |

Local codebase-design, DEEPENING, and DESIGN-IT-TWICE supply most of the useful
method: ordinary caller usage, ownership, interface depth, and comparison with
the current shape. The new entrypoint consolidates those judgments without a
mandatory glossary or fixed number of designs.

Local audit-codebase, DESIGN-LENS, and CANDIDATE-CONTRACT contribute evidence
discipline: demonstrate the cost, distinguish a recurring cause from an isolated
awkward case, and recheck decisive findings. Its repository mapping, report,
selection gates, and tracking procedure remain outside this skill. Retaining
the current design is a legitimate result.

## Conditional context

One integration reference holds three subjects that need more than general
engineering advice:

- State across owners: acceptance versus completion, enforceable authority,
  uncertain remote effects, and authoritative versus derived state.
- Dependencies: useful interface boundaries and the production properties a
  substitute cannot establish.
- Contract migration: old and new consumers, record conversion with concurrent
  writers, temporary compatibility, and rollback limitations.

The entrypoint routes to the relevant section only. It does not duplicate the
prototype build-and-cleanup procedure or the engineering contract's routine
implementation policy.

## Challenger review

Two fresh-context, read-only challengers reviewed the fixed draft independently.
One owned scope, authority, and composition; the other owned substantive design
judgment. Both were asked for concrete failure scenarios rather than a score.

Accepted corrections:

- Limit escalation over a changed guarantee to changes not already authorized.
- If prototype is unavailable, return the framed experiment to authorized
  implementation for execution with available tools. Keep unsupported conclusions
  conditional; design-only work may return the evidence gap.
- Decide when existing records are converted and how concurrent writers affect
  that transition when conversion is needed.
- Remove the reference paragraph duplicating routine migration and regression
  policy already owned by the engineering contract.

The root also made alternative rejection conditional on having compared a
credible alternative, consistent with the rule against invented options.

Both challengers rechecked the final candidate and passed their assigned scopes.
The skill package validator, repository skill validator, local Markdown link
checks, and whitespace checks passed.

The challengers exercised two-service ownership, persisted data with old workers,
misleading substitutes, unsupported architecture smells, design-only requests,
and embedded authorized implementation. This was a textual challenge. A clean
behavioral comparison is still needed before claiming this skill improves
results beyond the engineering contract and model baseline.
