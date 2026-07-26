# Fresh Composition Epoch migration control

Status: frozen inventory; no migration authorized or performed.

This durable `.scratch/` control implements issue #41 and remains temporary
cross-ticket execution state. It is not research, synthesis, validation, or
runtime authority. The complete private inventory remains only in the ignored
sidecar at `.tmp/fresh-composition-epoch/migration-ledger-private.json`; this tracked closeout deliberately
publishes no private source locators.

## Fixed point

- Source Git HEAD: `f2fe6d3342781ac6e7031c553d5493f84da8d15f`
- Public inventory fingerprint: `sha256-v1:6d590c2d9de4a060b22e698bbf438130916ae8dcc54ca300f284988a5e51b08d`
- Private inventory fingerprint: `sha256-v1:ea2a555b40dfca4e3690c56b14975029425a6e71d7edec314eec8e3cb997ce5e`
- Public rows: 476
- Private/local rows: 70
- Public migration dispositions: `extract-and-preserve` 7, `merge-index` 5, `move` 23, `owner-gap` 132, `preserve-in-place` 309
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
