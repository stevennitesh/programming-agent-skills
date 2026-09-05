# Astra shaping and current-route handoff

Date: 2026-09-05. The user directed all projects using the pack to target current
Astra, without preserving legacy execution routes. This change updates source
guidance and the current repository's affected routes. It does not update other
repositories or global installed copies automatically.

## Changes

- Shape-work preserves an explicit request for one ticket; decomposition into
  several items is not required to invoke to-tickets.
- Accepted-source revisions during delivery identify affected commitments,
  tickets, writers and proof. Execution owns pausing affected dispatch and writer
  quiescence; source, acceptance, gates and assignments are reconciled before
  resumption. Unaffected work and evidence remain valid.
- Direct domain updates load the same revision safeguards, not merely the
  publication section. A proposal remains distinct from current accepted meaning
  until coordinated application is settled.
- Bootstrap's domain seed names current Astra shape-work. Bootstrap compatibility
  guidance migrates retired routes and fields instead of preserving alternate
  execution paths. Source/install mismatches are explicit gaps, not fallback routes.
- Current domain and tracker guides, CONTEXT.md and the design brief reflect this
  policy. Historical research and custom source artifacts remain evidence.

## Validation migration

The repository validator previously required a literal retired domain-owner route.
The existing setup checker now accepts an explicit domain-owner argument; the
current repository selects shape-work, and its tests reject replacing that route
with domain-modeling. Historical custom-package tests retain their original source
contract. Active reference validation recognizes present Astra packages without
allowing custom source to depend on them. The setup fingerprint was refreshed.

This is not a wholesale validator/installer migration. The existing setup checker
still validates the repository's current project-lanes configuration and custom
helper presence. Its success does not establish current Astra worker permissions.
The custom-only installer remains unsuitable for deploying Astra; no installation
or blanket project migration was performed.

## Challenger review

Two fresh read-only challengers owned separate seams: shaping/delivery semantics,
and bootstrap/current-route/validation coherence. The first caught the direct
domain path's narrow reference-loading trigger; it was fixed and rechecked. The
second found no blocker and identified the validator scope limitation above.

## Workflow exercise

The previous exercise already covered real concurrent lanes and integrated
tracker closeout. This extension lives under `.tmp/astra-shape-exercise/` and
isolates the previously untested source-to-ticket revision handoff.

The root captured accepted shape revision 1 and published exactly one new JSON
ticket beside already-complete producer/CSV work. A fixture-owner input then
changed the pending JSON outcome from integer cents to an exact signed decimal
amount string. The root made the ticket non-ready, reconciled revision 2 and ticket
acceptance, verified unchanged completed files, then claimed the revised item.
A fresh worker receives only that current source/ticket and owns the JSON module
and its focused test. The root's independent proof includes negative sub-unit
amounts, zero, positive/negative amounts, and an integer exceeding binary-float
precision, while verifying unchanged CSV behavior from the same produced record.

This is a root-orchestrated integration exercise, not a blind test of autonomous
skill selection or a multi-coordinator race. It does not exercise stopping an
already-running affected writer; that boundary was reviewed, while this scenario
revises pending work. Scratch history and state retain evidence locally.

The exercise passed. Initial publication was `c0aea32019029b0a560f7b751924ba71e9b8e0dc`;
withheld readiness at `c34dad7c8bd8d90a66e320c005ed1752fb6938c9`; reconciled revision
2 at `4977e8ad3c3a5ce090823bc5b82374a84e6a6658`; and claimed the verified ticket at
`9c84d92e532e9b2b1cbfe628d40f6d8bb802c86d`. The worker delivered
`7742e6a48fe69f63288ac72bd60a83f49aabb0e7`, with two focused tests covering nine
signed amount cases and identity. Root's five independent producer-to-consumer
cases passed for both the revised JSON and unchanged CSV.

Completion metadata produced `fc941b5a3f31bc10e9e143924a93a3e492d8010d`, changing
only the owned ticket. Producer, CSV implementation, and the unrelated completed
ticket remained byte-identical. Final fixture checkout was clean. Test commits
exist only inside the disposable fixture repository.

Full repository tests passed: 350 passed, 5 skipped. Skill/package validation,
31 affected local links, and both whitespace checks passed. No main-repository
commit, push, or global installation was performed.
