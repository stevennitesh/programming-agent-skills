# Audit Codebase Validation

This directory owns historical and fresh per-skill validation for
`audit-codebase`. Evaluation directories use stable `EV-...` identities.

Evaluation directories are immutable evidence for the exact bytes recorded by
their locks. They are current proof only while those hashes match the canonical
package; otherwise they remain historical or superseded contribution evidence.
`docs/validation/evals/core-workflows.md` owns the current reusable workflow
contract, and focused executable tests own the current helper/schema contract.
