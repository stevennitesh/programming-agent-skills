# Fresh Composition Epoch migration control

Status: active control; 88 migration row(s) verified.

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
- Public migration dispositions: `move` 34, `owner-gap` 132, `preserve-in-place` 313
- Private/local source states: `local-residue` 44, `private-ignored` 26

## Verified migrations

- `MIG-0072` -> `docs/research/skills/to-spec/RP-to-spec-20260724-01.md`
- `MIG-0073` -> `None`
- `MIG-0074` -> `None`
- `MIG-0075` -> `None`
- `MIG-0076` -> `None`
- `MIG-0077` -> `docs/research/skills/convergent-pr-review/RP-convergent-pr-review-20260724-01.md`
- `MIG-0078` -> `docs/research/skills/implement/RP-implement-20260724-02.md`
- `MIG-0079` -> `docs/research/skills/implement/RP-implement-20260724-01.md`
- `MIG-0080` -> `None`
- `MIG-0081` -> `None`
- `MIG-0082` -> `None`
- `MIG-0083` -> `None`
- `MIG-0084` -> `None`
- `MIG-0085` -> `None`
- `MIG-0086` -> `docs/research/skill-pack-composition/sources/SRC-0002.md`
- `MIG-0087` -> `docs/research/skill-pack-composition/sources/SRC-0003.md`
- `MIG-0088` -> `docs/research/skill-pack-composition/sources/SRC-0004.md`
- `MIG-0089` -> `docs/research/skill-pack-composition/sources/SRC-0005.md`
- `MIG-0090` -> `docs/research/skill-pack-composition/sources/SRC-0006.md`
- `MIG-0091` -> `docs/research/skill-pack-composition/sources/SRC-0007.md`
- `MIG-0092` -> `None`
- `MIG-0093` -> `None`
- `MIG-0094` -> `None`
- `MIG-0095` -> `None`
- `MIG-0096` -> `None`
- `MIG-0097` -> `docs/research/skills/parallel-implement/RP-parallel-implement-20260724-02.md`
- `MIG-0098` -> `docs/research/skills/parallel-implement/RP-parallel-implement-20260724-01.md`
- `MIG-0099` -> `docs/research/skills/review/RP-review-20260724-01.md`
- `MIG-0100` -> `None`
- `MIG-0101` -> `docs/research/skills/implement/RP-implement-20260726-01.md`
- `MIG-0102` -> `docs/research/skills/implement/RP-implement-20260726-02.md`
- `MIG-0103` -> `docs/research/skills/to-spec/RP-to-spec-20260725-01.md`
- `MIG-0104` -> `docs/research/skills/to-tickets/RP-to-tickets-20260723-01.md`
- `MIG-0105` -> `None`
- `MIG-0106` -> `None`
- `MIG-0107` -> `docs/research/skill-pack-composition/sources/SRC-0001.md`
- `MIG-0108` -> `None`
- `MIG-0109` -> `None`
- `MIG-0110` -> `None`
- `MIG-0111` -> `docs/research/skills/to-tickets/RP-to-tickets-20260725-01.md`
- `MIG-0112` -> `docs/research/skills/writing-great-skills/RP-writing-great-skills-20260724-01.md`
- `MIG-0113` -> `None`
- `MIG-0114` -> `None`
- `MIG-0115` -> `None`
- `MIG-0116` -> `None`
- `MIG-0117` -> `None`
- `MIG-0118` -> `None`
- `MIG-0119` -> `None`
- `MIG-0120` -> `None`
- `MIG-0121` -> `None`
- `MIG-0122` -> `None`
- `MIG-0123` -> `None`
- `MIG-0124` -> `None`
- `MIG-0125` -> `None`
- `MIG-0126` -> `None`
- `MIG-0127` -> `None`
- `MIG-0128` -> `None`
- `MIG-0129` -> `None`
- `MIG-0130` -> `None`
- `MIG-0131` -> `None`
- `MIG-0132` -> `None`
- `MIG-0133` -> `None`
- `MIG-0134` -> `None`
- `MIG-0135` -> `None`
- `MIG-0136` -> `None`
- `MIG-0137` -> `None`
- `MIG-0138` -> `None`
- `MIG-0139` -> `None`
- `MIG-0140` -> `None`
- `MIG-0141` -> `None`
- `MIG-0142` -> `None`
- `MIG-0143` -> `None`
- `MIG-0144` -> `None`
- `MIG-0145` -> `None`
- `MIG-0146` -> `None`
- `MIG-0147` -> `None`
- `MIG-0148` -> `None`
- `MIG-0149` -> `None`
- `MIG-0150` -> `None`
- `MIG-0151` -> `None`
- `MIG-0159` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/candidate.md`
- `MIG-0160` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/manifest.json`
- `MIG-0161` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt1-m0.md`
- `MIG-0162` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt2-h1.md`
- `MIG-0163` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt3-build.md`
- `MIG-0164` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt4-decision.md`
- `MIG-0165` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/prompt5-final.md`
- `MIG-0166` -> `docs/validation/skills/to-tickets/campaigns/to-tickets-2026-07-25/pruning.md`

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
