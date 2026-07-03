# Prompt 10: Plain-Language Validation Candidate For Implement Facet 1

This executes
[`docs/synthesis/methods/prompts/10-plain-language-validation-candidate.md`](../../../methods/prompts/10-plain-language-validation-candidate.md)
for `implement`.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/current/implement/SKILL.md`

Facet or scope: `1 - Ready Issue Selection`

Detailed skill-context draft:
[`09-detailed-skill-context-draft.md`](09-detailed-skill-context-draft.md)

Draft decision: `ready-for-plain-language-candidate`

Traceability map and validation scenarios: Prompt 09 Sections 8 and 10.

Existing skill text: `skills/current/implement/SKILL.md`, especially
`### 1. Select The Issue`.

Revision feedback: none.

Subagent inputs used:

- Schema pass: no prior Prompt 10 artifact exists; use the current seven-section
  Prompt 10 schema and decision `ready-for-reality-validation`.
- Plain-language pass: compress the replacement section into short gates while
  preserving issue-equivalent selection, readiness, owner boundaries, and
  selection facts.
- Validation pass: preserve V1-V12, with first validation pressure on `A4`,
  V3/V11/V12, readiness, owner-boundary, and handoff behavior.

Do not edit `SKILL.md` in this prompt.

## 1. Plain-Language Candidate Scope

Skill and facet:

- `implement`, Facet 1 - `Ready Issue Selection`

Detailed skill-context draft used:

- [`09-detailed-skill-context-draft.md`](09-detailed-skill-context-draft.md)

Prompt 09 draft decision used:

- `ready-for-plain-language-candidate`

Existing behavior that must not regress:

- `implement` still selects and implements one ready-for-agent issue;
- explicit issue, path, or URL targets still work when they name one
  issue-equivalent item;
- PRDs/specs/source documents can identify one ready item but cannot become
  implementation scope by themselves;
- no-input selection still uses repo tracker docs, ready labels, and
  dependency/order policy to select the next unblocked ready item;
- tracker-state eligibility and explicit-target no-substitution remain runtime
  gates;
- ambiguous order asks, no ready item stops, and blocked work waits;
- local readiness checks do not become full Context Intake, proof planning, or
  issue repair;
- owner-owned work stays outside `implement`;
- selection facts are recorded before file discovery, planning, proof strategy,
  edits, or Context Intake.

This pass will not decide final runtime text, edit `SKILL.md`, validate against
real tasks, final-prune the skill, create support docs, define tracker syntax,
define high-risk policy, or add behavior not present in Prompt 09.

## 2. Revision Feedback Disposition

No revision feedback to disposition.

## 3. Leading Word And Gate Plan

| Draft Meaning | Leading Word / Gate | Keep / Merge / Cut | Why |
| --- | --- | --- | --- |
| One concrete implementation target | `one issue-equivalent item`; "No one item, no implementation." | Keep | Carries V1 and prevents queue/PRD/batch pickup. |
| Valid explicit issue/path/URL targets | `issue-equivalent item`; `path-backed ready slice` | Keep | Preserves current explicit target behavior and V3. |
| Broad source surfaces are not scope | "not implementation scope by itself" | Keep | Keeps PRD/spec/path source work routed without becoming `to-issues`. |
| Source docs may identify one ready item | "use those sources only to find one ready item" | Keep | Preserves V2 and V12 without decomposition. |
| Selection authority | `explicit user target` / `repo-visible ready/order policy` | Keep | Prevents invented priority and preserves V4. |
| No-input tracker path | `next unblocked ready item` | Keep | Preserves existing skill behavior and V11. |
| Tracker-state eligibility | `tracker-state eligibility` | Keep | Protects `A4`; exact labels stay in tracker docs. |
| Explicit target ineligible | "stop on that target"; "Do not substitute" | Keep | Blunt gate for V4. |
| Local readiness | `readiness gate` | Keep | Compresses four readiness facts into one checklist. |
| Agent-prompt adequacy | "fresh coding agent can start Context Intake without issue repair" | Keep | Preserves V6 without requiring full context. |
| Observable done signal | "expected behavior, repro, doc target, validation hint, or done condition" | Keep | Preserves V6 without proof planning. |
| Blockers/dependencies | "Blocked work waits" | Keep | Preserves V7. |
| Result-defining ambiguity | "Ask only after naming the missing fact..." | Keep | Preserves V8 without "ask if unsure." |
| Owner boundary | "Detect unready work; do not make it ready" | Keep | Preserves V9 and prevents triage drift. |
| Obvious multi-item candidate | "ask for one ready item or hand off upstream" | Keep | Preserves O2 as ask/handoff, not slicing. |
| Selection handoff | `Select first, plan later` | Keep | Preserves V10 and prevents phase collapse. |
| High-risk policy | Engineering contract pointer | Cut from runtime candidate | Prompt 09 kept `O3` support-only. |
| Source-process rationale | WIP/DoR/Scrum rationale | Cut | Research/support material, not validation candidate. |

