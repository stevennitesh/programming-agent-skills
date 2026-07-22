# Facet 1: Bounded Slice Agent Bridge

Historical source-to-skill Prompt 06 artifact for `implement` Facet 1.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Facet: `1. Bounded Slice`

Facet research question: How do strong teams keep one implementation run small,
valuable, independently provable, and reviewable?

Facet boundaries:

- Owns: slice lock, one-path implementation pressure, support-slice honesty,
  adjacent-work handling, proof-boundary scope pressure, stop/split behavior.
- Does not own: baseline/fixed-point mechanics, full context intake,
  commitment authority, TDD procedure, seam-depth theory, protected
  simplification, fixed-point review, implementation notes, or commit readiness.
- Should answer: how an agent keeps one selected request as one bounded,
  independently provable behavior or support slice.
- Should not answer: how to author the issue, run the full proof discipline,
  redesign the module, or close the implementation.

Source triage packet:
[`docs/research/skill-facets/implement/FACET-1-BOUNDED-SLICE-triage.md`](../../../../research/skill-facets/implement/FACET-1-BOUNDED-SLICE-triage.md)

## 1. Agent Bridge Scope

This behavior flow converts the Prompt 05 triage packet for `implement` Facet 1:
`Bounded Slice`.

Surviving material in scope:

- runtime leading words: `bounded slice`, `tracer bullet`, `support slice`,
  `one self-contained change`, `one concept`, `file spread`, and `success
  criteria`;
- runtime behavior rules: lock one behavior/support proof before editing,
  prefer one real path over breadth, treat support work as support, reduce
  variation to required cases, keep related proof with the diff, separate broad
  refactors, treat file spread as scope evidence, and classify failed proof
  before fixing;
- runtime gates: one concept plus one proof story, proof target named before
  editing, highest useful path proof, every touched area in scope, and
  broad-refactor split pressure;
- runtime stop rules: missing proof target, second independent concept, failed
  proof outside the slice, file spread beyond expected surface, broad refactor,
  ambiguous success criteria, or walking-skeleton work crossing a commitment
  boundary.

Material intentionally left for support/reference:

- conditional walking-skeleton guidance;
- support-slice taxonomy for docs, config, tests, harnesses, and refactors;
- weak/no-op phrase table for later pruning;
- boundary matrix against Facets 2-8, `$tdd`, `$review`, and repo engineering
  contracts;
- reviewability evidence notes;
- small-batch anti-overclaim guardrails;
- agentic bridge cleanup for translating source jargon into plain
  search/edit/prove/stop behavior;
- bounded offload notes for runs using helper agents.

This flow must not decide final runtime wording, generous synthesis prose,
specific validation mechanics, acceptance-criteria authoring, baseline capture,
commitment authority, seam-depth design, simplification procedure, final review,
implementation-note format, or commit behavior.

## 2. Runtime Candidate Inventory

| Candidate | Type | Why It Survived | Behavior Role |
| --- | --- | --- | --- |
| `bounded slice` | leading word | It is the facet's central concept and already matches local repo language. | Frame the run as one selected request converted into one behavior/support proof. |
| `tracer bullet` | leading word | It names one real, production-shaped path that produces feedback. | Prefer a meaningful path through the system over broad feature surface. |
| `support slice` | leading word | It keeps docs/config/tests/refactor/harness work honest when no user-visible path exists. | Require an unblocker or de-risking purpose plus validation for non-behavior work. |
| `one self-contained change` | evidence gate | It keeps code, rationale, and proof traveling together. | Finish only when the diff can be understood as one change with attached proof. |
| `one concept` | stop/ask rule | It gives a crisp split signal for adjacent work. | Stop, split, or record follow-up when an independent second concept appears. |
| `file spread` | failure mode | It is a practical warning that the run may be widening even when LOC stays low. | Re-bound and justify each touched area when files/directories spread. |
| `success criteria` / proof target | evidence gate | The agent cannot prove a slice without a pass/fail target. | Name what proof must confirm before editing. |
| Lock one behavior/support proof before editing | behavior rule | It prevents issue-title implementation and early wandering. | State selected path or support purpose, non-goals, likely touched area, and validation target. |
| Prefer one real path over breadth | behavior rule | It counters horizontal slicing and whole-feature expansion. | Build the first meaningful path before broadening variants or surfaces. |
| Reduce variation to required cases | behavior rule | It prevents accumulated optional variants from becoming the slice. | Keep required acceptance criteria in scope and record non-required variants as follow-ups. |
| Keep related proof with the diff | evidence gate | It prevents code-only completion and detached validation. | Ensure the proof would fail or become suspect if the slice promise were wrong. |
| Classify failed proof before fixing | stop/ask rule | It prevents validation feedback from silently widening scope. | Decide whether a failure is in-slice, adjacent, changed commitment, or environment/tooling. |
| Split broad refactors from behavior | stop/ask rule | It prevents cleanup or design work from tangling with the behavior change. | Allow only tiny, local, required, protected refactors inside the slice. |
| Failed checks do not automatically expand scope | failure mode | Tool feedback is useful only when interpreted against the locked slice. | Fix only failures justified as in-slice; otherwise ask, split, follow up, or report blocker. |

