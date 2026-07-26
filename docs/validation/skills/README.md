# Per-Skill Validation

`docs/validation/skills` owns fresh per-skill campaign and evaluation evidence.
Evaluation identities use `EV-<skill-at-mint>-<purpose>-YYYYMMDD-NN`.
Historical validation remains readable in place until a separately authorized
migration reconciles it.

New Fresh Deploy campaign manifests live at
`<skill>/campaigns/<campaign-epoch>/manifest.json` and conform to
`../shared/schemas/deploy-campaign-manifest-v2.schema.json`. Keep evaluation
evidence under `<skill>/evals/<evaluation-id>/`; the manifest points to exact
artifact identities and receipts instead of copying evidence or judgments.
Historical manifest v1 records remain readable in place and are never
rewritten as v2.
