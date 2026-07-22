# Facet 1: Bounded Slice Source Triage

Historical source-to-skill Prompt 05 artifact for `implement` Facet 1.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Facet: `1. Bounded Slice`

Facet research question: How do strong teams keep one implementation run small,
valuable, independently provable, and reviewable?

Source search packet:
[`FACET-1-BOUNDED-SLICE-sources.md`](FACET-1-BOUNDED-SLICE-sources.md)

Source extraction packet:
[`FACET-1-BOUNDED-SLICE-extraction.md`](FACET-1-BOUNDED-SLICE-extraction.md)

Do not search for new sources. Do not extract new material except tiny gap
notes. Do not synthesize the behavior flow yet. Do not write runtime
`SKILL.md` wording yet.

## 1. Triage Scope

This packet triages extracted source material for `implement` Facet 1:
`Bounded Slice`.

Source lanes represented:

- professional SWE and review practice;
- product/requirements slicing;
- delivery small-batch rationale;
- empirical code-review research;
- official coding-agent docs and agentic coding papers.

Out of scope:

- upstream issue creation/readiness work owned by `to-issues` and `triage`;
- full TDD, proof modes, and test mechanics owned by `$tdd` and later Semantic
  Proof research;
- baseline/fixed-point mechanics owned by Facet 2;
- commitment-authority rules owned by Facet 4 and the engineering contract;
- seam-depth and load-bearing internal guidance owned by Facet 6;
- simplification/refactor detail owned by Facet 7;
- fixed-point review, implementation-note detail, residual risk, and commit
  readiness owned by `$review` and Facet 8.

Over-keeping would mean importing story-mapping, small-batch economics,
code-review doctrine, agent-framework vocabulary, or full proof procedure into
runtime `implement` wording. This facet should keep only material that helps an
agent execute one selected issue as one bounded, provable slice.

## 2. Keep / Reject Standard

- Keep material only when it can change `$implement` behavior during one issue:
  slice lock, scope containment, proof choice, stop/split decisions, or
  follow-up handling.
- Reject or demote slogans that need another sentence to become actionable,
  such as "keep it small", "be reviewable", or "run validation".
- Treat runtime wording as expensive. If a concept needs explanation, nuance,
  source history, or a taxonomy, move it to support or research unless the
  runtime gate is impossible without it.
- Keep support material when it helps later prompts preserve nuance without
  bloating `SKILL.md`.
- Mark `owned-elsewhere` when another facet, skill, repo doc, ADR, or the
  engineering contract already owns the behavior.
- Reject over-cautious stop rules that would make the agent ask about ordinary
  implementation technique inside the bounded slice.

## 3. Leading Word Triage