## 3. Support / Reference Inventory

| Candidate | Why It Belongs In Support | Runtime Pointer Needed? |
| --- | --- | --- |
| Conditional walking skeleton | Useful when system shape or proof path is genuinely uncertain, but too heavy as default runtime advice. | Yes: mention only as an uncertain-path support option. |
| Support-slice taxonomy | Helps classify docs/config/tests/refactor/harness work without bloating `SKILL.md`. | Yes: runtime should require purpose and validation. |
| Weak/no-op phrase table | Helps later prompts prune slogans such as "keep it small", "be reviewable", and "run validation". | No, unless final wording drifts into slogans. |
| Boundary matrix | Prevents Facet 1 from absorbing baseline, TDD, commitment, seam, simplification, and review behavior. | Yes: runtime should point out handoffs, not restate procedures. |
| Reviewability evidence notes | Useful for later Review And Lock synthesis, but Facet 1 only needs one-concept-plus-proof pressure. | Light pointer only. |
| Small-batch anti-overclaim guardrail | Preserves source nuance that boundedness is not a guaranteed speed claim. | No direct runtime pointer. |
| Agentic bridge cleanup | Keeps research-paper vocabulary out of final skill language. | No direct runtime pointer. |
| Bounded offloads note | Useful only when helper agents are used; not a core implement behavior. | Maybe: support docs can warn that offloads answer assigned questions only. |

## 4. Behavior Sequence

### Step 1: Lock The Slice Before Editing

Trigger / situation:

- One ready request or issue has been selected for `implement`, but editing has
  not started.

Agent action:

- Name the selected behavior path or support purpose.
- Name the proof target, non-goals, likely touched area or seam, and validation
  target.
- If the work is not user-visible behavior, classify it as a `support slice`
  and state the unblocker or de-risking purpose.

Leading words:

- `bounded slice`
- `support slice`
- `success criteria`

Evidence gate:

- The slice can be stated as one behavior/support proof, not just an issue title
  or project bucket.

Stop / ask / continue rule:

- Stop, ask, or propose a narrower slice if the proof target, non-goals, or
  likely area cannot be stated concretely.
- Continue when the slice has a checkable proof target and boundary.

Failure prevented:

- Issue-title implementation, project-bucket execution, and early scope drift.

Source pressure:

- `Lock one behavior/support proof before editing`.
- `Cannot state one behavior/support proof`.
- `Acceptance/success criteria named`.

Next:

- Step 2: Localize Enough To Avoid Wandering.

### Step 2: Localize Enough To Avoid Wandering

Trigger / situation:

- The slice is locked, but the relevant code path, caller/operator path, or
  support surface is not concrete enough to edit.

Agent action:

- Read and search only enough to identify the path or surface that belongs to
  the locked proof.
- Treat broad exploration as evidence that the slice may need re-bounding.

Leading words:

- `tracer bullet`
- `one concept`
- `file spread`

Evidence gate:

- The agent can explain why the likely touched area belongs to the selected
  proof.

Stop / ask / continue rule:

- Continue once the edit surface is bounded.
- Re-bound, split, or ask if exploration spreads into unrelated areas or
  reveals a different commitment.

Failure prevented:

- Broad autonomous wandering and layer/component work detached from the proof.

Source pressure:

- `Localize before editing`.
- `Broad autonomous wandering`.
- `Vertical/thin slice` translated into one caller/operator path or support
  proof.

Next:

- Step 3: Implement One Real Path Or Honest Support Slice.

### Step 3: Implement One Real Path Or Honest Support Slice

Trigger / situation:

- A bounded path or support surface is known.

Agent action:

- Make the smallest production-shaped change that proves one required case.
- For support work, make the smallest change that unblocks or de-risks the
  selected future behavior, with its own concrete validation.
