# What distinctive, operationally meaningful language and vocabulary does the Ponytail skill pack use?

Status: answered
Supports: later vocabulary synthesis without selecting canonical local terms or editing runtime skills
Scope: complete Ponytail checkout, including skills, adapters, commands, hooks, metadata, examples, tests, benchmarks, and human-facing documentation
Freshness: checkout state verified 2026-07-22 at commit `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`

## Question And Boundary

This packet asks what language Ponytail uses to route work, choose a solution,
mark deliberate shortcuts, evaluate results, and stop. Ponytail is primary
evidence only for its own vocabulary and behavior. The packet does not judge
that vocabulary universally correct, select local canonical language, draft
skill wording, or authorize edits to vocabulary owners or runtime skills.

The complete tracked checkout is included. Six PNG assets are classified
`not-applicable` because they contain no inspectable textual contract; the five
SVG assets were inspected. Generated copies and translated documentation were
checked for drift, not counted as independent authority. Compatibility claims
in the platform catalog and performance claims in benchmark reports are
descriptive of this revision, not externally verified guarantees.

Ponytail vocabulary was extracted before comparison with `CONTEXT.md`,
`docs/agents/engineering-contract.md`,
`docs/research/language/03-high-signal-steering-words.md`, and
`docs/research/language/04-agentic-bridge-vocabulary.md`. Every local comparison
below is labeled `synthesis` or `inference`.

## Source Identity

| Pack | Origin | Revision | Worktree State | Verified | Authority | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| Ponytail | `https://github.com/DietrichGebert/ponytail` | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; branch `main` tracking local `origin/main` at `+0/-0` | Clean; no modified, untracked, or ignored checkout files | 2026-07-22 | The checked-out repository is primary evidence for its own language and implementation | No fetch was performed. Equality with `origin/main` describes the existing local remote-tracking ref, not a fresh claim about the live remote. |

## Coverage

The checkout contains 156 tracked files. The categories below are mutually
exclusive and account for the whole tree.

| Surface | Inspected / Skipped / Not Applicable | Files Or Count | Consequence |
| --- | --- | --- | --- |
| Canonical skills | Inspected | 6 `skills/ponytail*/SKILL.md` files | Primary authority for the mode, ladder, specialized reports, boundaries, and output contracts. |
| Generated skill mirrors | Inspected | 6 `.openclaw/skills/*/SKILL.md` files | Bodies match the canonical skills; rewritten frontmatter was checked for lost routing detail. |
| Commands | Inspected | 12 Claude/Gemini TOML and OpenCode Markdown command files | Short command summaries sometimes omit canonical ladder rungs or qualifications. |
| Runtime adapters | Inspected | 22 hook, OpenCode, Pi, and MCP files | Defines activation, persistence, injection, status, subagent propagation, and host-specific collisions. |
| Scripts | Inspected | 5 files | Interfaces, messages, comments, copy checks, version gates, publishing, and owned cleanup were vocabulary-bearing. |
| Tests | Inspected | 14 files | Establishes mode branches, copy parity, conservative cleanup, and several behavioral distinctions. |
| Benchmarks | Inspected | 35 code, config, prompt, control, README, and result files | Defines behavior gates, evidence tiers, baselines, judge trust, known-good/bad controls, and limitations. Superseded results remain historical evidence only. |
| Human-facing docs | Inspected | 7 root/translated README, install, portability, platform, and agent-rule files | Establishes the pack identity, portability model, public command family, and platform-native examples. |
| Examples | Inspected | 12 Markdown files | Demonstrates replacement and `Skipped`/`Add when` reporting; model-generated examples are illustrative, not normative. |
| Metadata and config | Inspected | 26 manifests, host rules, workflows, package/config files, and root support files | Seven host rules mirror `AGENTS.md`; other files establish routing and distribution vocabulary. Generic manifest syntax was pruned. |
| Assets | Inspected / Not Applicable | 5 textual SVGs inspected; 6 PNGs not applicable | SVG labels added no unique operational term. PNGs do not expose an inspectable textual contract. |

The root `.gitignore` ignores `.tmp/*`; no raw term list, concordance, frequency
report, or copied corpus was persisted. `.tmp/vocabulary/ponytail/` did not
exist before or after extraction.

## Vocabulary Clusters

### 1. Minimum-solution selection

