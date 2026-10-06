# Upstream refresh and Astra assessment, 2026-10-06

All ten reference clones in `.tmp/repos/` were refreshed. Nine advanced; Andrej
Karpathy Skills was already current. Every clone finished clean with HEAD equal
to its freshly fetched target. GSD retained `next`; React retained detached HEAD
while advancing to `origin/main`; the other eight retained `main`.

The most useful findings are stronger controls for skill comparisons, checks that
reject plausible but incomplete benchmark work, and enforceable prevention of
repeated mistakes. Most underlying principles already exist in Astra. Prefer
small conditional refinements and useful evaluation cases over additional root
instructions. **Session diagnosis substantially overlaps Matt Pocock's retro;
analyze them as one retrospective workflow and prefer an existing-owner
extension before a new skill.** Package-specific skill generation remains an
optional candidate. Neither has been adopted.

This document records inspected evidence and recommendations. It does not change
the managed pack, installed skills, accepted design, or model policy. The Astra
comparison used the clean source at
`889349f6d6d7626606ebec120c7fb0f0029e796e` and its current
[design brief](../astra/design-brief.md).

## Exact update boundaries

Baselines were captured immediately before fetching, rather than reconstructed
from the previous report. Counts include merge commits and cover each whole
repository; they are not counts of new skills. Baseline dates vary by clone.

| Clone | Target | Before | After | New reachable commits | Changed files |
| --- | --- | --- | --- | ---: | ---: |
| andrej-karpathy-skills | origin/main | `2c60614` | `2c60614` | 0 | 0 |
| cursor-plugins | origin/main | `5bf2b15` | `df58112` | 145 | 234 |
| ECC | origin/main | `ac30ff3` | `ef648e0` | 743 | 1,835 |
| gsd-core | origin/next | `6ee4349` | `13d3723` | 1,391 | 2,893 |
| gstack | origin/main | `a325940` | `c285d88` | 65 | 2,905 |
| mattpocock-skills | origin/main | `3cca18b` | `4588b32` | 44 | 71 |
| ponytail | origin/main | `356918e` | `552acd5` | 89 | 105 |
| react | origin/main, detached | `b685b40` | `278794d` | 108 | 517 |
| skilld | origin/main | `c836844` | `f2f7c4b` | 134 | 540 |
| superpowers | origin/main | `b36e082` | `8ca22db` | 2 | 81 |

The refresh fetched with `git fetch --prune origin`, established ancestry, and
used `git merge --ff-only` for attached branches. React used `git switch --detach`
to the fetched target after the same ancestry and clean-state checks. No resets,
rebases, stashes, or branch deletion were needed. Other fetched branches were
not incorporated into the checkouts.

The first elevated inspection stopped before any fetch because Git's Windows
identity differed from the sandbox owner of ECC. After inspecting the affected
local configurations, the retry used exact, command-scoped `safe.directory`
entries. It changed neither filesystem ownership nor global Git configuration.

Full SHAs, origins, timestamps, status, and target parity are in
[before.json](../../.tmp/upstream-refresh-2026-10-06/before.json) and
[after.json](../../.tmp/upstream-refresh-2026-10-06/after.json). The same local
evidence directory holds complete commit lists, changed paths, diff statistics,
and fetch/update logs for every clone. Those ignored local files accompany this
working copy; the pinned public links below allow independent source inspection.

## What changed