## 4. Plain-Language Candidate Text

```markdown
### 1. Select The Issue

Select exactly one issue-equivalent item before Context Intake: one issue, URL,
tracker item, path-backed ready slice, or explicit user-selected work item. A
queue, PRD, spec, batch, list, or bare source path is not implementation scope
by itself. Use those sources only to find one ready item. If they do not name
one, ask for the target item or hand off to `to-issues`. Use an explicit path
or URL when it already names one issue-equivalent item. No one item, no
implementation.

Use an explicit user target or repo-visible ready/order policy. Do not invent
priority or readiness. If no item is provided, use repo tracker docs, ready
labels, and repo-visible dependency/order policy to pick the next unblocked
ready-for-agent item. If multiple eligible items are ready but unordered, ask.
If no ready item exists on the checked surface, stop and report that surface.

For tracker items, confirm tracker-state eligibility through repo tracker docs.
If an explicit tracker target is ineligible, stop on that target. Do not
substitute another issue. Do not edit tracker metadata here.

Before pickup, run the readiness gate:

- tracker state is eligible, when a tracker item is involved;
- the prompt can guide a fresh coding agent into Context Intake without issue
  repair;
- there is an observable done signal;
- blockers and dependencies allow this item to be worked now;
- no unresolved ambiguity would change the expected result.

Blocked work waits unless the selected item is the blocker or repo-visible
order says this item comes next.

When asking, name the missing fact and how it would change the expected result.

Detect unready work; do not make it ready inside `implement`. Do not repair,
promote, relabel, rewrite, split, reprioritize, or mutate tracker state during
selection. If the candidate contains multiple independent outcomes, items, or
unrelated surfaces, ask for one ready item or hand off upstream.

Record the selected item identity, checked surface, selection authority,
tracker eligibility when relevant, readiness facts, and selection outcome
before file discovery, implementation planning, proof strategy, edits, or
Context Intake. Select first, plan later.
```

## 5. Preservation Check

| Prompt 09 Behavior / Line IDs | Preserved In Plain-Language Text | Risk |
| --- | --- | --- |
| `R1`, `R4`: exactly one item; no one item, no implementation | Opening paragraph and blunt gate | Prompt 11 must ensure this blocks queues and batches. |
| `R5`: issue, URL, tracker item, path-backed ready slice, explicit target | Opening definition | Final prune could remove path/URL protection. |
| `R2`, `R3`: PRD/spec/source/path handling | Source-surface sentences and `to-issues` handoff | Prompt 11 must distinguish valid path target from bare source path. |
| `A1`: explicit user target or repo-visible policy | Selection authority paragraph | "Ready/order policy" must not let the agent invent priority. |
| `A2`: unordered multiple candidates ask | "multiple eligible items... ask" | Ask target is concise; Prompt 11 should test ambiguous order. |
| `A3`: no ready item stops | "stop and report that surface" | Reporting must not become issue creation or repair. |
| `A4`: tracker eligibility and no substitution | Tracker eligibility paragraph and readiness checklist | Highest-risk compression; Prompt 11 should test ineligible explicit target. |
| `L1`, `L2`, `L3`: readiness gate, prompt adequacy, done signal | Readiness checklist | "Observable done signal" is compressed; validation must prove it is understood. |
| `L4`: blocker/dependency state | Readiness checklist plus blocked-work gate | Prompt 11 should test blocked candidate. |
| `L5`: result-defining ambiguity ask | Missing-fact ask line | Must not become generic "ask if unsure." |
| `L6`: no readiness facts, no pickup | Checklist plus stop/ask gates | The exact phrase is merged, not repeated. |
| `O1`: detect unready work, do not make it ready | Owner-boundary paragraph | Forbidden-operation list may be final-pruned after validation. |
| `O2`: multi-outcome/item/surface ask or handoff | Owner-boundary paragraph | Must not become slicing. |
| `H1`, `H2`, `H3`: record selection facts before later phases | Final paragraph and `Select first, plan later` | Prompt 11 must test no Context Intake before facts are recorded. |
| `O3`, `L7`, `O4`, `S1`, `O5`, `H4`, `S2` | Not included | Correctly cut/deferred; no runtime behavior loss. |

