# Fresh Composition Epoch migration control

Status: frozen inventory; no migration authorized or performed.

This durable `.scratch/` control implements issue #41 and remains temporary
cross-ticket execution state. It is not research, synthesis, validation, or
runtime authority. The complete private inventory remains only in the ignored
sidecar at `.tmp/fresh-composition-epoch/migration-ledger-private.json`; this tracked closeout deliberately
publishes no private source locators.

## Fixed point

- Source Git HEAD: `338e62adaa964f8ab771d7d060d716f6ce54f7fd`
- Public inventory fingerprint: `sha256-v1:7fb812f56c00b63f4c3b16dcd594a9ea28cca350c2c1c639e88b9de3e43df0f8`
- Private inventory fingerprint: `sha256-v1:ea2a555b40dfca4e3690c56b14975029425a6e71d7edec314eec8e3cb997ce5e`
- Public rows: 472
- Private/local rows: 70
- Public migration dispositions: `extract-and-preserve` 7, `merge-index` 5, `move` 23, `owner-gap` 132, `preserve-in-place` 305
- Private/local source states: `local-residue` 44, `private-ignored` 26

## Contract

Each inventoried artifact has one `MIG-NNNN` row across the tracked ledger and
ignored sidecar. Epoch, Catalog-query, proof-reuse, and migration dispositions
are separate fields. A move or removal requires a recovery pointer and Lock.
No row is `verified`; owner gaps remain explicit. Hash/access failure is
`blocked` and never receives an inferred identity.

Run:

```text
python -m scripts.migration_ledger check
```

The check re-enumerates tracked, untracked, ignored, private, and empty local
residue; recomputes hashes and inbound tracked references; and fails on fixed
point drift, missing/duplicate/stale rows, privacy leakage, or premature proof.
Any new in-scope artifact stales this control before migration.

Source: issues #32, #34, #38, #39, and #41; ADR-0008 and ADR-0009.