| Term | Source | Category | Why | Behavior It Can Steer | Risk If Kept | Action |
| --- | --- | --- | --- | --- | --- | --- |
| `bounded slice` | Facet map / extraction synthesis | `keep-runtime` | Central facet concept and already local repo language. | Keep one selected issue inside one behavior/support proof. | Vague if not tied to proof and drift rules. | keep for behavior flow |
| `tracer bullet` | *The Pragmatic Programmer* | `keep-runtime` | Strongest compact word for one real path that produces feedback. | Prefer one production-shaped path over feature breadth. | Prototype drift or incomplete fake behavior if "real/proved" is lost. | keep for behavior flow |
| `support slice` | Humanizing Work / engineering contract | `keep-runtime` | Prevents docs/config/refactor/test-harness work from pretending to be user behavior. | State the unblocker/de-risking purpose and proof for non-behavior work. | Can excuse technical drift if proof is not named. | keep for behavior flow |
| `one self-contained change` | Google Small CLs | `keep-runtime` | Best compact review/proof boundary: code, rationale, and related proof together. | Keep the diff to one issue/concept with proof attached. | Duplicates `bounded slice` if expanded as separate doctrine. | keep for behavior flow |
| `one concept` | di Biase / Ram | `keep-runtime` | Crisp split signal when adjacent work appears. | Stop, split, or record follow-up when an independent second concept appears. | Can over-split legitimately coupled edits. | keep for behavior flow |
| `file spread` | Google Small CLs / Bosu | `keep-runtime` | Practical mid-run warning that review size is not just LOC. | Re-bound or justify touched areas when the diff spreads. | Can become file-count policy. | keep for behavior flow |
| `vertical slice` | Humanizing Work / Patton | `bridge-needed` | Useful product-slicing concept, but slogan risk is high. | Could steer toward one caller/operator path. | Imports Agile/product baggage if kept raw. | translate before keeping |
| `thin slice` | Patton / Humanizing Work | `keep-research` | Overlaps `vertical slice`; weaker than `tracer bullet` for runtime. | Could reinforce one small caller path. | Product/story-mapping baggage and duplication. | keep as research only |
| `walking skeleton` | GOOS / Patton | `bridge-needed` | Valuable only when system shape or feedback path is uncertain. | Establish minimal executable path before breadth. | Too heavy for routine issues; invites architecture theater. | move to support |
| `small batch` | DORA / Continuous Delivery | `keep-research` | Good rationale for feedback/recovery, weak direct runtime hook. | Guard against broad AI-generated diffs. | Overclaims merge speed or imports delivery doctrine. | keep as research only |
| `reviewable change` | Ram / Google / SWE@Google | `bridge-needed` | Useful, but full review is owned by `$review`/Facet 8. | Keep purpose, changed areas, and proof understandable. | Duplicates review/lock and bloats runtime. | translate before keeping |
| `success criteria` | OpenAI / GitHub / Anthropic | `keep-runtime` | Checkability belongs at the slice boundary. | Name the proof target before editing. | Duplicates Context Intake if expanded into readiness authoring. | keep for behavior flow |
| `localize-repair-validate` | Agentless / SWE-agent | `bridge-needed` | Good agent action pattern, bad runtime phrase. | Read enough, edit narrowly, prove. | Bug-fix bias and framework jargon. | translate before keeping |
| `tool feedback` | SWE-agent / OpenAI | `bridge-needed` | Useful only when tied to scope classification. | Let failed checks steer only in-scope fixes. | Default agent behavior if kept generically. | translate before keeping |

## 4. Behavior Rule Triage

| Rule | Source | Category | Why | Operational Gate | Failure Prevented | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Lock one behavior/support proof before editing. | Tracer bullets; OpenAI/GitHub task guidance; Ram | `keep-runtime` | Most behavior-changing rule for this facet. | State selected proof, non-goals, likely seam/areas, and validation target. | Issue-title implementation and scope drift. | keep for behavior flow |
| Prefer one real path over feature breadth. | *The Pragmatic Programmer*; GOOS; Patton | `keep-runtime` | Prevents whole-feature expansion. | The first path can produce meaningful feedback. | Building broad feature surface before proving the path. | keep for behavior flow |
| Treat support work as support. | Humanizing Work; engineering contract | `keep-runtime` | Keeps non-user-visible work honest. | Support work names its unblocker/de-risking purpose and validation. | Fake user-value language and support sprawl. | keep for behavior flow |
| Reduce variation to one required case. | Humanizing Work | `keep-runtime` | Directly prevents variation creep. | Non-required variants become follow-ups; required acceptance remains in scope. | Whole-feature implementation by accumulation. | keep for behavior flow |
| Keep related proof with the diff. | Google Small CLs; OpenAI Codex | `keep-runtime` | Prevents code-only completion and detached proof. | The slice has proof that would fail if the promise is wrong. | Validation theater and unproven output. | keep for behavior flow |
| Separate broad refactors from behavior. | Google Small CLs; di Biase | `keep-runtime` | Prevents tangled diffs. | Refactor is required for the slice, tiny/protected, split, or follow-up. | Cleanup drift and mixed concepts. | keep for behavior flow |
| Treat file spread as scope evidence. | Google Small CLs; Bosu | `keep-runtime` | Practical re-bound warning. | Every touched area has an in-scope reason. | Broad rewrites hidden behind low LOC. | keep for behavior flow |
| Stop broadening after failed proof. | Tracer feedback; OpenAI; SWE-agent | `keep-runtime` | Keeps validation failures from becoming scope creep. | Failure is classified as in-slice, adjacent, changed commitment, or environment. | Chasing unrelated tests/defects. | keep for behavior flow |
| Justify boundedness by proof, review, feedback, and recovery, not speed. | Kudrjavets; DORA | `keep-research` | Important guardrail but not a runtime action. | No synthesis/runtime claim says small changes merge faster. | Unsupported speed folklore. | keep as research only |
| Localize before editing. | Agentless; SWE-agent; OpenAI | `bridge-needed` | Good execution shape but source phrase is too agent-paper-shaped. | Read/search enough to identify the relevant seam before edits. | Broad autonomous wandering. | translate before keeping |
| Make the diff understandable cold. | Ram; Pascarella; Google | `bridge-needed` | Useful slice-level pressure, but final review/note details belong later. | Purpose, changed areas, and proof are understandable without scratch context. | Hidden reasoning and review confusion. | translate before keeping |
| Use bounded offloads only. | Agentic bridge sources | `keep-support` | Useful when subagents are used, but not central runtime behavior. | Helper output answers a narrow assigned question. | Multi-agent sprawl. | move to support |