| Repository | Substantive changes in the inspected range |
| --- | --- |
| Andrej Karpathy Skills | No checkout changes. No new lesson can be attributed to this refresh. |
| Cursor Plugins / pstack | Pstack adds `correct`, `benchmark-checklist`, `principle-explain-the-number`, and `poteto-help`; architecture guidance addresses split state ownership, alternative legacy paths, accessible internals, and duplicated lists. It also trims instructions and changes its model defaults. Pstack accounts for 14 commits and 65 changed files in the range; the wider repository adds plugin integrations and changes existing ones. [Comparison](https://github.com/cursor/plugins/compare/5bf2b1544db739998121a306340631963c2ff3de...df581122cde17e6e27686b5a448bde23e4ad4318). |
| ECC | A broad plugin/control-plane expansion, including contract-first collaboration, unified memory, additional specialist skills, installer safety work, and bounded harness evaluation with candidate integrity, paired samples, and rollback machinery. The checked-out VERSION is 2.2.3. This breadth does not establish a reason to import its agent-first pipeline. [Comparison](https://github.com/affaan-m/ECC/compare/ac30ff3ea249bf5f94dbc5e9b18ab681cc9af91d...ef648e01899ba3e8dc6371642deaaf64b4477775), [evaluation addition](https://github.com/affaan-m/ECC/commit/623f2c020f052319657674e4e6c29ab5d0ad566b). |
| GSD Core | The `next` branch advances to package version 1.16.0. Important changes consolidate workflow verdicts and routing, distinguish missing/malformed/stale verification, bind verification to a versioned input set, and fix worker lifecycle, worktree, install, and review-disposition problems. [Comparison](https://github.com/open-gsd/gsd-core/compare/6ee43492723dababa4138ceb72fd2cd26d4325d9...13d37238ba08377929e4850fd6ae4b8db49a22ca). |
| gstack | The checked-out VERSION becomes 1.91.27.0. The range includes test-value auditing, content-bound review evidence, behavioral skill tests and judge calibration, host/install ownership fixes, reduced instruction load, and extensive security-scanner work. Generated host copies, goldens, and fixtures contribute to its large file count. [Comparison](https://github.com/garrytan/gstack/compare/a3259400a366593e0c909dd9ac3e59752efd2488...c285d88b90d39116ccfa2b901f80ea0fce0b26eb). |
| Matt Pocock Skills | Version 1.3.1: graduates `implement-spec`, `pr`, and `retro`; adds experimental `chief-of-staff`; removes its merge-conflict skill; renames its domain-document convention to GLOSSARY; and repairs stale routing. Retro explicitly favors deterministic checks for mechanical mistakes. [Changelog](https://github.com/mattpocock/skills/blob/4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d/CHANGELOG.md). |
| Ponytail | Advances through release 4.13.0. Most changes repair hooks, platform adapters, configuration and state ownership, installation, and benchmark reporting. Particularly useful changes isolate benchmark arms from inherited instructions/memory, preserve an explicit plugin override during self-test, and disclose structural-only checks. [Comparison](https://github.com/DietrichGebert/ponytail/compare/356918eba965ee1eac64bd3a7f0dd02108350de5...552acd5efd0aeae2583a12efe39373d2f076f25e). |
| React | Changes span Compiler, DOM/Fiber, Flight/server rendering, Fragment behavior, and DevTools; the old Timeline profiler is removed. This is implementation reference material rather than a skill pack. API/flag changes require package-version and release-channel evidence before becoming advice for an application. [Comparison](https://github.com/react/react/compare/b685b40d870b90a975da28c8d22ecf0ba910b1a1...278794d7dee9cd2a3a2aaf9f0b2a4b8b747d74ee). |
| skilld | Expands its native Rust CLI, exact remote-source provenance, multi-agent installation/sync, and maintainer-facing package/project skill generation and review. Package generation now requires version-specific consumer examples and distinguishes packaging, discovery, activation, and completion. [Comparison](https://github.com/skilld-dev/skilld/compare/c8368441070e2c0c29af6d2f8c9425f62e8b9afb...f2f7c4b43a468ddd4abc665a85b2785f5f298be3). |
| Superpowers | Two release commits bring 6.4.1 and 6.4.2: transcript-based session inspection, inline plan execution, leaner plans, review scope/evidence fixes, and more host adapters. Claimed efficiency and probe results in its release notes remain upstream reports, not Astra measurements. [Release notes](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/RELEASE-NOTES.md). |

## Lessons worth using

### 1. Verify the instructions each evaluation arm actually receives

Ponytail's benchmark cells lived below its own repository instructions. Its fix
disables inherited instruction files and automatic memory in those cells, and
restores the caller's plugin-directory override after a self-test. Otherwise a
baseline can receive the treatment, or a supposedly pinned run can use another
installed version. The patch establishes the changed mechanics; it does not
retroactively validate earlier reported gains.
[Inspected patch](https://github.com/DietrichGebert/ponytail/commit/e9d4a7ee556ee4dfe184441bb9f7fb63c166d6cd).

**Astra owner:** [Behavior evaluation](../../skills/astra/writing-for-agents/references/behavior-evaluation.md).
Its equivalent-context and attribution rules already apply. A useful refinement
would explicitly check inherited repository/global instructions, memory, hooks,
and installed skill identity when evaluating a skill. Preserve necessary common
task context in every arm. Verify loading instead of assuming a host-specific
environment flag works everywhere.

### 2. A plausible performance number needs proof of completed useful work

Pstack's new benchmark material checks errors, work completion, realistic
configuration, variability, resource limits, and the end-to-end effect. Ponytail
now labels two checks as structural rather than executed behavior. These are
concrete ways a fast or green result can answer a weaker question than intended.
[Benchmark checklist](https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/benchmark-checklist/SKILL.md),
[structural-check disclosure](https://github.com/DietrichGebert/ponytail/commit/7083805a4d923fdda3cad3cbbbc4bab11eb1f20a).

**Astra owners:** [Measurement integrity](../../skills/astra/hillclimb/references/measurement-integrity.md)
and [verification harness](../../skills/astra/verification-harness/SKILL.md).
Both already require useful output and faithful verification. Worth evaluating:
small known-good, known-bad, or no-op controls, plus explicit error and completed-work
counts where those distinguish an invalid win. Keep replication proportional;
do not import a fixed five-run rule or demand profiling for every metric.

### 3. Recurring mistakes should change the mechanism that permits them

Pstack's `correct` orders interventions through ownership/architecture, types,
mechanical checks, behavioral tests, and judgment guidance. Matt's retro now
separates mechanical violations from judgment and checks whether existing tooling
is unwired before adding more prose.
[Correct](https://github.com/cursor/plugins/blob/df581122cde17e6e27686b5a448bde23e4ad4318/pstack/skills/correct/SKILL.md),
[retro patch](https://github.com/mattpocock/skills/commit/0243b6ec4ca02f5a188506d0c0342e3617a7dee1).

**Astra owners:** [Codebase design](../../skills/astra/codebase-design/SKILL.md)
and [context hygiene](../../skills/astra/context-hygiene/SKILL.md).
They already favor enforceable ownership and existing mechanical enforcement.
Retain this direction; a useful future example would demonstrate a proposed check
rejecting an authentic previous mistake while allowing a valid case. Do not adopt
automatic redesign after every correction, mandatory commits, or a new global
rule table. Evidence and authorized scope still determine the intervention.

### 4. Verification has identity, scope, and failure states

GSD closes its status vocabulary and centralizes routing. Its fingerprint uses a
shared input calculation, excludes the report itself, and retains stored-version
semantics. gstack binds reusable review evidence to the reviewed content and
branch. These mechanisms address different failures: stale results, self-induced
staleness, incorrect retry routes, and evidence reused for changed work.
[GSD verdict decision](https://github.com/open-gsd/gsd-core/blob/13d37238ba08377929e4850fd6ae4b8db49a22ca/docs/adr/5057-one-owner-per-workflow-verdict.md),
[verification implementation](https://github.com/open-gsd/gsd-core/blob/13d37238ba08377929e4850fd6ae4b8db49a22ca/src/verification.cts),
[gstack review binding](https://github.com/garrytan/gstack/commit/85b8c038fc0002a1549789ea018e924c1d335de4).

**Astra owners:** [Change review](../../skills/astra/change-review/SKILL.md),
[parallel implement](../../skills/astra/parallel-implement/SKILL.md), and
verification harness already require candidate identity and applicable evidence.
Keep these contracts. For tooling that caches a verdict, test changed inputs,
empty scope, malformed evidence, and an actual failing result. Introduce hashes
or closed enums only where persisted reuse or consumer routing creates the need.

### 5. Test value follows the regression it detects

gstack's new test-audit material asks which behavior a test protects, which
credible regression breaks it, whether coverage already exists, and whether it
requires a production seam used only by tests. It also recognizes legitimate
machine-consumed byte contracts and warns that text search alone cannot prove
code is unused.
[Test value bar](https://github.com/garrytan/gstack/blob/c285d88b90d39116ccfa2b901f80ea0fce0b26eb/docs/test-value-bar.md).

**Astra owners:** repository test policy, [audit codebase](../../skills/astra/audit-codebase/SKILL.md),
and change review. Already substantially covered. Use the regression questions
as a scoped audit lens; retain real packaging, protocol, schema, security, and
installation checks. Do not add rating cards, coverage scores, or a separate
test-audit skill without a repeated workflow gap.

### 6. Package advice should be exercised as a consumer of that version

skilld's package authoring skill builds a minimal consumer, uses the recorded
package and peer versions, checks relevant export/runtime modes, runs included
examples, and reports documentation discrepancies and untested examples. This
can reveal assumptions hidden by a package repository's own configuration.
[Package generation](https://github.com/skilld-dev/skilld/blob/f2f7c4b43a468ddd4abc665a85b2785f5f298be3/skills/generate-package-skill/SKILL.md).

**Astra owners:** [Skill authoring](../../skills/astra/writing-for-agents/references/skill-authoring.md),
research's repository mapping, and verification harness. A conditional package
authoring reference is a plausible small addition if this work recurs. It should
distinguish authoring examples from observed host activation and leave package
bug fixes outside an authoring-only assignment.

### 7. Plans can preserve decisions without prescribing implementation bodies

Superpowers replaces full-code plans with interfaces, assertions, accepted values,
and checks, retaining algorithm detail when genuinely needed. Pstack also removes
instructions its target model reportedly follows without them. The transferable
idea is to preserve missing decisions and real boundaries while removing redundant
method prescriptions. Their reported cost effects need equivalent Astra trials.
[Superpowers planning changes](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/RELEASE-NOTES.md),
[pstack subtraction](https://github.com/cursor/plugins/commit/b0b9c7a0baf8b6aa1d00bf77d4101e577d4ba411).

**Astra owner:** writing-for-agents. Its capable-receiver and discretionary-method
direction already covers this. No additional planning phase or pack rewrite is
justified by these updates.

## Candidates and existing-owner overlap

| Candidate | Assessment | Distinct boundary and next evidence |
| --- | --- | --- |
| **Session retrospective / diagnosis** | **Analyze together; extend an existing owner first.** Matt's retro and Superpowers' diagnosis share session evidence and retrospective investigation. | Matt seeks improvements to the agent's environment; Superpowers formalizes evidence attribution and reporting. Prefer a conditional session-retrospective reference under context-hygiene. A standalone skill needs evidence that this extension leaves a distinct, recurring workflow unmet. |
| **Package-skill generation** | Secondary, optional package. | A maintained library version and its consumer-facing skill are the input/output. skilld supplies a substantive method, but general authoring and verification already own much of it. Test one real package case before making this a managed Astra skill. |
| Chief of staff / continuous project coordination | Watch, withhold adoption. | Matt's new experimental skill coordinates a long-running goal through subagents and schedules. It supplies no detailed completion, budget, recovery, or authority contract. Astra already has cost-aware delivery, lane custody, and long-running handoff rules; require a demonstrated strategic-coordination gap before adding another controller. |
| Correct, benchmark checklist, test audit, contract first, PR format | Existing-owner refinement first. | Their useful concepts map to design, measurement, audit/review, integration, and communication. A useful format or checklist alone does not establish a distinct workflow needing another discovery entry. |

Matt's retro already reads primary session sources, including logs, and investigates
navigation, checks, standards, instruction load, tool economy, no-op guidance, and
information access. Superpowers supplies more explicit transcript identity,
historical provenance, bounded extraction, and export controls, while restricting
its output to reporting involvement for a triager. These are different emphases
within substantially the same retrospective task. The original recommendation
overstated session diagnosis as a distinct new skill; additional evidence-handling
detail does not by itself justify another discovery entry.
[Matt's retro](https://github.com/mattpocock/skills/blob/4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d/skills/engineering/retro/SKILL.md).

For a combined retrospective workflow, borrow source attribution, bounded field extraction,
historical-versus-current skill provenance, and the distinction between direct
human input, injected messages, and parent dispatches. A tool request's acceptance
must be distinguished from its result. Handle source transcripts read-only and
keep private source material local; export and publication require their own
authorization. Do not copy Superpowers' mandatory seven analysts, serial intake
for an already-clear request, or prohibition on offering a supported correction.
[Source workflow](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/diagnosing-superpowers/SKILL.md),
[bounded reads](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/diagnosing-superpowers/references/context-safety.md),
[provenance template](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/diagnosing-superpowers/templates/case.md).

A useful bounded evaluation of the existing-owner extension would include: a failed skill load followed by direct
execution; duplicated work after compaction; a queued asynchronous action mistaken
for completion; and a successful session where no material workflow defect should
be invented. Check attribution and justified conclusions before comparing tokens
or elapsed time. Missing cost counters should remain unavailable.

The follow-up [comparison and context-hygiene proposal](context-hygiene-session-retrospective-2026-10-06.md)
contains the combined workflow draft, Astra and Opus 5.5 alignment, ownership,
and proposed behavioral evaluation cases. It remains a proposal.

## Adoption boundaries and verification limits

Do not import upstream model defaults, compulsory delegation/TDD, automatic
schedules, filename migrations, universal production/security checklists, or
automatic commits. Matt's removal of its conflict skill does not establish that
Astra's distinct preservation and operation-identity contract should be removed.
ECC's useful contract-first caution allows a shared type for a boundary changed
atomically; it does not justify contract-generation infrastructure everywhere.
[Chief-of-staff source](https://github.com/mattpocock/skills/blob/4588b32ecab9ecc9fc8cc6b6c5e7d675b6004b0d/skills/in-progress/chief-of-staff/SKILL.md),
[ECC contract first](https://github.com/affaan-m/ECC/blob/ef648e01899ba3e8dc6371642deaaf64b4477775/skills/contract-first/SKILL.md).

Coverage included the complete saved commit/path inventories, release material,
and selected decisive skill, implementation, and test sources. Large ECC, GSD,
gstack, plugin, and React deltas were screened, not audited file by file. Examples
include GSD's verification owner/status tests, gstack's review-binding library
and test-value policy, ECC's candidate/paired-evaluation code, and Ponytail's
benchmark isolation patch. Test source describes intended assertions; no upstream
suite, paid model comparison, or live adapter test was run.

Git exit results, ancestry, update success, branch mode, clean status, fetched
target equality, and final checkout identity were checked. Both parent repository
whitespace checks passed after writing this report. No runtime skill source was
changed, so package validation or behavioral efficacy cannot be claimed from this
documentation-only assessment. The report remains uncommitted.
