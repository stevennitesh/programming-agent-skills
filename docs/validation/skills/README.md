# Per-Skill Validation

`docs/validation/skills` owns per-skill historical campaign and current
evaluation evidence.
Evaluation identities use `EV-<skill-at-mint>-<purpose>-YYYYMMDD-NN`.
Historical migrations preserve original bytes, identities, provenance, and
tested bounds; placement does not admit them into a Fresh Composition Epoch.

Historical campaign directories are inert records and have no supported schema
or reader. Keep current evaluation evidence under
`<skill>/evals/<evaluation-id>/`.

Each `<skill>/README.md` owns that skill's evaluation index. An `EV-...`
directory is the stable evaluation pointer; member files preserve their exact
protocol, rubric, fixture, result, or retained-evidence role.