## 5. Failure Mode Triage

| Failure Mode | Source | Category | Why | Skill Countermeasure | Evidence / Warning Sign | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Prototype drift | *The Pragmatic Programmer* / Artima | `keep-runtime` | Direct tracer-bullet hazard. | Scratch code is deleted or productionized and proved. | Scratch/spike code remains in final diff without proof. | keep for behavior flow |
| Horizontal slice / broken middle | Humanizing Work; GOOS | `keep-runtime` | Core bounded-slice failure. | Prove one behavior path or explicitly classify work as support. | Layer-only change claims behavior is done. | keep for behavior flow |
| Component masquerade | Humanizing Work | `keep-runtime` | Important for support-slice honesty. | State support purpose and validation. | Technical task has no behavior, unblocker, or proof. | keep for behavior flow |
| Variation creep | Humanizing Work | `keep-runtime` | Common implementation expansion path. | Keep required variants; record non-required variants. | Diff grows across rules/data/users/interfaces outside acceptance. | keep for behavior flow |
| Tangled/composite change | Ram / di Biase | `keep-runtime` | Strong one-concept split trigger. | Split, ask, or follow-up independent second concepts. | Summary becomes a list of unrelated fixes. | keep for behavior flow |
| File-spread blind spot | Google / Bosu | `keep-runtime` | Practical scope warning. | Re-bound and justify touched areas. | Many files/directories touched without one proof story. | keep for behavior flow |
| Tool-feedback overtrust | SWE-agent / OpenAI | `keep-runtime` | Prevents failed checks from widening the mission. | Classify failures before fixing. | Agent fixes failures unrelated to selected issue. | keep for behavior flow |
| Walking-skeleton overuse | GOOS / Patton | `keep-support` | Real risk, but conditional and too nuanced for core runtime. | Use only when system shape/proof path is uncertain. | Routine issue grows infrastructure. | move to support |
| Smallness speed myth | Kudrjavets | `keep-research` | Good synthesis guardrail, not execution. | Avoid speed claims. | Language says small changes merge faster. | keep as research only |
| Broad autonomous wandering | Agentic bridge sources | `bridge-needed` | Useful, but should become ordinary search/edit/prove language. | Localize before edit and keep failures in-scope. | Many files searched/edited without slice reason. | translate before keeping |
| Multi-agent sprawl | Agentic bridge sources | `reject` | Not core Facet 1 behavior unless delegation is in scope. | None in runtime; support may mention bounded offloads. | Helper returns adjacent opportunities. | reject |

## 6. Evidence Gate Triage