## 6. Reality Validation Handoff

| Plain-Language Candidate Area | Prompt 09/10 Validation IDs | What Prompt 11 Should Test First | Pass / Fail Signal |
| --- | --- | --- | --- |
| One issue-equivalent item gate | `V1-single-item` | Batch, queue, or project request with no one item. | Pass: stops/asks; fail: starts implementation. |
| Source-surface handling | `V2-prd-source-handoff`, `V12-prd-identifies-one-ready-item` | PRD/spec/source document with and without one named ready item. | Pass: selects only the one ready item or routes to `to-issues`; fail: implements whole source. |
| Path/URL acceptance | `V3-path-backed-slice` | Explicit path/URL that already names one ready slice versus bare source path. | Pass: accepts ready path/URL, rejects bare source path; fail: overblocks or overaccepts. |
| Selection authority and ineligible explicit target | `V4-authority` | Named tracker issue is ineligible. | Pass: stops on that target without substitution or metadata edits; fail: chooses another issue or edits labels. |
| No-ready surface | `V5-no-ready` | Checked surface has no ready item. | Pass: stops and reports surface; fail: creates/repairs/promotes work. |
| Local readiness | `V6-readiness` | Ready-labeled item lacks prompt adequacy or done signal. | Pass: stops or asks narrowly; fail: proceeds from unusable issue. |
| Blockers/dependencies | `V7-blocker` | Candidate has unresolved blocker. | Pass: waits unless candidate is blocker or order says now; fail: works blocked item. |
| Result-defining ambiguity | `V8-ambiguity` | Missing fact would change expected result. | Pass: names fact and result effect; fail: asks vaguely or invents. |
| Owner boundary | `V9-owner-boundary` | Candidate needs repair, relabeling, splitting, or issue authoring. | Pass: asks/hands off; fail: mutates or decomposes inside `implement`. |
| Selection handoff | `V10-selection-boundary` | Candidate passes selection. | Pass: records identity, surface, authority, eligibility/readiness facts, and outcome before Context Intake; fail: starts discovery/planning first. |
| No-input tracker selection | `V11-next-ready-from-tracker` | No target and exactly one next unblocked `ready-for-agent` item exists. | Pass: selects it using repo-visible authority before Context Intake; fail: asks unnecessarily or picks by taste. |

Prompt 11 should test first:

1. `V4-authority`
2. `V11-next-ready-from-tracker` plus `V10-selection-boundary`
3. `V3-path-backed-slice` plus `V12-prd-identifies-one-ready-item`
4. `V6-readiness` plus `V8-ambiguity`
5. `V9-owner-boundary`

## 7. Plain-Language Candidate Decision

Plain-language candidate decision: `ready-for-reality-validation`

Artifact path:

`docs/synthesis/facets/implement/FACET-1-READY-ISSUE-SELECTION/10-plain-language-validation-candidate.md`

Text areas ready for validation:

- one issue-equivalent item gate;
- source-surface and explicit path/URL handling;
- selection authority and no-input next-ready selection;
- tracker-state eligibility and no-substitution;
- local readiness gate;
- owner-boundary stop/handoff;
- selection-facts handoff before Context Intake.

Behavior or line IDs preserved:

- `R1`, `R2`, `R3`, `R4`, `R5`;
- `A1`, `A2`, `A3`, `A4`;
- `L1`, `L2`, `L3`, `L4`, `L5`, `L6`;
- `O1`, `O2`;
- `H1`, `H2`, `H3`;
- validation IDs `V1` through `V12`.

Behavior or line IDs cut or merged and why:

- `L6` is merged into the readiness checklist and stop/ask gates.
- `H3` is merged into the final selection-facts handoff.
- `O3` remains out of runtime because high-risk policy belongs to the
  engineering contract / repo docs.
- `L7`, `O4`, and `S1` remain support placeholders only.
- `O5`, `H4`, and `S2` remain cut as duplicate, meta, or rationale bloat.

Validation scenarios Prompt 11 should run first:

- `V4-authority`
- `V11-next-ready-from-tracker`
- `V10-selection-boundary`
- `V3-path-backed-slice`
- `V12-prd-identifies-one-ready-item`
- `V6-readiness`
- `V8-ambiguity`
- `V9-owner-boundary`

Likely final-prune targets after validation:

- concrete examples in the issue-equivalent definition if V3 stays protected;
- the forbidden-operation list in the owner-boundary paragraph;
- duplicate tracker-state eligibility between the tracker paragraph and
  readiness checklist;
- the final `Select first, plan later` sentence if the preceding sentence
  carries the boundary strongly enough.
