# Archived Fresh Composition Epoch migration control

This directory preserves the tracked migration control for the legacy Fresh
Composition Epoch workflow. It is historical evidence and compatibility tooling,
not current Astra routing or a required step for ordinary maintenance.

- `migration-ledger.json` preserves the large public migration ledger at a stable
  archived location.
- `legacy-closeout.md` preserves the generated closeout that previously lived
  under root `.scratch/`.
- `scripts/migration_ledger.py` and its tests retain the explicit legacy
  maintenance path.

For current pack composition and ownership, use
[`docs/astra/design-brief.md`](../../docs/astra/design-brief.md) and
[`skills/astra/`](../../skills/astra/).