| Gate | Source | Category | Why | Too Weak If | Too Heavy If | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Slice lock | Tracer bullets; OpenAI/GitHub docs | `keep-runtime` | Checkable pre-edit boundary. | It names only an issue title. | It becomes a PRD/story-map exercise. | keep for behavior flow |
| One concept plus one proof story | Google; Ram; di Biase | `keep-runtime` | Best compact completion pressure for this facet. | The summary is a bag of fixes. | Coupled proof edits are split mechanically. | keep for behavior flow |
| Related proof travels with diff | Google Small CLs | `keep-runtime` | Keeps implementation and evidence together. | It says tests exist somewhere. | It pulls in unrelated test cleanup. | keep for behavior flow |
| Highest useful path proof | Tracer bullets; GOOS; Humanizing Work | `keep-runtime` | Avoids both syntax-only checks and mandatory slow E2E proof. | It checks only syntax or output existence. | It requires end-to-end infrastructure when a smaller seam proves the issue. | keep for behavior flow |
| Acceptance/success criteria named | OpenAI; GitHub; Anthropic; SBE | `keep-runtime` | Agent needs a proof target before editing. | It says "works" or "improve." | It demands all future variants. | keep for behavior flow |
| Every touched area has an in-scope reason | Google; Bosu | `keep-runtime` | Operationalizes file-spread warning. | It counts LOC only. | It becomes a full file inventory for every small edit. | keep for behavior flow |
| Reviewer information check | Pascarella; Ram; Google | `keep-support` | Useful finalization checklist, but mostly Facet 8. | It depends on hidden scratch work. | It repeats exploration logs. | move to support |
| Recovery/revertability check | DORA; Pascarella; Google | `owned-elsewhere` | Release/risk detail exceeds this facet. | Unrelated span is ignored. | It imports release ceremony. | move to support |
| Validation cannot run substitute | OpenAI / engineering contract | `owned-elsewhere` | Proof reporting belongs to Semantic Proof and Review/Lock. | It treats no validation as done. | It blocks all progress despite reasonable substitute evidence. | move to support |

## 7. Stop / Ask Rule Triage

| Condition | Source | Category | Why | Agent Should | Resume When | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Cannot state one behavior/support proof. | OpenAI/GitHub; Humanizing Work | `keep-runtime` | Prevents guesswork and project-bucket implementation. | Ask for missing commitment or propose a narrower slice. | Proof target, non-goals, and likely seam are concrete. | keep for behavior flow |
| Second independent concept appears. | Google; di Biase; Ram | `keep-runtime` | Best split/stop trigger. | Split, ask, or record follow-up. | Active diff returns to one concept or broader scope is approved. | keep for behavior flow |
| Proof failure points outside the locked slice. | Tracer feedback; OpenAI; SWE-agent | `keep-runtime` | Prevents validation-driven scope creep. | Classify as adjacent, changed commitment, environment, or in-slice. | New slice is approved or failure is shown to be in-scope. | keep for behavior flow |
| File spread grows beyond expected surface. | Google; Bosu | `keep-runtime` | Practical re-bound moment. | Re-bound and justify before continuing. | Each touched area supports selected proof. | keep for behavior flow |
| Broad refactor is needed. | Google Small CLs | `keep-runtime` | Prevents behavior/refactor tangles. | Split/ask unless tiny, local, required, and protected. | Refactor is separate, approved, or proven necessary for the slice. | keep for behavior flow |
| Walking skeleton implies architecture/dependency/tooling/public contract/data/security/privacy change. | GOOS; SWE@Google; GitHub | `keep-runtime` | Crisp commitment-boundary trigger. | Ask before implementing. | User approves changed commitment or smaller local path is chosen. | keep for behavior flow |
| Acceptance/success criteria are ambiguous. | OpenAI; GitHub; Anthropic | `keep-runtime` | Agent cannot prove done without a concrete target. | Ask or propose a narrow plan for approval. | Pass/fail proof is concrete enough to run or inspect. | keep for behavior flow |
| Broad, cross-repo, incident-like, security-critical, or deep-domain task. | GitHub Copilot docs | `owned-elsewhere` | Mostly readiness/triage/engineering-contract policy. | Reference contract or ask at the boundary. | User confirms scope/risk boundary. | move to support |
| Validation cannot run. | OpenAI; engineering contract | `owned-elsewhere` | More Semantic Proof / Review And Lock than slice boundary. | Record blocker and strongest substitute evidence. | Tools available or substitute evidence accepted. | move to support |
| Helper agents produce adjacent opportunities. | Agentic bridge sources | `reject` | Too specific to delegation workflow. | Integrate only assigned evidence if delegation is in play. | Adjacent work becomes approved slice. | reject |

