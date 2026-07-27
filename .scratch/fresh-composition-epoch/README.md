# Fresh Composition Epoch migration control

Status: active control; 1 migration row(s) verified.

This durable `.scratch/` control implements issue #41 and remains temporary
cross-ticket execution state. It is not research, synthesis, validation, or
runtime authority. The complete private inventory remains only in the ignored
sidecar at `.tmp/fresh-composition-epoch/migration-ledger-private.json`; this tracked closeout deliberately
publishes no private source locators.

## Fixed point

- Source Git HEAD: `2397586d4bbb0774d9b479ccff9f8a5640df705e`
- Public inventory fingerprint: `sha256-v1:142696879766074cb49dd023ed738d20887fe0b8b6fef3e74a20c06c71d3e122`
- Private inventory fingerprint: `sha256-v1:ea2a555b40dfca4e3690c56b14975029425a6e71d7edec314eec8e3cb997ce5e`
- Public rows: 479
- Private/local rows: 70
- Public migration dispositions: `extract-and-preserve` 7, `merge-index` 5, `move` 24, `owner-gap` 132, `preserve-in-place` 311
- Private/local source states: `local-residue` 44, `private-ignored` 26

## Verified migrations

- `MIG-0107` -> `docs/research/skill-pack-composition/sources/SRC-0001.md`

## Contract

Each inventoried artifact has one `MIG-NNNN` row across the tracked ledger and
ignored sidecar. Epoch, Catalog-query, proof-reuse, and migration dispositions
are separate fields. A move or removal requires a recovery pointer and Lock.
Only the listed rows are `verified`; every other row remains pending. Hash/access failure is `blocked` and never receives
an inferred identity.

Run:

```text
python -m scripts.migration_ledger check
```

The check re-enumerates tracked, untracked, ignored, private, and empty local
residue; verifies unchanged public content and each applied target; and fails
on unexplained path/content drift, missing/duplicate/stale rows, privacy
leakage, or premature proof.

Source: issues #32, #34, #38, #39, #41, and #46; ADR-0008 and ADR-0009.
