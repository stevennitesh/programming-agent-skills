# Per-Skill Validation

`docs/validation/skills` owns per-skill campaign and evaluation evidence.
Evaluation identities use `EV-<skill-at-mint>-<purpose>-YYYYMMDD-NN`.
Historical migrations preserve original bytes, identities, provenance, and
tested bounds; placement does not admit them into a Fresh Composition Epoch.

New Fresh Deploy campaign manifests live at
`<skill>/campaigns/<campaign-epoch>/manifest.json` and conform to
`../shared/schemas/deploy-campaign-manifest-v2.schema.json`. Keep evaluation
evidence under `<skill>/evals/<evaluation-id>/`; the manifest points to exact
artifact identities and receipts instead of copying evidence or judgments.
Historical manifest v1 records remain readable in place and are never
rewritten as v2.

Each `<skill>/README.md` owns that skill's evaluation index. An `EV-...`
directory is the stable evaluation pointer; member files preserve their exact
protocol, rubric, fixture, result, or retained-evidence role.