## 8. Agentic Bridge Triage

| Source Concept | Agentic Translation | Category | Why | Agent Bridge Candidate | Action |
| --- | --- | --- | --- | --- | --- |
| Vertical/thin slice | Name one caller/operator path or support proof. | `bridge-needed` | Source term is good, runtime phrase is too product-shaped. | Lock selected path/proof before edits. | translate before keeping |
| Walking skeleton | Use only when system shape or proof path is uncertain. | `keep-support` | Nuance matters; default runtime term would be too heavy. | Conditional support note for uncertain new structure. | move to support |
| Localize-repair-validate | Read enough, edit narrowly, prove. | `bridge-needed` | Useful behavior, bad jargon. | Explore just enough to find the seam, then implement/prove narrowly. | translate before keeping |
| Tool feedback | Failed checks do not automatically expand the slice. | `keep-runtime` | Runtime-worthy only as scope classifier. | Classify failed proof before fixing. | keep for behavior flow |
| Reviewable change | One concept plus proof understandable without hidden context. | `bridge-needed` | Useful but overlaps `$review`/Facet 8. | Final slice check, not full review. | translate before keeping |
| Simple agent loop | Use plain search/edit/test/review/stop actions. | `keep-research` | Good anti-jargon guardrail. | Avoid framework vocabulary in later synthesis. | keep as research only |
| Coherent unit/thread | Do not let `$implement` become a project bucket. | `keep-runtime` | Strong direct agent behavior. | Finish or stop after one selected slice. | keep for behavior flow |

## 9. Owned-Elsewhere Check

| Item | Better Owner | Why | Keep Reference? |
| --- | --- | --- | --- |
| Ready-for-agent issue writing, issue creation, raw request triage, `AGENT-BRIEF` shape | `to-issues`, `triage`, repo tracker docs | Facet 1 starts from one selected issue. | Yes, boundary note only. |
| Acceptance criteria authoring and ready-enough intake checks | Facet 3 Context Intake, `triage`, `to-issues` | Facet 1 can notice missing proof target but should not own issue readiness. | Yes |
| Full TDD, red-green-refactor, outside-in testing, acceptance-test procedure | `$tdd`, Facet 5 Semantic Proof | Facet 1 only needs proof-boundary pressure. | Yes |
| Specific proof modes, fixtures, examples, Specification by Example depth | Facet 5 Semantic Proof, `$tdd` support docs | Too detailed for bounded-slice triage. | Yes |
| Baseline capture, dirty-work preservation, starting ref, commit isolation | Facet 2 Baseline And Fixed Point | Explicitly excluded from Facet 1 except slice boundary. | Yes |
| Fixed-point review mechanics and Standards/Spec review | `$review`, Facet 8 Review And Lock | Facet 1 may keep reviewability pressure, not full review procedure. | Yes |
| Implementation note details, residual risk, skipped-check format, commit readiness | Facet 8 Review And Lock | Final handoff belongs to closing facet. | Yes |
| Commitment changes: public contracts, architecture, dependencies, data/security/privacy semantics | Facet 4 Commitment Boundary, engineering contract, ADRs | Authority boundary, not slice-shaping detail. | Yes |
| Load-bearing internals, seam depth, interface/module proof choice | Facet 6 Seams And Internals, `codebase-design` | Facet 1 can say proof path; seam theory belongs elsewhere. | Yes |
| Cleanup/refactor disposal, scratch/prototype cleanup, behavior-preserving simplification | Facet 7 Protected Simplification, `codebase-cleanup` when relevant | Facet 1 rejects drift; detailed simplification gates come later. | Yes |
| Broad cleanup campaigns, architecture review, deepening candidates | `codebase-cleanup`, `improve-codebase-architecture`, `codebase-design` | Outside one implementation slice. | No |
| Story mapping workshops, backlog/release planning, product-owner procedure | `to-prd`, `to-issues`, research only | Product slicing is useful pressure; procedure would overtake `implement`. | Research only |
| Google-specific CL stacking, approval bits, ownership process | `$review`, repo docs, research only | Source-specific process, not portable runtime behavior. | Research only |
| Deployment/trunk-based delivery doctrine and release ceremony | engineering contract, Facet 8, research only | Small-batch rationale helps; release doctrine is too broad. | Research only |
| ACI, benchmark, leaderboard, and agent architecture terms | research only / reject | No direct bounded-slice behavior. | No |
| Hard PR-size, LOC, or guaranteed merge-speed claims | reject / research-only caution | Facet explicitly avoids numeric folklore and speed guarantees. | Research only |
| Multi-agent/subagent orchestration details | support/reference docs | Bounded offloads are useful only when delegation is in play. | Support only |