Ponytail presents itself as a **lazy senior developer**, where lazy means
efficient rather than careless. Its central mechanism is **the ladder**: an
ordered elimination test that stops at the **first rung that holds**. The rungs
move from not building, through reuse and already-available capabilities, to
the minimum new code. A **higher rung** is the earlier, less-built sufficient
option. The ladder is a **reflex, not a research project**, but it runs only
after the agent understands the task and traces the real flow
([`skills/ponytail/SKILL.md:20-48`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L20),
[`README.md:88-104`](../../../.tmp/ponytail/README.md#L88)).

The pack's reduction vocabulary is guarded rather than absolute: **shortest
working diff**, **deletion over addition**, **boring over clever**, and **fewest
files** apply only after comprehension; trust-boundary validation, data-loss
handling, security, accessibility, requested behavior, and physical-world
calibration are floors, not bloat
([`skills/ponytail/SKILL.md:50-64`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L50),
[`skills/ponytail/SKILL.md:90-112`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L90)).

### 2. Availability before invention

The ladder distinguishes **already in this codebase**, **stdlib**, **native
platform feature**, and **already-installed dependency**. These are not generic
synonyms for simplicity; they encode an ordered search for an existing owner.
**Platform-native** spans browser primitives, language/runtime libraries, UI
frameworks, and database features. A **library earns its place** only when the
native option is genuinely insufficient for compatibility, edge cases, or
scale-relevant ergonomics
([`skills/ponytail/SKILL.md:34-42`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L34),
[`docs/platform-native.md:197-211`](../../../.tmp/ponytail/docs/platform-native.md#L197)).

### 3. Deliberate shortcut accounting

A lowercase **`ponytail:` marker** records a simplification that cuts a real
corner. It must name a **known ceiling** and an **upgrade path** or **trigger to
revisit**. `/ponytail-debt` harvests markers into a **debt ledger** and assigns
**no-trigger** to entries whose missing revisit condition creates **rot risk**
([`skills/ponytail/SKILL.md:64`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L64),
[`skills/ponytail-debt/SKILL.md:11-38`](../../../.tmp/ponytail/skills/ponytail-debt/SKILL.md#L11)).

The compact delivery form **Skipped / Add when** applies the same idea at the
response boundary: state what was deliberately omitted and the condition that
would justify it later
([`skills/ponytail/SKILL.md:66-75`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L66),
[`examples/debounce.md:209`](../../../.tmp/ponytail/examples/debounce.md#L209)).

### 4. Lifecycle and intensity

**Lite**, **full**, and **ultra** are named intensities: name a lazier
alternative; enforce the ladder; or push deletion/YAGNI while still honoring
explicit requirements. The main mode is **persistent** across responses until
changed or the session ends. Help, gain, audit, and debt are described as
**one-shot** reports or displays that should not mutate mode
([`skills/ponytail/SKILL.md:26-30`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L26),
[`skills/ponytail/SKILL.md:77-88`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L77),
[`skills/ponytail-help/SKILL.md:9-22`](../../../.tmp/ponytail/skills/ponytail-help/SKILL.md#L9)).

Runtime surfaces refine that language into **default mode**, **session/live
mode**, **report-only/status**, **ruleset injection**, **subagent propagation**,
and **deactivation**. They also expose host-specific inconsistencies rather
than one uniform persistence model
([`hooks/ponytail-runtime.js:6-34`](../../../.tmp/ponytail/hooks/ponytail-runtime.js#L6),
[`hooks/ponytail-mode-tracker.js:20-81`](../../../.tmp/ponytail/hooks/ponytail-mode-tracker.js#L20),
[`hooks/ponytail-subagent.js:4-25`](../../../.tmp/ponytail/hooks/ponytail-subagent.js#L4)).

### 5. Complexity findings and terminal reports

`ponytail-review` is a diff-scoped complexity hunt; `ponytail-audit` is its
whole-tree, biggest-cut-first form. Both use a terse finding taxonomy:
**delete**, **stdlib**, **native**, **yagni**, and **shrink**. Their quantitative
terminal is **net: -N lines possible** (and for audit, dependencies); the empty
terminal is **Lean already. Ship.**
([`skills/ponytail-review/SKILL.md:13-48`](../../../.tmp/ponytail/skills/ponytail-review/SKILL.md#L13),
[`skills/ponytail-audit/SKILL.md:12-40`](../../../.tmp/ponytail/skills/ponytail-audit/SKILL.md#L12)).

### 6. Evidence against deceptive smallness

**One runnable check** is the minimum evidence floor for non-trivial logic: the
smallest assertion, demo, self-check, or test that fails when the logic breaks.
Tests are a positive signal, not bloat
([`skills/ponytail/SKILL.md:107-112`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L107),
[`benchmarks/agentic/README.md:63-72`](../../../.tmp/ponytail/benchmarks/agentic/README.md#L63)).

Benchmark surfaces distinguish **measurement** from **gate**, and **correct**
from **safe** and **complete**. A **behavior gate** asks whether the ruleset
produces the behavior rather than merely containing the words. **Instrument
first / refuse to spend** requires a known-good reference to pass and a
lazy-plausible bad reference to be caught before live model calls. An
**auditable judge** uses a fixed model, zero temperature, a published rubric,
and a self-test ranking known references. **Under-delivery** names low-LOC work
that is small because it did less
([`benchmarks/behavior.yaml:1-13`](../../../.tmp/ponytail/benchmarks/behavior.yaml#L1),
[`benchmarks/agentic/README.md:63-104`](../../../.tmp/ponytail/benchmarks/agentic/README.md#L63),
[`benchmarks/agentic/complete.py:2-14`](../../../.tmp/ponytail/benchmarks/agentic/complete.py#L2)).

The gain skill adds an **honesty boundary**: benchmark medians are not current
repo savings, because an unbuilt counterfactual provides no per-repo baseline.
The only pack-defined per-repo substitutes are the counted debt ledger and the
audit's cuttable findings
([`skills/ponytail-gain/SKILL.md:16-24`](../../../.tmp/ponytail/skills/ponytail-gain/SKILL.md#L16),
[`skills/ponytail-gain/SKILL.md:39-45`](../../../.tmp/ponytail/skills/ponytail-gain/SKILL.md#L39)).

### 7. Portable loading and runtime support

Ponytail calls itself an **agent-portable skill distribution**: canonical
skills hold core behavior and host files are **thin adapters**. Documentation
distinguishes **plugin-tier** integration, with hooks, activation, commands,
and mode tracking, from **instruction-tier** always-on rules
([`docs/agent-portability.md:3-38`](../../../.tmp/ponytail/docs/agent-portability.md#L3)).

Runtime support uses **best-effort / never-block** for lifecycle helpers,
**shell-safe path gate** for statusline setup, **owned cleanup** for uninstall,
and copy/version gates to prevent adapter drift. These terms recruit a narrow
support policy: optional integration failure must not freeze the host or erase
unrelated configuration
([`hooks/ponytail-mode-tracker.js:122-130`](../../../.tmp/ponytail/hooks/ponytail-mode-tracker.js#L122),
[`hooks/ponytail-activate.js:44-89`](../../../.tmp/ponytail/hooks/ponytail-activate.js#L44),
[`scripts/uninstall.js:2-56`](../../../.tmp/ponytail/scripts/uninstall.js#L2)).

## Retained Vocabulary

| Term | Variants | Class | Meaning In This Pack | Behavior Or Distinction Recruited | Spread | Claim Label | Best Provenance | Conditions / Limits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lazy senior developer | Ponytail; lazy, not careless | candidate-leading-word; pack-specific | Build the least new machinery that safely satisfies the task. | Questions existence and searches for existing owners before implementation. | Skills, rules, README, examples | corroborated | [`skills/ponytail/SKILL.md:20-24`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L20) | Governs what is built, not terse prose; does not excuse shallow reading. |
| ladder | rung; first rung that holds; higher rung | workflow-control; pack-specific | Ordered sufficiency filter from non-existence through minimum new code. | Stops solution search at the earliest sufficient option after comprehension. | Skill, rule copies, commands, README, runtime fallback, benchmarks | corroborated | [`skills/ponytail/SKILL.md:32-48`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L32) | Command/help summaries omit some rungs. |
| already in this codebase | reuse what already lives here | workflow-control; domain-design | Searches local helpers, types, and patterns before external or new code. | Prevents sibling reimplementation and semantic divergence. | Skill, rules, benchmark quality tasks | corroborated | [`skills/ponytail/SKILL.md:36-38`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L36) | Behavioral value of the rung was not reproduced on every model. |
| stdlib / native / installed dependency | platform-native; existing capability | workflow-control; domain-design | Ordered existing solution owners before new code or dependency. | Replaces wrappers and custom machinery with maintained capabilities. | Skills, reviews, docs, examples | corroborated | [`skills/ponytail/SKILL.md:38-42`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L38) | Platform compatibility and ergonomics must still be checked. |
| library earns its place | native insufficient | failure-exclusion; domain-design | Dependency is justified only by a concrete limit of the native solution. | Defers installation until compatibility, edge cases, or scale requires it. | Platform doc, examples | direct | [`docs/platform-native.md:209-211`](../../../.tmp/ponytail/docs/platform-native.md#L209) | Not a universal dependency ban. |
| root cause, not symptom | fix shared function once; grep every caller | workflow-control; evidence-completion | Trace callers and repair the shared route rather than the ticket's visible path. | Makes the smaller fix the shared semantic fix, not a surface patch. | Skill, rules, benchmark tasks/results | corroborated | [`skills/ponytail/SKILL.md:50-54`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L50) | “Root cause” alone is generic; the caller-trace formulation is distinctive. |
| shortest working diff | deletion over addition; boring over clever; fewest files | candidate-leading-word; workflow-control | Optimize change size after understanding and correctness. | Rejects speculative abstraction, scaffolding, and avoidable files. | Skill, rules, reviews, README | corroborated | [`skills/ponytail/SKILL.md:58-64`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L58) | The smallest change in the wrong place is explicitly rejected. |
| `ponytail:` marker | shortcut comment; ceiling comment | artifact-state; pack-specific | Inline record of an intentional corner-cutting simplification. | Makes the deferral discoverable by `/ponytail-debt`. | Skill, rules, debt, scripts, docs, benchmarks | corroborated | [`skills/ponytail/SKILL.md:64`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L64) | Lexically collides with namespaced skill names. |
| known ceiling | limit; upgrade path; trigger to revisit | artifact-state; evidence-completion | Boundary of the shortcut plus condition/action for replacing it. | Prevents an intentional temporary limit from silently becoming permanent. | Skill, debt, rules, benchmarks | corroborated | [`skills/ponytail-debt/SKILL.md:25-38`](../../../.tmp/ponytail/skills/ponytail-debt/SKILL.md#L25) | Upgrade action and revisit condition are not modeled separately. |
| debt ledger | counted ledger; no-trigger; rot risk | artifact-state; failure-exclusion | Read-only harvest of `ponytail:` markers, grouped and counted. | Exposes unowned or triggerless deferrals without inventing savings. | Debt, gain, help, README | corroborated | [`skills/ponytail-debt/SKILL.md:11-38`](../../../.tmp/ponytail/skills/ponytail-debt/SKILL.md#L11) | Durable file output requires a separate request. |
| Skipped / Add when | ship and question | relationship-handoff; artifact-state | Compact statement of omitted scope and the escalation condition. | Delivers a safe default without silently broadening scope or stalling. | Main skill, examples, historical benchmark language | corroborated | [`skills/ponytail/SKILL.md:62-75`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L62) | Rule copies sometimes say only to question the request, weakening the ship-first contract. |
| lite / full / ultra | intensity; level | invocation-routing; workflow-control | Three strengths of reduction behavior. | Chooses alternative-naming, ladder enforcement, or maximal YAGNI/deletion. | Skill, help, commands, adapters, tests | corroborated | [`skills/ponytail/SKILL.md:77-88`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L77) | Ultra summaries disagree on whether challenge precedes or accompanies delivery. |
| persistent mode | default mode; session/live mode; active/off | invocation-routing; artifact-state | Coding rules remain injected until changed, deactivated, or lifecycle ends. | Controls cross-response activation and restoration. | Skills, hooks, Pi, OpenCode, Hermes, tests | corroborated | [`hooks/ponytail-runtime.js:18-34`](../../../.tmp/ponytail/hooks/ponytail-runtime.js#L18) | “Persistent” has multiple host-specific durations and absent-state meanings. |
| one-shot | report-only; display-only | invocation-routing; failure-exclusion | Specialized command returns information without changing the coding mode. | Separates reports from persistent behavior. | Audit, debt, gain, help, commands | corroborated | [`skills/ponytail-gain/SKILL.md:11-14`](../../../.tmp/ponytail/skills/ponytail-gain/SKILL.md#L11) | Some one-shot skills still include reversion language, creating lifecycle ambiguity. |
| delete / stdlib / native / yagni / shrink | review tags | artifact-state; workflow-control | Mutually useful labels for what to remove or replace. | Makes complexity findings terse, ranked, and action-bearing. | Review, audit, commands, help | corroborated | [`skills/ponytail-review/SKILL.md:21-27`](../../../.tmp/ponytail/skills/ponytail-review/SKILL.md#L21) | `stdlib` and `native` also name ladder rungs. |
| Lean already. Ship. | net: `-N` lines; `-M` deps | evidence-completion; pack-specific | Empty-result terminal and estimated reduction summary. | Ends review/audit when no cut is found. | Review and audit | corroborated | [`skills/ponytail-audit/SKILL.md:31-34`](../../../.tmp/ponytail/skills/ponytail-audit/SKILL.md#L31) | No estimation method is specified for possible line/dependency reductions. |
| one runnable check | smallest thing that fails; test reflex | evidence-completion | Minimal executable check required for non-trivial logic. | Prevents “small” from meaning unverified while avoiding framework scaffolding. | Skill, rules, behavior benchmark, agentic scorer | corroborated | [`skills/ponytail/SKILL.md:107-112`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L107) | Trivial one-liners are exempt; it is a floor, not broad semantic proof. |
| behavior gate | behavior present/absent | evidence-completion | Test that the ruleset produces a behavior rather than repeats vocabulary. | Requires positive and negative examples around an operational probe. | Benchmark config, grader, tests | corroborated | [`benchmarks/behavior.yaml:1-13`](../../../.tmp/ponytail/benchmarks/behavior.yaml#L1) | Covers three selected behaviors, not the whole pack. |
| instrument first | known-good / lazy-plausible bad; refuse to spend | evidence-completion; failure-exclusion | Validate a scorer before spending on live model runs. | Good must pass and bad must be caught; failed self-test aborts the matrix. | Agentic and robustness benchmark code/docs | corroborated | [`benchmarks/agentic/tasks.py:1-21`](../../../.tmp/ponytail/benchmarks/agentic/tasks.py#L1) | Judge self-tests may themselves require a model call. |
| correct / safe / complete | correctness gate; safety floor; completeness judge; under-delivery | evidence-completion; failure-exclusion | Separate functional success, adversarial robustness, and fulfillment. | Prevents low LOC from winning by dropping a guard or requested behavior. | Agentic benchmark code/docs/results | corroborated | [`benchmarks/agentic/README.md:63-104`](../../../.tmp/ponytail/benchmarks/agentic/README.md#L63) | These labels collide across task tiers and are not interchangeable metrics. |
| honesty boundary | fair baseline; not this repo; counted ledger | evidence-completion; failure-exclusion | Refuses counterfactual per-repo savings claims from benchmark medians. | Qualifies measurement by baseline, generation, scope, and reproducibility. | Gain, README, benchmark docs/results | corroborated | [`skills/ponytail-gain/SKILL.md:39-45`](../../../.tmp/ponytail/skills/ponytail-gain/SKILL.md#L39) | Benchmark results establish pack evidence only, not external validity. |
| agent-portable skill distribution | core behavior; thin adapter; plugin-tier; instruction-tier | relationship-handoff; pack-specific | Canonical skills own behavior; host files load as much lifecycle support as the host allows. | Separates semantic owner from adapter and distribution surfaces. | Portability doc, scripts, manifests, tests | corroborated | [`docs/agent-portability.md:3-38`](../../../.tmp/ponytail/docs/agent-portability.md#L3) | Fallback instruction copies weaken the “one shared source” claim. |
| best-effort / never-block | shell-safe path gate; owned cleanup | failure-exclusion; workflow-control | Optional lifecycle support must fail quietly and preserve unrelated user state. | Avoids frozen sessions, unsafe command embedding, and broad uninstall mutation. | Hooks, scripts, tests | corroborated | [`hooks/ponytail-mode-tracker.js:122-130`](../../../.tmp/ponytail/hooks/ponytail-mode-tracker.js#L122) | Fail-open subagent injection favors persona continuity over strict scoping. |

## Techniques Encoded By The Language

| Vocabulary | Technique | Essential Mechanics | Use Context In The Pack | Failure / Misuse Risk | Claim Label | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| ladder / first rung that holds | Ordered elimination before implementation | Understand and trace; test necessity, local reuse, stdlib, platform, installed dependency, one-line form, then minimum new code; stop at earliest sufficient rung. | Any coding task under the persistent skill. | Treating the ladder as a substitute for reading or as code golf. | corroborated | [`skills/ponytail/SKILL.md:32-48`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L32) |
| root cause, not symptom | Shared-route repair | Enumerate callers and place one guard at their shared semantic owner. | Bug fixes. | Assuming shared placement without tracing all affected paths. | corroborated | [`skills/ponytail/SKILL.md:50-54`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L50) |
| ceiling + upgrade path | Explicitly bounded shortcut | Mark an intentional corner with its limit and revisit trigger; harvest it later. | Deliberate simplifications with known future limits. | Marker without a trigger becomes rot; not every simplification needs a marker. | corroborated | [`skills/ponytail-debt/SKILL.md:11-38`](../../../.tmp/ponytail/skills/ponytail-debt/SKILL.md#L11) |
| Skipped / Add when | Deferred-scope handoff | Deliver the safe sufficient version and name the omitted feature plus concrete escalation condition. | Complex request with a smaller sufficient default. | Using it to omit explicitly required behavior or a safety floor. | corroborated | [`skills/ponytail/SKILL.md:62-75`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L62) |
| one runnable check | Minimal executable evidence | Leave one assertion, demo, self-check, or test for non-trivial logic; exclude it from bloat scoring. | Branches, loops, parsers, and money/security paths. | Treating the minimum check as exhaustive proof. | corroborated | [`skills/ponytail/SKILL.md:107-112`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L107) |
| review tags + net reduction | Cut-oriented inspection | Classify each replaceable construct, name its replacement, rank cuts, and terminate explicitly. | Diff review or whole-repo audit for complexity only. | Estimated LOC can imply false precision; correctness/security/performance remain out of scope. | corroborated | [`skills/ponytail-review/SKILL.md:13-56`](../../../.tmp/ponytail/skills/ponytail-review/SKILL.md#L13) |
| behavior gate | Test behavioral recruitment | Probe behavior-present and behavior-absent examples rather than checking text inclusion. | Skill behavior evaluation. | Selected probes do not establish complete behavior. | corroborated | [`benchmarks/behavior.js:1-44`](../../../.tmp/ponytail/benchmarks/behavior.js#L1) |
| instrument first / auditable judge | Validate evidence machinery | Known-good passes, known-bad fails, fixed rubric/model where nondeterministic judgment is unavoidable, then live run. | Benchmark correctness, safety, completeness, and over-engineering. | A self-tested judge is still model-mediated; unknown routes sometimes pass as skipped. | corroborated | [`benchmarks/agentic/README.md:63-104`](../../../.tmp/ponytail/benchmarks/agentic/README.md#L63) |
| honesty boundary | Qualify counterfactual measurement | Pin the baseline and benchmark generation; distinguish current-repo counts from benchmark medians; preserve superseded/contaminated evidence as such. | Gain display and benchmark reporting. | Mixing single-shot and agentic baselines or treating median ranges as repo savings. | corroborated | [`skills/ponytail-gain/SKILL.md:39-45`](../../../.tmp/ponytail/skills/ponytail-gain/SKILL.md#L39) |
| thin adapter + drift gates | Preserve one behavioral owner across hosts | Generate or compare copies, verify invariant phrases and versions, and adapt only lifecycle transport. | Multi-host distribution. | Fallback duplication and host-specific command semantics still drift. | corroborated | [`docs/agent-portability.md:34-38`](../../../.tmp/ponytail/docs/agent-portability.md#L34) |
| best-effort / never-block | Conservative lifecycle support | Silent optional failures, bounded stdin fallback, safe path check, and owned-only cleanup. | Activation, mode tracking, statusline, subagents, uninstall. | Silent failure can hide lost support; fail-open injection can broaden scope. | corroborated | [`hooks/ponytail-mode-tracker.js:114-130`](../../../.tmp/ponytail/hooks/ponytail-mode-tracker.js#L114) |

## Aliases, Collisions, And Inconsistencies

| Terms | Relationship | Evidence | Consequence For Interpretation |
| --- | --- | --- | --- |
| lazy / simplest / shortest / minimal / do less | Invocation aliases around one reduction concept. | [`skills/ponytail/SKILL.md:3-15`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L3) | Do not promote each phrase as an independent term. |
| `Ponytail`; `ponytail:` | Brand/mode versus source-code marker; the same prefix also namespaces Hermes skills. | [`skills/ponytail-debt/SKILL.md:11-23`](../../../.tmp/ponytail/skills/ponytail-debt/SKILL.md#L11), [`after-install.md:18-24`](../../../.tmp/ponytail/after-install.md#L18) | The marker needs its syntactic context to avoid collision. |
| upgrade path / trigger to revisit | Used almost interchangeably, but one may denote action and the other condition. | [`skills/ponytail-debt/SKILL.md:29-36`](../../../.tmp/ponytail/skills/ponytail-debt/SKILL.md#L29) | The ledger's single `upgrade` field loses this distinction. |
| canonical seven-rung ladder; help/command ladder | Short summaries omit local reuse and already-installed dependency. | [`skills/ponytail/SKILL.md:34-42`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L34), [`skills/ponytail-help/SKILL.md:14-20`](../../../.tmp/ponytail/skills/ponytail-help/SKILL.md#L14) | Short surfaces can recruit a materially narrower search. |
| question complex request; ship and question | Rule copies suggest asking; canonical skill says deliver a safe default and never stall. | [`AGENTS.md:19-28`](../../../.tmp/ponytail/AGENTS.md#L19), [`skills/ponytail/SKILL.md:62`](../../../.tmp/ponytail/skills/ponytail/SKILL.md#L62) | Host tier can change whether the behavior is decisive or conversational. |
| persistent | Always every response, session state, transcript-restored state, cross-chat file, or cross-restart default. | [`hooks/ponytail-runtime.js:18-34`](../../../.tmp/ponytail/hooks/ponytail-runtime.js#L18), [`pi-extension/index.js:24-37`](../../../.tmp/ponytail/pi-extension/index.js#L24) | Always name the host and persistence boundary. |
| `review` | Specialized skill, JS independent mode, benchmark evaluation activity; not a JS-valid default but allowed by Hermes config. | [`hooks/ponytail-instructions.js:8-9`](../../../.tmp/ponytail/hooks/ponytail-instructions.js#L8), [`hooks/ponytail-config.js:76-99`](../../../.tmp/ponytail/hooks/ponytail-config.js#L76), [`__init__.py:52-63`](../../../.tmp/ponytail/__init__.py#L52) | There is no pack-wide settled `review` state. |
| bare `/ponytail` | Reports current mode, activates fallback, reports in Hermes, or writes default in OpenCode. | [`hooks/ponytail-mode-tracker.js:50-63`](../../../.tmp/ponytail/hooks/ponytail-mode-tracker.js#L50), [`pi-extension/index.js:39-45`](../../../.tmp/ponytail/pi-extension/index.js#L39) | Command meaning is host-specific. |
| absent state | Means off in hook runtime but configured default in other adapters. | [`hooks/ponytail-runtime.js:27-34`](../../../.tmp/ponytail/hooks/ponytail-runtime.js#L27), [`pi-extension/index.js:24-37`](../../../.tmp/ponytail/pi-extension/index.js#L24) | State diagrams cannot assume one default branch. |
| correct / safe / complete / pass / LOC / baseline | Each changes meaning across benchmark generations or task tiers. | [`benchmarks/agentic/README.md:13-24`](../../../.tmp/ponytail/benchmarks/agentic/README.md#L13), [`benchmarks/agentic/README.md:63-104`](../../../.tmp/ponytail/benchmarks/agentic/README.md#L63) | Metrics require their scorer, tier, and baseline; labels alone are insufficient evidence. |
| one-shot; stop/revert wording | One-shot tools promise no mode mutation but still carry deactivation language. | [`skills/ponytail-gain/SKILL.md:39-50`](../../../.tmp/ponytail/skills/ponytail-gain/SKILL.md#L39) | Reversion text should not be read as evidence that the one-shot tool activated a mode. |
| English; Spanish; Korean docs | Translations add no unique term but lag commands and hosts. | [`README.md:285-296`](../../../.tmp/ponytail/README.md#L285), [`README.es.md:233-243`](../../../.tmp/ponytail/README.es.md#L233) | English current-state docs are stronger for inventory; translations corroborate core meaning only. |
| examples; current safety language | Some generated examples omit error handling or use validation patterns later benchmarks reject. | [`examples/csv-sum.md:60-69`](../../../.tmp/ponytail/examples/csv-sum.md#L60), [`benchmarks/agentic/README.md:48-61`](../../../.tmp/ponytail/benchmarks/agentic/README.md#L48) | Examples are demonstrations, not the current normative safety contract. |

## Inferred Applications

These comparisons describe semantic proximity or collision only. They do not
recommend adoption.

| Ponytail Vocabulary | Local Comparison | Label | Assumption Requiring Validation |
| --- | --- | --- | --- |
| ladder / first rung that holds | The local `Explore -> Choose -> Prove -> Expand -> Simplify -> Lock` spine is also ordered, but Ponytail's ladder selects the least-built sufficient solution while the spine governs the lifecycle of proving and completing work. Treating them as aliases would collapse selection into execution. | synthesis | A downstream synthesis would need to decide whether both sequences can coexist without routing ambiguity. [`engineering-contract.md:42-55`](../../agents/engineering-contract.md#L42) |
| shortest working diff | Local **bounded slice** and **deep simplicity** also constrain complexity, but local language preserves commitments and semantic proof rather than optimizing raw diff size. | synthesis | Any local use would need evidence that “shortest” does not override the commitment boundary or proof seam. [`engineering-contract.md:15-22`](../../agents/engineering-contract.md#L15), [`engineering-contract.md:36-40`](../../agents/engineering-contract.md#L36) |
| one runnable check | Local **proof lane** and **semantic proof** are broader caller-facing evidence concepts; Ponytail's check is a minimum floor for non-trivial logic. | synthesis | A downstream owner would need to establish when the minimum check is adequate and when the proof seam demands more. [`engineering-contract.md:18-24`](../../agents/engineering-contract.md#L18) |
| ceiling + upgrade trigger + debt ledger | Local **residual risk** records uncertainty and skipped proof; the Ponytail marker instead records an intentional implementation limit and revisit condition. | synthesis | A local mapping would need to preserve deliberate design limits separately from uncertainty. [`engineering-contract.md:27-32`](../../agents/engineering-contract.md#L27) |
| behavior gate / instrument first | Local **negative control**, **evaluation harness**, and evidence discipline are close techniques: prove the evaluator discriminates before trusting it. | synthesis | The evaluator's negative case and admission threshold would need to be defined per behavior rather than copied from Ponytail's probes. [`engineering-contract.md:57-71`](../../agents/engineering-contract.md#L57), [`04-agentic-bridge-vocabulary.md:76-87`](04-agentic-bridge-vocabulary.md#L76) |
| agent-portable core + thin adapters | Local context trace and artifact ownership likewise assign one semantic owner and point downstream surfaces toward it. | synthesis | Ponytail's fallback copies show that “thin” does not guarantee one source of truth; local validation would still need parity proof. [`CONTEXT.md:16-33`](../../../CONTEXT.md#L16), [`CONTEXT.md:35-53`](../../../CONTEXT.md#L35) |
| persistent mode / one-shot | Local owners describe skill invocation, procedures, and completion, but the compared vocabulary owners do not define a general mode-duration taxonomy. | inference | A later synthesis would need actual local runtime cases before deciding whether Ponytail's lifecycle words fill a gap or introduce private jargon. [`CONTEXT.md:24-33`](../../../CONTEXT.md#L24) |
| honesty boundary / qualified baseline | Local **fixed point**, **review snapshot**, **evidence**, and **residual risk** similarly require the comparison target and remaining uncertainty to be explicit. | synthesis | Benchmark baselines and review baselines have different semantics; only the discipline of qualification appears transferable. [`engineering-contract.md:23-32`](../../agents/engineering-contract.md#L23) |
| lazy senior developer | Local steering guidance prefers professional vocabulary that recruits established practice and de-emphasizes private dialect. Ponytail's leading phrase is deliberately persona-like and pack-specific. | synthesis | Any downstream consideration would need behavioral evidence that the persona adds control beyond YAGNI, reuse, native capability, and evidence terms. [`03-high-signal-steering-words.md:1-27`](03-high-signal-steering-words.md#L1), [`03-high-signal-steering-words.md:105-127`](03-high-signal-steering-words.md#L105) |

## Prune Log

| Removed Or Merged Material | Reason | Stronger Retained Owner | Reconsider Only If |
| --- | --- | --- | --- |
| simplest, minimal, shortest path, do less, be lazy | Invocation aliases without separate semantics. | lazy senior developer; ladder | A surface gives one alias a distinct branch or completion rule. |
| generic simplicity, productivity, code review, over-engineering | Too broad in isolation. | ladder; review tags; shortest working diff | The pack explicitly defines an additional operational distinction. |
| ordinary validation, security, accessibility, error handling | Established boundary language, not distinctive Ponytail vocabulary by itself. | safety floor under minimum-solution cluster | The question changes to safety guidance rather than pack vocabulary. |
| raw benchmark percentages, model names, and speed/cost claims | Results, not operational vocabulary; externally narrow and revision-sensitive. | honesty boundary; qualified baseline | A later evidence review asks whether the performance claims generalize. |
| output cap, anti-deliberation, test reflex, robust variant rule | Historical benchmark labels whose current behavior is better owned by canonical output, runnable-check, or correctness language. | Skipped/Add when; one runnable check; correct/safe/complete | A runtime surface promotes one as a current named contract. |
| platform API catalog entries | Concrete examples, not a vocabulary item per API. | platform-native; library earns its place | A compatibility audit asks which replacements remain current. |
| host names, manifest keys, package-manager syntax, license/version metadata | Distribution syntax without semantic decision content. | agent-portable distribution; thin adapter | A host-integration question makes one interface operationally relevant. |
| benchmark-only task names and adversarial cases | Fixtures illustrate the gates but do not name pack-wide concepts. | correct/safe/complete; instrument first | A benchmark-method packet is requested. |
| Caveman modes and vocabulary | Control-arm language from another pack. | Ponytail/Caveman distinction | The source question expands to cross-pack vocabulary. |
| translated variants | No unique operational meaning; merged into English semantic owner. | corresponding English terms | A localization-quality audit is requested. |

## Evidence Gaps

- No fetch was performed, so this packet cannot claim that the checkout equals
  the live remote state on 2026-07-22.
- The pack has no settled name for the understand-and-trace phase before the
  ladder, no formal schema name for the `ponytail:` marker, and no distinct
  canonical label for the runnable-check floor.
- Host adapters disagree on `review`, bare `/ponytail`, invalid commands,
  default persistence, and the meaning of absent state. These are source
  inconsistencies, not terminology resolved by this packet.
- The canonical ladder has seven rungs, while help and command summaries omit
  two. Host-shortened rules also weaken the ship-and-question behavior.
- Fallback instruction text is duplicated across adapters, so the stated thin
  adapter / shared-core model is incomplete in practice.
- Review/audit reduction estimates have no specified estimation method.
- Benchmark terms such as `correct`, `safe`, `complete`, `pass`, `LOC`, and
  `baseline` are meaningful only with their generation and scorer. Unknown
  probes sometimes pass as skipped, and several checks are structural proxies.
- The strongest benchmark evidence is limited by task set, model, sample size,
  nondeterminism, and historical contamination. It cannot establish production
  readiness, general security, or universal savings.
- Platform-native examples are compatibility-sensitive and were not checked
  against current external platform documentation because the question asks
  what the checked-out pack says, not whether each API recommendation is
  currently correct.
- Six PNG assets were not semantically inspectable. Their adjacent alt text and
  SVG equivalents added no unique operational concept.

## Source Trace

| Source | Authority | Version Or Date | Supports |
| --- | --- | --- | --- |
| `skills/ponytail*/SKILL.md` | Canonical skill behavior and routing | Commit `16f2980`; verified 2026-07-22 | Ladder, modes, reports, marker, evidence floor, boundaries. |
| `AGENTS.md`, commands, host rules, `.openclaw` mirrors | Shortened and generated loading surfaces | Same commit | Spread, aliasing, omissions, and mirror drift. |
| `hooks/`, `.opencode/plugins/`, `pi-extension/`, `ponytail-mcp/`, `__init__.py` | Executable runtime semantics | Same commit | Activation, persistence, injection, status, subagents, host collisions. |
| `scripts/` and `tests/` | Enforced distribution, lifecycle, and cleanup contracts | Same commit | Copy/version gates, owned cleanup, branch behavior, negative cases. |
| `README*`, `docs/`, `examples/`, `after-install.md` | Human-facing explanation and demonstrated use | Same commit | Public identity, portability, platform-native meaning, reporting patterns, translation/example limitations. |
| `benchmarks/` | Pack's own evaluation methods and historical results | Same commit; result dates 2026-06-12 through 2026-06-22 | Behavior gates, evidence distinctions, benchmark honesty, contradictions and limits. |
| Local vocabulary owners | Primary evidence only for local comparison | Working-tree state inspected 2026-07-22 | Synthesis/inference comparisons; no Ponytail meaning attributed from them. |

## Final Decision

`source-packet-complete`