- Keep scratch/spike code out of the final diff unless it is productionized and
  proved.

Leading words:

- `tracer bullet`
- `support slice`
- `one self-contained change`

Evidence gate:

- The diff advances one concept and has a proof story that would fail or become
  suspect if the slice promise were wrong.

Stop / ask / continue rule:

- Stop, split, or record a follow-up when a second independent concept,
  optional variant, or broad refactor appears.
- Continue when coupled edits are required for the same proof story.

Failure prevented:

- Horizontal slices, component masquerade, prototype drift, and whole-feature
  expansion.

Source pressure:

- `Prefer one real path over feature breadth`.
- `Treat support work as support`.
- `One concept plus one proof story`.
- `Prototype drift`.

Next:

- Step 4: Keep Scope Pressure During The Diff.

### Step 4: Keep Scope Pressure During The Diff

Trigger / situation:

- The diff starts spreading across files, directories, concepts, variants, or
  enabling support changes.

Agent action:

- Re-check every touched area against the locked proof.
- Keep required variants in scope and move non-required variants to follow-up.
- Allow refactor only when it is tiny, local, required for the slice, and
  protected by the slice proof.

Leading words:

- `file spread`
- `one concept`
- `bounded slice`

Evidence gate:

- Every touched area has an in-scope reason tied to the selected proof.

Stop / ask / continue rule:

- Continue if the spread is necessary for the selected proof.
- Split, ask, or follow up if the spread reveals a second concept, optional
  variant, broad refactor, or changed commitment.

Failure prevented:

- Tangled/composite changes, variation creep, file-spread blind spots, and
  behavior/refactor tangles.

Source pressure:

- `Treat file spread as scope evidence`.
- `Reduce variation to one required case`.
- `Separate broad refactors from behavior`.
- `Second independent concept appears`.

Next:

- Step 5: Classify Proof Feedback Before Fixing.

### Step 5: Classify Proof Feedback Before Fixing

Trigger / situation:

- A check, test, manual inspection, or other proof path fails or exposes
  adjacent problems.

Agent action:

- Classify the failure before fixing it:
  `in-slice`, `adjacent`, `changed commitment`, or `environment/tooling`.
- Fix only failures justified as in-slice.
- For other failures, stop widening and ask, split, record follow-up, or report
  the blocker through later proof/review facets.

Leading words:

- `tool feedback`
- `success criteria`
- `bounded slice`

Evidence gate:

- The next fix is justified by the failure classification and the locked proof.

Stop / ask / continue rule:

- Continue for in-slice failures.
- Ask before changed commitments.
- Split or follow up for adjacent work.
- Report environment/tooling blockers without expanding the slice.

Failure prevented:

- Tool-feedback overtrust, validation-driven scope creep, and unrelated fixes.

Source pressure:

- `Stop broadening after failed proof`.
- `Proof failure points outside the locked slice`.
- `Failed checks do not automatically expand scope`.

Next:

- Step 6: Finish The Slice As Self-Contained.

### Step 6: Finish The Slice As Self-Contained

Trigger / situation:

- The implementation and proof are in place or the slice is blocked.

Agent action:

- Check that code, rationale, and proof travel together as one
  self-contained change.
- Confirm the result remains one concept plus one proof story.
- Leave unrelated adjacent work outside the slice for later facets to capture
  as residual risk, follow-up, or issue notes.

Leading words:

- `one self-contained change`
- `one concept`
- `bounded slice`

Evidence gate:

- A cold reader can understand the slice as one concept with attached proof,
  without hidden scratch context.

Stop / ask / continue rule:

- Do not call the facet complete if proof is missing, detached, syntax-only when
  behavior proof is available, or if unresolved adjacent work is required for
  acceptance.
- Handoff to Semantic Proof, Protected Simplification, Review And Lock, and
  commit behavior rather than restating them here.

Failure prevented:

- Code-only completion, detached proof, hidden reasoning, and Facet 1 absorbing
  final review/commit behavior.

Source pressure:

- `Keep related proof with the diff`.
- `Make the diff understandable cold`.
- `One self-contained change`.
- Owned-elsewhere table for `$tdd`, `$review`, Facets 5, 7, and 8.

Next:

- Handoff to later `implement` facets and any invoked specialized skill such as
  `$tdd` or `$review`.

## 5. Branches

