# Documentation reconciliation status

Initial inspection 2026-09-07; public entry-point follow-up 2026-09-23. This is a
bounded review of the reader-facing entry points, agent routes, plans, ADRs, and
referenced research/synthesis; it is not an audit of every historical packet or
external project. The [design brief](design-brief.md) owns current direction. Do
not treat this inventory as an execution backlog.

## Public-release cleanup, 2026-09-23

Audited root metadata, tracked workspace state, local/scratch artifacts,
contribution guidance, dependency declarations, and release verification.

Removed the tracked machine-specific `.codex/config.toml` and unreferenced
`.diagram-design` profile and added ignore rules so those local tool settings
do not re-enter the repository. The former Fresh Composition Epoch migration
control was preserved but moved from root `.scratch/` into
`.archive/fresh-composition-epoch/`; its original generated closeout is kept as
historical evidence while a small archive README makes its legacy scope explicit.
The legacy migration tool/tests now use the archived path.

Added `CONTRIBUTING.md` with the current Astra source/legacy boundary and the
small validation path expected of contributors. Added GitHub Actions CI on Linux
and Windows using Python 3.11; it runs the repository public-readiness validator
and the full pytest suite serially for deterministic filesystem/transaction
coverage.

The public validator now requires the contribution guide and CI workflow, scans
the contributor guide as a current surface, and treats reserved synthetic
`@example.invalid` fixture addresses as examples rather than secret leakage.
Its local-identifier/secret heuristic is scoped to current public/runtime
surfaces rather than preserved historical research, synthesis, validation, and
test fixtures; the first CI run exposed that distinction by correctly surfacing
old machine-path provenance as a false release blocker. The CI workflow uses the
current Node-24/ESM GitHub Actions majors. The development dependency set remains
warranted by current plus explicitly retained legacy tests; no dependency removal
was justified in this pass.

## Installer architecture audit, 2026-09-23

Reviewed `scripts/install_skills.py` and its installer tests for source
selection, ownership, idempotence, migration, target topology, transaction
preparation, atomic displacement, rollback, crash recovery, and global-bootstrap
updates.

The transaction/recovery machinery is large but materially justified: it protects
modified managed copies, unrelated skills, multi-target locking, partial swaps,
retirements, manifest/global updates, interrupted state writes, rollback
quarantines, and recovery identity. No broad rewrite was made.

The changes instead harden boundaries the transaction previously trusted too
long. The installer now rejects missing/empty Astra source packs and source skill
directories without `SKILL.md`, rejects link/reparse redirects in the managed
source, global template, and installed manifest before reading them, and refuses
to interpret an incomplete checkout as a request to retire every managed skill.

Live managed-skill, manifest, and global-AGENTS identities are rechecked after
snapshots and again immediately before their corresponding mutations. Skill
replacement and retirement also verify the displaced tree against the last
accepted cache-insensitive identity, preventing a concurrent non-cache edit from
being silently quarantined and discarded.

Global bootstrap content is now rendered once during planning and those exact
planned bytes are committed. The commit phase no longer re-renders a potentially
changed source template. A source change during installation therefore becomes a
later update rather than mixing source epochs inside one transaction.

Recovery now honors the existing `--json` flag with a small stable recovery
payload. Installation documentation was reconciled with these guarantees.

## Validator and repository-code audit, 2026-09-23

Reviewed the default validator, focused pytest wrapper, current package contracts,
installed-pack parity checks, and adjacent repository tests for correctness,
robustness, stale ownership, and avoidable duplication.

The main defect was ownership drift: `python -m scripts.validate_skills` still
unconditionally imported and executed retained custom/experimental, Fresh
Composition Epoch, legacy synthesis/integration, legacy repo-bootstrap schema, and
research-catalog validators even though `skills/astra/` is the only managed pack.
Those checks now run only with explicit `--legacy`. The default path validates
current Astra packages, README/example parity, current required guidance, current
stale-token surfaces, global bootstrap, optional installed parity, repository
Markdown hygiene, public checks when requested, and Git diff hygiene. Legacy
modules are imported lazily so a historical helper failure cannot prevent current
Astra validation from starting.

