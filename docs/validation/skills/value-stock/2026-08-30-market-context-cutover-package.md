# Market-context cutover package

Status: deployed by stock-valuation ticket 05

This record identifies the canonical `value-stock` package prepared and then
installed by the atomic deployment gate in stock-valuation ticket 05.

## Package identity

- Canonical root: `skills/extra/value-stock/`
- Canonical branch: `main`
- Base commit: `8518c5ba52d2b8b64673b7dfe3481a9708b29102`
- Revalidated cutover tree identity:
  `sha256:19d4aa3dbd79a9777be81b817e3246ea373cb925002b0086aea791a00670fc22`
- Identity algorithm: repository `skill-tree-v1` via
  `scripts.install_skills.skill_tree_hash()`, excluding only generated
  `__pycache__` directories and `.pyc` files.

The prepared package changes `SKILL.md`, `references/analyst-runbook.md`,
`references/compact-report.md`, `references/report-contract.md`, and
`references/valuation-methods.md`, and adds `references/market-context.md`.
Ticket 05 consumes this exact revalidated identity.

## Route contract

- Price-dependent intrinsic valuation requires market context.
- Explicit relative valuation requires market context.
- Intrinsic valuation without price records `not_requested` and avoids market
  data collection.
- Required market context freezes outcome-free selection before outcomes,
  dispositions exactly the five named lanes, and delegates calculation to
  proven typed runtime operations rather than analyst prose.

## Proof

- `python -m pytest tests\test_value_stock_calculator_convenience.py -q`:
  16 passed.
- `python -m scripts.validate_skills`: passed.
- `python -m scripts.install_skills --dry-run`: 27 managed skills, 27
  unchanged, global bootstrap present.
- Installed package before and after the dry run:
  `sha256:21cdf3a7e8b2449fc2f9e91ff153461eaeb6136a8b5265f197f0441a4f03bf68`.

Ticket 05 revalidation found that the earlier recorded identities were not
reproducible under the documented row algorithm. It removed only a generated
`__pycache__`, reran the 14 focused tests, canonical validation, and managed-pack
dry run, then adopted the repository-owned `skill-tree-v1` identity above. The
pre-install installed-package identity under the same algorithm is
`sha256:136362a25dfdff2abe9b30b7a4872741b86c6b881bdfcddf56ed076faa83f9ad`.

## Deployment proof

- Canonical and installed `skill-tree-v1` identities after installation:
  `sha256:19d4aa3dbd79a9777be81b817e3246ea373cb925002b0086aea791a00670fc22`.
- Recoverable pre-cutover backup:
  `C:/Users/steve/.agents/skill-backups/value-stock-before-failure-binding-20260830-2130`.
- Focused three-route contract test: 1 passed.
- Installed semantic route smoke: all three route shapes and typed-operation
  routing passed.
- Full canonical repository test suite: 478 passed, 5 skipped.
- Final skill validation passed. The managed-pack dry run reported 27 managed
  skills unchanged and the global bootstrap present.
- The stock-valuation runtime gate passed 398 tests, Ruff format and lint, MyPy,
  and the active CLI probe before this record was closed.

The final remediation replaced the stale `AnalystAssessmentV2` runbook name
with the active `AnalystAssessment` export, documented exact identity binding
for failed receipts, added negative contract tests, and reinstalled only the
canonical `value-stock` tree. The canonical and installed trees were read back
with the repository-owned hasher and matched the identity above.

No commit or push is part of ticket 05.