| Branch | Trigger | Behavior | Gate | Rejoin / Exit |
| --- | --- | --- | --- | --- |
| Support slice | The request is docs, config, tests, harness, refactor, or other support work rather than direct user-visible behavior. | Classify it as support; name the unblocker/de-risking purpose, smallest proof, and non-goals. | Support purpose and validation are concrete; runtime does not pretend the work is user behavior. | Rejoin after Step 1 once proof is locked; exit/ask if no support proof or unblocker can be named. |
| Uncertain walking-skeleton path | System shape or feedback path is genuinely uncertain. | Build only enough executable path to establish meaningful feedback for the selected slice. | Skeleton is minimal, tied to selected proof, and does not cross architecture, dependency, tooling, public-contract, data, security, or privacy commitments without approval. | Rejoin once proof path exists; ask before commitment-boundary changes; reject for routine issues. |
| Second concept appears | An adjacent independent fix, feature, refactor, or variant appears. | Split, ask, or record follow-up instead of absorbing it. | Active diff still has one concept plus one proof story. | Rejoin when back to one concept; exit/ask if broader scope is required. |
| Proof failure outside slice | A check or inspection fails and may be adjacent, environment/tooling, or a changed commitment. | Classify before fixing. | Fix is taken only if failure is proven in-scope. | Rejoin if in-slice; exit, ask, or follow up if adjacent/changed/environment. |
| File spread | Touched files or directories grow beyond the expected surface. | Re-bound and justify each touched area against the proof. | Every touched area is in-scope and tied to the proof story. | Rejoin if justified; split/ask if spread reveals a second concept or broader commitment. |
| Broad refactor | A refactor seems useful or necessary while implementing behavior. | Allow only if tiny, local, required for the slice, and protected; otherwise split, ask, or record follow-up. | Refactor is necessary for the slice, not a separate cleanup concept. | Rejoin if tiny/local/proved; exit/ask if broad. |

## 6. Completion Criteria

| Criterion | What It Proves | How Agent Checks It | Too Weak If | Too Heavy If |
| --- | --- | --- | --- | --- |
| Slice lock explicit before editing | The run starts from one bounded behavior/support proof. | Check for proof target, non-goals, likely seam/areas, and validation target. | It names only the issue title. | It becomes PRD, story-map, or readiness authoring. |
| Success criteria are pass/fail enough | Done is knowable before implementation. | Confirm what behavior/support outcome the proof must confirm. | It says "works", "improve", or "add tests". | It demands all future variants or full product completion. |
| One real path or support purpose selected | The slice is not a layer-only or component-only claim. | Behavior slice names one caller/operator path; support slice names unblocker/de-risking purpose and validation. | A layer/component change pretends behavior is complete. | A walking skeleton is required for routine issues. |
| One concept plus one proof story holds | The diff remains reviewable and independently provable. | Summarize the result as one concept with attached proof. | The summary is a bag of fixes. | Legitimately coupled proof edits are split mechanically. |
| Related proof travels with diff | Evidence belongs to the change, not somewhere else. | Confirm the proof would fail or become suspect if the slice promise were wrong. | It says tests exist somewhere. | It pulls in unrelated test cleanup or full proof mechanics. |
| Highest useful proof path chosen | The proof is meaningful without becoming ceremony. | Select the smallest meaningful check that proves the selected boundary. | It checks only syntax, formatting, or output existence when behavior proof is available. | It requires slow end-to-end infrastructure when a smaller seam proves the slice. |
| Variation reduced to required cases | The slice satisfies required acceptance without accumulating optional breadth. | Required variants remain in scope; non-required variants become follow-ups. | Adjacent variants are silently added. | Required acceptance criteria are deferred. |
| File spread justified by slice | Physical diff spread does not hide scope drift. | Every touched area has an in-scope reason. | It only counts LOC or files. | It requires a full inventory for tiny edits. |
| Refactor, if present, is slice-bound | Cleanup does not become a separate concept. | Refactor is tiny, local, required, and protected, or it is split/followed up. | It says "refactor as needed". | It blocks a small enabling edit required for proof. |
| Failed proof classified before fixing | Tool feedback does not expand the mission by default. | Classify failure as in-slice, adjacent, changed commitment, or environment/tooling. | The agent chases unrelated failures. | It becomes full skipped-validation reporting or review procedure. |

## 7. Stop / Ask Rules