The validator also now parses SKILL frontmatter and host metadata as YAML rather
than treating frontmatter and required policy files as line-oriented regex data.
Non-string names/descriptions fail cleanly instead of risking type errors, folded
YAML descriptions are accepted, malformed metadata is rejected, and the
invocation key is still required exactly once when policy is required.

The focused pytest wrapper now targets current validator/Astra tests instead of
the historical custom-pack contract suite. `AGENTS.md` documents the default
Astra validator and the explicit `--legacy` extension.

A duplicate parametrized installer test with the same Python function name and
body was also removed. The second definition had replaced the first at import
time, so the duplicate source added no test coverage. A repository-wide scan of
top-level Python function names found no other duplicate definitions in
`scripts/` or `tests/`.

## Canonical skill-selection examples, 2026-09-23

Added [selection-examples.md](selection-examples.md) as one compact discovery
boundary specification for all 18 managed Astra skills. Each row contains one
representative eligible request, the behavior that skill should own, and the
nearest realistic non-match.

The examples remain outside runtime skill bodies so normal invocations do not pay
for duplicated teaching text. Frontmatter descriptions remain host-facing
discovery authority and each `SKILL.md` remains execution authority. The examples
serve maintainers, reviewers, and future discovery evaluations.

The validator now requires exactly one example row per managed Astra skill and
checks skill/link parity, so adding, retiring, or renaming a skill cannot silently
leave this selection surface stale. The README and design brief link to the
examples without turning them into a required workflow.

## README and discoverability pass, 2026-09-23

Reorganized the public README around the newcomer path: install first, understand
the distinction between repository guidance/direct coding/specialist skills, then
select a skill. The complete 18-skill catalog and invocation labels remain
unchanged as a machine-validated contract.

The previous README put installation after a long example and embedded detailed
cost-aware worker policy, effort escalation, recovery, and telemetry guidance.
Those mechanics now stay with the owning skill. The README retains only the
stable cost-aware roles and its composition boundary with parallel-implement.
It also makes explicit that ordinary bounded implementation is the default and
that examples are not a required pipeline.

## Astra package consistency audit, 2026-09-23

Audited all 18 managed Astra packages for directory/frontmatter identity,
selection descriptions, Codex invocation metadata, package-local resources, and
public catalog consistency.

The existing package shape is intentionally not uniform beyond its contract.
Every skill has a matching `SKILL.md` name and nonempty description. The 11
explicit-only skills are exactly the packages that set
`policy.allow_implicit_invocation: false`; the seven automatically selectable
skills omit `agents/openai.yaml` and use Codex's implicit default. Four
explicit-only skills also carry optional launcher interface metadata where a
custom display/default prompt is useful. References, scripts, and templates
remain capability-specific rather than mandatory empty scaffolding.

The consistency gap was enforcement rather than package content. The validator
now checks that every managed Astra skill appears exactly once in the README
catalog, each catalog link resolves to the same skill name, and its
`Request explicitly` / `Automatic when relevant` label agrees with effective
Codex metadata. It also validates known optional interface fields as nonempty
strings when present. Regression tests cover valid parity, mode drift, duplicate,
missing, unknown, and mismatched-link entries, plus malformed interface metadata.

No skill package was padded or rewritten merely for visual uniformity.

## Current-vs-historical cleanup, 2026-09-23

Audited current routers and owners for stale counts, retired skill names,
superseded workflows, installation directions, and abandoned design proposals.
The current managed set is defined mechanically by immediate
`skills/astra/*/SKILL.md` entries; this branch has **18**. Historical counts and
retired names remain evidence and must not be used as current inventory.

Changes from this pass:

- moved the explicitly requested legacy Deploy Campaign route out of **Current
  Runbooks**;
