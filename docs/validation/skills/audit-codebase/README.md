# Audit Codebase Validation

This directory owns historical and fresh per-skill validation for
`audit-codebase`. Evaluation directories use stable `EV-...` identities.

Evaluation directories are immutable evidence for the exact bytes recorded by
their locks. They are current proof only while those hashes match the canonical
package; otherwise they remain historical or superseded contribution evidence.
`docs/validation/evals/core-workflows.md` preserves historical pack-level
evidence. Fresh Audit Codebase proof belongs in the indexed `EV-...`
evaluations; focused executable tests own the current helper/schema contract.

Current evaluation:

- [`EV-audit-codebase-delegation-gate-20260812-01`](evals/EV-audit-codebase-delegation-gate-20260812-01/decision.md):
  `reject-no-control-deficit`; the shared delegation gate already prevented
  optional fanout in all five pre-change controls.
