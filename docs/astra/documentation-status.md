# Documentation reconciliation status

Inspected 2026-09-07. This is a bounded review of the reader-facing entry points,
agent routes, plans, ADRs, and referenced research/synthesis; it is not an audit
of every historical packet or external project. The [design brief](design-brief.md)
owns current direction. Do not treat this inventory as an execution backlog.

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