## 10. Rejection Log

| Item | Source | Rejection Reason | Do Not Revive Unless |
| --- | --- | --- | --- |
| "Keep it small" | Review/DORA summaries | Too vague; invites LOC thinking. | Translated into concept plus proof plus boundary. |
| "Do a vertical slice" | Product slicing sources | Slogan without observable path/proof. | It names caller/operator path and proof. |
| "Make progress" | Tracer/small-batch misread | Decorative; no done condition. | It defines feedback from a locked path. |
| "Add tests" | Google/OpenAI proof guidance | Default/testing theater. | The proof would fail if selected behavior were wrong. |
| "Avoid scope creep" | General bounded-slice idea | True but inert. | It becomes a second-concept, file-spread, or proof-failure gate. |
| "Be reviewable" | Reviewability sources | Aspirational and overlaps `$review`. | Limited to one concept plus proof understandable cold. |
| "Use walking skeleton" | GOOS/Patton | Too heavy for routine work. | System shape or feedback path is genuinely uncertain. |
| "Refactor as needed" | Google separate-refactor guidance | Invites cleanup drift. | Refactor is necessary for the slice and protected by proof. |
| "Run validation" | OpenAI/Codex guidance | Too vague; does not state what validation proves. | It names what the check proves. |
| "Well-scoped task" | GitHub coding-agent docs | Good source term, weak alone. | Expanded into problem, proof target, likely seam, and non-goals. |
| "Use agentic workflows" | Agentic papers/docs | Jargon and runtime bloat. | Reduced to plain actions. |
| "Autonomously solve it" | Agent autonomy lane | Encourages overreach. | Autonomy is explicitly bounded by the locked slice. |
| "Run tests if possible" | Validation escape hatch | Too easy to skip proof. | Replaced by focused proof and explicit skipped-check reason. |
| "Small PRs merge faster" | Kudrjavets contrast | Unsupported by the selected empirical source. | New evidence specifically supports the claim. |
| "Just add a follow-up" | Story slicing misuse | Can dodge required acceptance criteria. | Follow-up is only for non-required adjacent variation or separate concept. |
| "Spike it" | Humanizing Work spike caution | Open-ended research escape hatch. | Spike is a bounded question with a stop condition. |
| "MVP" | Product/delivery lane | Product-process heavy and ambiguous. | The facet intentionally expands to product release framing. |
| Story-map workshop procedure | Patton / Humanizing Work | Upstream product/backlog process, not implementation behavior. | The skill starts owning issue creation, which it should not. |
| Google CL stacking/approval bits | Google Small CLs / SWE@Google | Source-specific review process. | Repo review process needs this exact procedure. |
| ACI / leaderboard / benchmark terms | Agentic papers | Framework jargon with no runtime behavior. | Translated into a concrete agent action gate. |

## 11. Surviving Material

### Runtime Candidates

- `bounded slice`: central frame for one selected issue as one behavior/support
  proof.
- `tracer bullet`: may belong as the strongest leading word for one real
  behavior path, if paired with production-shaped proof.
- `support slice`: likely needed as an honest escape hatch for docs, config,
  tests, refactors, harness, and other support work.
- `one self-contained change`: compact gate for keeping code, rationale, and
  proof together.
- `one concept`: crisp stop/split signal when adjacent work appears.
- `file spread`: useful mid-run re-bound signal, without numeric thresholds.
- `success criteria`: keep as "proof target before editing", not issue-authoring
  procedure.