- added a direct historical-scope notice to `docs/synthesis/skill-pack.md`, whose
  recorded 24/25-skill composition and "active" terminology are legacy;
- relabeled synthesis/method index sections so their Deploy Campaign instructions
  cannot read like current Astra routing;
- changed residual "active/current" wording inside the legacy-pack vocabulary to
  legacy-scoped wording;
- made `CONTEXT.md` state how to derive the managed inventory instead of trusting
  counts in historical artifacts; and
- aligned the design brief with the README: the historical custom pack is more
  detailed, but there is not current comparative evidence that smaller models
  perform better with it.

The installer source and `INSTALLATION.md` remain consistent: `skills/astra/`
is the only managed skill source, old custom manifests are migration evidence,
and the documented preview/install/recovery route still matches the installer.
No installation rewrite was warranted. Dated research proposals, numbered ADR
bodies, validation results, and archived records keep their original counts,
names, and conclusions when their historical scope is already explicit.

## Public entry-point follow-up, 2026-09-23

Rechecked the README, repository instructions, root context, installation guide,
Astra design brief, plan/domain/tracker routes, ADR index and applicability record,
and all 18 managed Astra skill entry points against pre-change branch HEAD
`64c82a96`.

The current navigation model remains intentionally small: `AGENTS.md` supplies
commands and conditional pointers, `CONTEXT.md` owns repository/source boundaries,
the Astra design brief owns current composition rationale, and each
`skills/astra/*/SKILL.md` owns execution. No additional context layer or required
workflow was introduced.

This pass corrected public README text encoding, made the historical custom pack's
non-managed status explicit, labeled Deploy Campaign as an explicitly requested
legacy route in repository instructions, and replaced stale GPT 5.6 Sol wording in
ADR-0018 with the current optional GPT 6 Sol/Luna cost-aware roles. The README's
18-skill inventory matches the managed Astra entry points and their invocation
boundaries.

| Surface | Finding and disposition |
| --- | --- |
| Design brief | Reconciled current Astra/Sol positioning, implemented composition, cost-aware gates, migration, and remaining evaluation questions. Removed obsolete rewrite-order and managed-custom claims. |
| Issue #94 | Original proposal remains evidence. A dated reconciliation note identifies superseded pilot/inventory directions and current owners; broader comparative acceptance remains open. |
| `CONTEXT.md` and domain route | Added target-model positioning and routed ADR selection through a scope index. |
| `docs/adr/0001`–`0017` | Preserve bodies. Added an index explaining applicability; old Implement, To Spec, review and worker routes must not override current Astra owners. |
| Former `docs/plans/engineering-vocabulary-reconciliation.md` | Archived to [root archive](../../.archive/docs/plans/engineering-vocabulary-reconciliation.md). Original claims preserved; four relative evidence links rebased. Plans index now routes to the archive. |
| `docs/synthesis/README.md` | Reconciled its legacy scope and descriptions of composition/relationship owners. |
| `docs/synthesis/skill-pack.md` and `skill-context-relationships.md` | Retain as legacy composition evidence. The first freezes an older inventory; the second explicitly maps custom routes and includes old global-template relationships. Neither is current Astra composition. Avoid moving them without auditing validation/evidence references. |
| `docs/agents/legacy-pack-context.md` | Corrected the implication that custom skills remain eligible for today's managed installation. Historical vocabulary remains available. |
| Initial Astra assessment, 2026-09-05 | Retain as a dated proposal: its four-skill and later candidate inventories do not represent current adoption. Already points to the design brief. |
| Astra engineering-contract assessment, 2026-09-05 | Retain as a snapshot. Its statement that Astra is outside managed installation was true of the recorded candidate, not the current repository. Research index now makes this boundary explicit. |
| Research, synthesis, validation packets and run logs | Preserve historical evidence in place. Index-level scope is preferable to rewriting results or breaking provenance links. |
| README and INSTALLATION | README was reconciled with current cost-aware behavior and Astra/Sol positioning; installation ownership remains consistent with the managed installer. No further installation rewrite identified. |
| Engineering contract, tracker and label guidance | No conflicting current route found in this pass; retain local owners. |