| Rule | Stop / Ask / Narrow / Continue | Why | Resume Condition |
| --- | --- | --- | --- |
| Cannot state one behavior/support proof | Ask or propose a narrower slice. | The agent cannot prove a project bucket. | Proof target, non-goals, and likely seam/area are concrete. |
| Acceptance or success criteria are ambiguous | Ask or narrow. | Done is unknowable without a pass/fail target. | Checkable outcome is concrete enough to run or inspect. |
| Second independent concept appears | Narrow, split, ask, or record follow-up. | A composite diff is no longer one bounded slice. | Active work returns to one concept or broader scope is approved. |
| Proof failure points outside locked slice | Stop widening and classify first. | Validation feedback can become unrelated work. | Failure is proven in-scope or a new slice is approved. |
| File spread exceeds expected surface | Narrow or justify before continuing. | Spread is evidence of possible scope drift. | Each touched area supports the selected proof. |
| Broad refactor is needed | Ask or split unless tiny, local, required, and protected. | Behavior and cleanup tangle easily. | Refactor is approved, separate, or proven necessary for the slice. |
| Support work lacks unblocker/de-risking purpose | Ask or narrow. | Support work without purpose becomes technical drift. | Purpose and validation are explicit. |
| Walking skeleton crosses commitment boundary | Ask. | Architecture, dependency, tooling, public-contract, data, security, and privacy shifts are user-owned commitments. | User approves the changed commitment or a smaller local path is chosen. |
| Non-required variation appears | Continue only by recording follow-up. | Optional breadth should not expand the active slice. | Required acceptance remains covered; optional variation is outside the active diff. |
| Ordinary implementation technique is uncertain but slice is clear | Continue. | The agent owns internal technique inside the bounded slice. | No user input needed unless the uncertainty changes commitment, proof, or scope. |

## 8. Ownership And Pointer Decisions

| Item | Runtime Skill | Support Doc | Research Only | Owned Elsewhere | Why |
| --- | --- | --- | --- | --- | --- |
| `bounded slice` | Yes | Light | No | No | Core runtime frame for this facet. |
| `tracer bullet` | Yes | Light | No | No | Strongest runtime word for one real path, if paired with production-shaped proof. |
| `support slice` | Yes | Yes | No | No | Needed runtime escape hatch; taxonomy belongs in support. |
| `one self-contained change` | Yes | Light | No | Facet 8 also uses reviewability | Runtime uses it as a slice gate, not a final review procedure. |
| `one concept` | Yes | Light | No | No | Crisp stop/split signal. |
| `file spread` | Yes | Light | No | No | Runtime warning, not numeric policy. |
| Success criteria / proof target | Yes | Light | No | Facet 3 owns deep intake | Facet 1 needs a pass/fail target but does not author the issue. |
| Lock proof before editing | Yes | No | No | Facet 2 owns baseline before editing | This is a scope lock, not dirty-work/fixed-point capture. |
| One real path over breadth | Yes | Yes | No | Facet 6 owns seam depth | This facet chooses narrowness; Facet 6 chooses correctness-critical seam detail. |
| Reduce variation | Yes | Light | No | No | Direct guard against optional breadth. |
| Related proof travels with diff | Yes | Light | No | Facet 5 / `$tdd` own proof mechanics | Runtime says proof must attach; later facets define how. |
| Classify failed proof before fixing | Yes | Light | No | Facet 5 / Facet 8 own skipped-check reporting | This facet controls scope expansion after feedback. |
| Broad refactor split rule | Yes | Light | No | Facet 7 owns protected simplification | Runtime keeps refactors from widening; later facet handles cleanup. |
| TDD/red-green mechanics | No | Pointer only | No | `$tdd`, Facet 5 | This flow can invoke or hand off; it should not duplicate. |
| Baseline/fixed point/dirty work/commit isolation | No | Pointer only | No | Facet 2 | Orthogonal trust boundary before editing. |
| Commitment changes | No | Pointer only | No | Facet 4, engineering contract | User-owned decisions need a separate authority model. |
| Load-bearing internals/seam depth | No | Pointer only | No | Facet 6, `codebase-design` | This flow should not become design theory. |
| Implementation note, residual risk, issue state, commit readiness | No | Pointer only | No | Facet 8, `$review` | Closing and locking behavior belongs later. |
| Story mapping/backlog/product workshop process | No | No | Yes | `to-prd`, `to-tickets` if needed | Useful source pressure, not implement runtime. |
| Small-batch economics and speed claims | No | Maybe | Yes | No | Keep as caution against overclaiming. |
| Google CL stacking/approval bits | No | No | Yes | Repo review docs if ever needed | Source-specific process is not portable runtime behavior. |
| Agent benchmarks/framework terms | No | No | Yes | No | No direct behavior after translation. |
| Multi-agent/offload controls | No | Yes | No | Delegation support docs | Useful only when helper agents are used. |