- Lock one behavior/support proof before editing.
- Keep related proof with the diff.
- Reduce variation to one required case and record non-required variants.
- Classify failed proof before fixing: in-slice, adjacent, changed commitment,
  or environment.
- Stop/split/ask on a second independent concept, broad refactor, file-spread
  expansion, or proof outside the slice.

### Support Candidates

- Conditional walking-skeleton note: use only when system shape or proof path is
  uncertain.
- Support-slice taxonomy for docs/config/tests/refactor/harness work.
- Weak/no-op phrase table as a pruning checklist for later prompts.
- Boundary matrix for Facet 1 versus Facets 2-8 and `tdd`/`review`/`triage`.
- Reviewability evidence notes from Ram/Pascarella/Bosu as support for later
  Review And Lock.
- Small-batch anti-overclaim guardrail: boundedness is for proof, review,
  feedback, and recovery, not guaranteed speed.
- Agentic bridge cleanup: translate papers into plain search/edit/prove/stop
  actions.
- Bounded offloads note for runs that use helper agents.

### Research-Only Material

- Story-mapping workshops, backlog/release planning, and product-owner
  procedure.
- Small-batch delivery doctrine and trunk/release mechanics.
- Google CL stacking, approval bits, and ownership process.
- Full empirical study details and reviewer taxonomy.
- Specification by Example depth, unless later Semantic Proof promotes it.
- Reinertsen/Cockburn/SPIDR/Elephant Carpaccio gap notes from Prompt 03.
- Speed/merge-time contrast from Kudrjavets, except as a synthesis guardrail.

### Bridge-Needed Material

- `vertical slice`: translate to one caller/operator path or support proof.
- `walking skeleton`: translate to conditional use when system shape/proof path
  is uncertain.
- `localize-repair-validate`: translate to read enough, edit narrowly, prove.
- `tool feedback`: translate to failed checks do not automatically expand the
  slice.
- `reviewable change`: translate to one concept plus proof understandable
  without hidden scratch context.
- `highest useful path proof`: needs crisp wording so it avoids both syntax-only
  checks and mandatory end-to-end proof.

## 12. Handoff To Agent Bridge

Strongest runtime candidates:

- lock one behavior/support proof before editing;
- `tracer bullet` as one real path, if kept tied to production-shaped proof;
- `support slice` as an honest category for non-behavior implementation work;
- one self-contained change / one concept;
- related proof travels with the diff;
- file spread as re-bound signal;
- proof-failure classification before fixing;
- required variation versus adjacent follow-up.

Strongest support/reference candidates:

- conditional walking skeleton;
- support-slice taxonomy;
- weak/no-op phrase table;
- owner/boundary matrix;
- small-batch anti-overclaim note;
- reviewability evidence notes for later facets.

Material that needs bridge translation:

- vertical/thin slice;
- localize-repair-validate;
- tool feedback;
- reviewable change / cold reviewer;
- highest useful path proof.

Biggest rejected temptation:

- carrying all attractive source vocabulary forward. Runtime should not become
  story mapping, delivery economics, code-review doctrine, or agent-framework
  jargon.

Ownership conflicts to watch:

- `$tdd` owns red-green-refactor and detailed proof mechanics.
- `$review` and Facet 8 own fixed-point review, final note detail, skipped
  checks, and residual-risk reporting.
- `triage` and `to-issues` own ready issue creation and issue-brief shape.
- Facet 4 and the engineering contract own commitment-boundary authority.
- Facet 6 owns seam depth and load-bearing internals.
- Facet 7 owns protected simplification and scratch/refactor disposal.

Prompt 06 should first turn this into an execution chain:

1. Lock one behavior/support proof, non-goals, likely touched areas, and
   validation target.
2. Choose the smallest real path or support unblocker that satisfies the
   selected issue.
3. Implement only that concept.
4. Keep proof attached to the diff.
5. Classify drift, file spread, failed proof, broad refactor, and second
   concepts before continuing.
6. Record adjacent work as follow-up instead of absorbing it.