## Context-hygiene follow-up, 2026-09-07

Applied the authorized repo-local cleanup. The selected follow-up set below is
12 source surfaces and 12 disposition claims: **6 keep, 6 migrate, 0 generalize,
0 expire, 0 review**. Migrate includes moving a stale applicability claim to its
proper legacy scope; it does not imply every file moved. Prior reconciliations
above remain part of this working tree.

| Source surface / claim | Kind and owner | Disposition and verified destination |
| --- | --- | --- |
| `AGENTS.md`: current commands and conditional loading | Repository procedure; local instructions | Keep. Commands and routes still point to current owners; no extra skill pipeline added. |
| `GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md`: route/setup/boundary | Global bootstrap seed; installer | Keep. Already leaves project facts and engineering procedures local. |
| `AGENTS_PORTABLE_FALLBACK.md`: direct coding without the pack | Standalone alternative; portable seed | Keep. Its stated uninstalled scope avoids competing with specialist runtime guidance. |
| `.codex/config.toml`: workspace permissions and runtime settings | Local configuration; host | Keep. No legacy skill or model route found. No global or host configuration changed. |
| Completed vocabulary-reconciliation plan: old delivery deferrals | Historical event; archive | Migrate to `.archive/docs/plans/`; current plan index updated. Text preserved except four rebased evidence links. No code/test consumer found for its former path. |
| `docs/synthesis/methods/README.md`: epoch/campaign applicability | Procedure router; legacy methods | Migrate applicability to explicitly selected legacy scope, with a current Astra pointer. Preserve optional source-distillation method. |
| `docs/research/skills/README.md`: retired skill names as packet owners | Evidence router; legacy research | Migrate interpretation to historical provenance, not active invocation. |
| `docs/validation/README.md`: future/general pack-validation wording | Evidence router; validation | Migrate to scoped evidence already present; legacy campaigns do not establish present pack-wide gains or required workflows. |
| `docs/validation/shared/README.md`: shared epoch contracts | Mechanical context; epoch helpers | Migrate loading scope to legacy consumers; retain files and links for tests. |
| `docs/validation/skill-pack/README.md`: epoch integration protocol | Procedure/evidence router; epoch helpers | Migrate applicability to legacy scope with current Astra pointer. |
| `docs/synthesis/skill-pack.md`: frozen composition | Historical contract; legacy scripts | Keep in place. `fresh_epoch_contract.py`, `pack_contract.py`, and tests consume this exact path; no current Astra adoption implied. |
| `docs/synthesis/skill-context-relationships.md`: custom relationship map | Historical topology; validator and legacy scripts | Keep in place. Validator, integration helpers, and tests consume the path; current scope is explained by the synthesis index. |

The archive retains its historical assertions and completion evidence. No history
was deleted, no new enforcement machinery was added, and no global memory,
installed skills, external project, or tracker was changed by this follow-up.

Coverage limits: entry points and relevant claims were inspected, not every
research packet, numbered ADR body, archived transcript, or historical run result.
The ADR index scopes old records but does not re-ratify them. Ignored `.tmp`, caches,
captures, and scratch trees were not treated as persistent instruction owners and
were not removed. Other skill bodies were not broadly re-audited. Retain these
sources as evidence unless a later targeted pass establishes a safe migration.


## Focused ADR reconciliation, 2026-09-07

Subsequently inspected ADRs 0001–0017 and reconciled their applicability through
[ADR-0018](../adr/0018-astra-composition-and-decision-applicability.md).
Each predecessor now starts with its retained, superseded, or legacy-only scope;
original bodies remain unchanged. The ADR index routes by task, and domain
guidance loads history only when rationale or applicability is needed. This
extends the earlier entry-point audit to the numbered ADR bodies, without
re-auditing historical research or changing the skill procedures.