## 9. Agent Bridge Risks

| Risk | Why It Matters | Mitigation |
| --- | --- | --- |
| Sequence absorbs all of `implement` | Bounded slice could expand into context intake, proof, review, and commit behavior. | Keep Facet 1 to slice lock, scope pressure, proof-boundary classification, and stop/split rules. |
| Duplicates the engineering contract | The repo contract owns commitment authority and broad engineering discipline. | Mention only when boundedness changes; point commitment decisions to Facet 4 and the contract. |
| Duplicates `$tdd` or Semantic Proof | Proof target language can drift into test procedure. | Keep proof as a boundary and handoff; leave red-green mechanics and proof modes to `$tdd` and Facet 5. |
| Duplicates `$review` or Review And Lock | "Reviewable" can become final review instructions. | Runtime keeps one concept plus proof; later facets own fixed-point review and lock. |
| Duplicates `triage` / `to-tickets` | Missing proof target could turn into issue-authoring workflow. | Stop or propose a narrower slice; do not author the whole issue inside this facet. |
| Walking skeleton becomes architecture theater | It is valuable only when the proof path is uncertain. | Keep as support-only and require approval before architecture/dependency/tooling/public-contract/data/security/privacy changes. |
| File spread becomes numeric policy | File counts can be misleading. | Treat spread as evidence to re-bound and justify, not as a hard threshold. |
| Failed proof broadens scope | Agents often chase whatever a tool reports. | Require classification before fixing and fix only in-slice failures. |
| Support slice becomes a loophole | Technical work can hide behind support language. | Require unblocker/de-risking purpose plus concrete validation. |
| Final runtime wording becomes too dense | Too many leading words can make the skill hard to execute. | Put taxonomy, source nuance, and caution tables in support; keep runtime to leading words and gates. |

## 10. Handoff To Full Behavior Synthesis

Final behavior sequence:

1. Lock the slice before editing.
2. Localize enough to avoid wandering.
3. Implement one real path or honest support slice.
4. Keep scope pressure during the diff.
5. Classify proof feedback before fixing.
6. Finish the slice as self-contained and hand off to later proof/review/commit
   facets.

Strongest leading words:

- `bounded slice`
- `tracer bullet`
- `support slice`
- `one self-contained change`
- `one concept`
- `file spread`
- `success criteria` / proof target

Strongest gates:

- The slice is one behavior/support proof, not just an issue title.
- The first path produces meaningful feedback for the selected slice.
- Support work names its unblocker/de-risking purpose and validation.
- The diff remains one concept plus one proof story.
- Related proof travels with the diff.
- Every touched area has an in-scope reason.
- Failed proof is classified before fixing.

Support/reference pointers needed:

- Support-slice taxonomy.
- Conditional walking-skeleton note.
- Weak/no-op phrase table.
- Boundary matrix against Facets 2-8, `$tdd`, `$review`, and repo engineering
  contract.
- Bounded offload note for multi-agent runs.

Unresolved design questions:

- Whether `tracer bullet` should appear inline in runtime wording or be
  translated to "one real path" with `tracer bullet` in support.
- Whether support-slice taxonomy deserves a dedicated support file or a short
  subsection in a broader `implement` reference.
- How much file-spread language belongs inline without becoming a file-count
  policy.
- How to phrase "highest useful proof path" without duplicating Facet 5 proof
  mechanics or Facet 6 seam-depth guidance.

Ownership conflicts to watch:

- Facet 2 owns baseline/fixed-point trust before editing.
- Facet 3 owns deep context intake and acceptance-readiness checks.
- Facet 4 owns user commitment boundaries.
- Facet 5 and `$tdd` own proof modes and red-green mechanics.
- Facet 6 and `codebase-design` own load-bearing internals and seam depth.
- Facet 7 owns protected simplification.
- Facet 8 and `$review` own fixed-point review, implementation notes, residual
  risk, and commit readiness.

Prompt 07 should explain in prose:

- why the sequence prevents scope creep without making the agent timid;
- the difference between a behavior slice and a support slice;
- why failed proof is classified before fixing;
- how one concept plus one proof story is the completion pressure;
- where walking skeleton, support taxonomy, and offload guidance should live;
- why this facet intentionally stops before full TDD, review, simplification,
  and commit procedure.
