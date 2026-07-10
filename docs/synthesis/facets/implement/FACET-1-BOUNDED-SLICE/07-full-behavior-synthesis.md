# Facet 1: Bounded Slice Full Behavior Synthesis

This executes
[`docs/synthesis/methods/prompts/07-full-behavior-synthesis.md`](../../../methods/prompts/07-full-behavior-synthesis.md)
for `implement` Facet 1.

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

Behavior flow:
[`06-agent-bridge.md`](06-agent-bridge.md)

Relevant research packets:

- Source search:
  [`docs/research/skill-facets/implement/FACET-1-BOUNDED-SLICE-sources.md`](../../../../research/skill-facets/implement/FACET-1-BOUNDED-SLICE-sources.md)
- Source extraction:
  [`docs/research/skill-facets/implement/FACET-1-BOUNDED-SLICE-extraction.md`](../../../../research/skill-facets/implement/FACET-1-BOUNDED-SLICE-extraction.md)
- Source triage:
  [`docs/research/skill-facets/implement/FACET-1-BOUNDED-SLICE-triage.md`](../../../../research/skill-facets/implement/FACET-1-BOUNDED-SLICE-triage.md)

## 1. Purpose

This facet should make `$implement` predictable when a selected issue starts to
look larger than one independently provable change. It matters after issue
selection and before or during editing: the agent has enough context to act, but
must keep the run from becoming a project bucket.

Average-agent behavior to prevent:

- implementing from an issue title without naming the proof target;
- searching or editing broadly because the repo has nearby interesting work;
- treating a layer, component, refactor, doc, config, or harness change as if it
  were a complete behavior slice;
- adding adjacent variants because they are easy to see;
- fixing every failing check or nearby defect discovered by tooling;
- finishing with code that is hard to explain as one concept with one proof
  story.

Upper-bound engineering taste to recruit:

- a `tracer bullet` is a real narrow path that teaches through production-shaped
  feedback, not a throwaway spike;
- a `support slice` is honest about what it unblocks or de-risks;
- a self-contained change carries its proof and rationale with the diff;
- scope is controlled by proof, reviewability, feedback, and recovery rather
  than by LOC, speed folklore, or ceremony;
- agent autonomy is strongest inside a locked slice and weakest when scope,
  commitments, or proof boundaries change.

This facet does not own the whole `implement` loop. It should not author issues,
perform baseline capture, define the full proof method, choose deep-module seam
strategy, run protected simplification, perform fixed-point review, write the
implementation note, or decide commit behavior. Its job is to keep the selected
work as one bounded behavior/support proof and to hand off cleanly when later
facets own the next gate.

## 2. Source Pressure

| Source / Prior | Pressure It Adds | Behavior It Supports | Runtime Or Support? |
| --- | --- | --- | --- |
| *The Pragmatic Programmer* tracer bullets | Use one real path to get feedback under real conditions; distinguish tracer from throwaway prototype. | Prefer one production-shaped path and remove or productionize scratch work. | Runtime with support caveat. |
| Google Engineering Practices, Small CLs | Make one self-contained change; keep related test/proof and context together; split broad refactors. | One concept plus proof story; broad-refactor split rule; related proof travels with diff. | Runtime. |
| Humanizing Work story splitting | Slice by value path or workflow, not by component; classify support work honestly; avoid variation creep. | Behavior slice versus support slice; required variation only; component masquerade guard. | Runtime plus support taxonomy. |
| Ram et al. reviewability | Reviewable changes are coherent, self-contained, and understandable, not merely small. | Completion pressure that a cold reader can understand the change as one concept. | Runtime gate, deeper review elsewhere. |
| GOOS walking skeleton | Use a minimal executable path when system shape or feedback path is uncertain. | Conditional walking-skeleton branch, not routine implementation advice. | Support with narrow runtime pointer. |
| Patton story mapping / thin slices | Ground slices in user/caller/operator activity rather than folder or layer boundaries. | Name the path or activity before editing. | Support pressure translated into runtime action. |
| DORA / Continuous Delivery small batches | Smaller independent units improve feedback, recovery, and learning, but not as a magic speed claim. | Keep the run independently validatable; avoid speed/productivity overclaims. | Research/support caution. |
| SWE@Google code review | Review is about correctness, comprehension, and maintainability at human scale. | Keep purpose, changed areas, and proof understandable without importing review procedure. | Support; final review elsewhere. |
| OpenAI Codex and GitHub coding-agent docs | Coding agents work best with focused tasks, concrete success criteria, and validation. | Lock proof target, non-goals, likely files/seam, and stop conditions before editing. | Runtime bridge. |
| di Biase change decomposition | Separate different concepts; mixed changes add review noise. | Stop, split, ask, or follow up when a second independent concept appears. | Runtime. |
| Kudrjavets small-change contrast | Do not claim small changes automatically merge faster. | Justify boundedness by proof, feedback, reviewability, and recovery. | Research-only caution. |
| Bosu useful reviews | File count/spread affects review usefulness beyond line count. | Treat file spread as scope evidence, not a numeric threshold. | Runtime. |
| Pascarella information needs | Reviewers need rationale, context, splittability, and necessity information. | Support final cold-understandability pressure; detailed note belongs to Facet 8. | Support / elsewhere. |
| Anthropic effective agents | Clear criteria and human oversight matter when autonomy crosses unclear boundaries. | Ask only at real commitment/proof/scope boundaries. | Runtime bridge. |
| Agentless / SWE-agent | Simple localize, repair, validate loops and tool feedback beat unconstrained autonomy. | Localize enough, edit narrowly, classify proof feedback before fixing. | Runtime bridge, no framework jargon. |

## 3. Chosen Behavior

The agent first locks the slice before editing. The lock is not a plan essay; it
is the minimum proof boundary: selected behavior path or support purpose, proof
target, non-goals, likely touched area or seam, and validation target. If the
work is not user-visible behavior, the agent calls it a `support slice` and
names what it unblocks or de-risks.

The agent then localizes only enough to make the edit surface concrete. The
search/read phase exists to find the relevant caller/operator path, support
surface, or seam for the locked proof. Exploration that spreads across unrelated
areas is not "being thorough"; it is a signal to re-bound, split, or ask.

Implementation should favor one real path over breadth. For behavior work, that
means a production-shaped `tracer bullet`: the smallest meaningful path that can
produce feedback for a required case. For support work, it means the smallest
change that proves the unblocker or de-risking purpose. Scratch or spike work is
not implementation unless it is productionized and proved.

During the diff, the agent watches for scope pressure. `File spread`, optional
variants, broad refactors, and second concepts are not automatically wrong, but
they need justification against the locked proof. Required coupled edits may
stay. Independent concepts, optional variants, and broad cleanup should become a
split, ask, or follow-up.

When proof fails, the agent classifies the failure before fixing it. A failure
can be `in-slice`, `adjacent`, `changed commitment`, or `environment/tooling`.
Only in-slice failures are fixed inside the active diff. Adjacent work becomes a
follow-up or new slice; changed commitments require user approval; environment
or tooling failures are reported through later proof/review behavior.

The handoff is one self-contained change: one concept plus one proof story. The
facet is done only when code, rationale, and proof travel together well enough
that later Semantic Proof, Protected Simplification, Review And Lock, and commit
steps can operate without rediscovering the boundary.

## 4. Leading Words

| Leading Word | Why It Recruits Useful Priors | Behavior It Anchors | Risk If Misused |
| --- | --- | --- | --- |
| `bounded slice` | Names a contained unit of implementation rather than a project bucket. | Keep one selected issue as one behavior/support proof. | Becomes a slogan if not tied to proof, non-goals, and stop rules. |
| `tracer bullet` | Recruits the idea of one real path that produces feedback under actual conditions. | Prefer a production-shaped path over feature breadth. | Can excuse incomplete or throwaway code if prototype distinction is lost. |
| `support slice` | Makes non-behavior work honest without rejecting it. | Name the unblocker/de-risking purpose and validation for docs/config/tests/refactors/harnesses. | Can become a loophole for technical drift without proof. |
| `one self-contained change` | Pulls code, proof, and rationale into one reviewable unit. | Finish with proof and context attached to the diff. | Can over-split legitimately coupled edits. |
| `one concept` | Gives a compact split test for adjacent work. | Stop, split, ask, or follow up when the diff becomes a bag of fixes. | Can be applied mechanically when edits are coupled by one behavior. |
| `file spread` | Recruits review burden beyond LOC. | Treat touched-area breadth as a scope warning. | Can become a file-count policy. |
| `success criteria` / proof target | Keeps done pass/fail instead of vibes-based. | Name what the slice must prove before editing. | Can drift into full issue-authoring work owned by other facets. |

## 5. Agent Execution Surface

| Execution Surface | Agent Action | Evidence Gate | Failure Prevented |
| --- | --- | --- | --- |
| read | Read the selected issue/spec enough to name proof target, non-goals, likely touched area, and required acceptance. | Slice can be stated as one behavior/support proof. | Issue-title implementation. |
| search | Search only enough to localize the relevant caller/operator path, support surface, or seam. | Search result explains why the touched area belongs to the proof. | Broad wandering. |
| inspect | Inspect the emerging diff for concepts, variants, refactor spread, and touched-area spread. | Every touched area has an in-scope reason. | File-spread blind spot and composite changes. |
| edit | Make the smallest production-shaped behavior/support change that proves the locked slice. | Diff advances one concept with one proof story. | Horizontal slices, component masquerade, prototype drift. |
| test / validate | Run or prepare the focused proof that would fail if the slice promise were wrong. | Related proof travels with the diff or is explicitly recorded as blocked by later proof rules. | Validation theater and code-only completion. |
| stop | Stop broadening when a second concept, optional variant, broad refactor, or out-of-slice proof failure appears. | Active work returns to one concept or a new slice is approved. | Scope creep disguised as diligence. |
| ask | Ask only when proof, scope, acceptance, or user-owned commitments are unclear or changing. | User resolves the commitment or approves a narrower/broader slice. | Timid over-asking and unauthorized commitment changes. |
| delegate | If helpers are used, assign narrow questions and integrate only bounded evidence. | Helper output answers the assigned question without creating new scope. | Multi-agent sprawl. |
| report | Hand off adjacent findings, skipped proof, or blockers to later facets instead of absorbing them. | Final result can still be described as one concept plus one proof story. | Unrelated repairs and hidden residual risk. |

## 6. Evidence Gates

| Gate | Why It Matters | Too Weak If | Too Heavy If | Candidate Consequence Shape |
| --- | --- | --- | --- | --- |
| Slice lock | Prevents editing before the agent knows what it is proving. | It names only the issue title. | It becomes PRD/story-map/readiness authoring. | "Before editing, name the behavior/support proof, non-goals, likely area, and validation target." |
| Pass/fail success criteria | Makes done knowable. | It says "works", "improve", or "add tests". | It demands all future variants. | "If you cannot say what would prove this slice, narrow or ask." |
| One real path or support purpose | Prevents layer-only work from pretending to be done. | A component change claims behavior without a caller/operator path or support proof. | Routine issues require walking skeletons. | "Behavior slices name the path; support slices name the unblocker and proof." |
| One concept plus one proof story | Keeps the diff independently reviewable and provable. | The summary is a list of unrelated fixes. | Coupled edits required by one behavior are split apart. | "If the diff is a bag of concepts, split or follow up." |
| Related proof travels with diff | Prevents detached validation. | It says tests exist somewhere. | It pulls in unrelated test cleanup. | "The proof should be next to this change and would fail if this promise were wrong." |
| Highest useful proof path | Avoids both syntax-only checks and unnecessary end-to-end ceremony. | It checks only output existence for semantic behavior. | It requires slow infrastructure when a smaller seam proves the slice. | "Use the smallest meaningful proof that exercises the selected boundary." |
| Variation boundary | Prevents optional breadth from joining the slice. | Adjacent variants are silently added. | Required acceptance cases are deferred. | "Required variants stay; optional variants become follow-up." |
| File-spread justification | Makes physical spread visible as scope pressure. | It counts only LOC or ignores touched areas. | It blocks necessary cross-file work. | "Every touched area needs an in-scope reason." |
| Refactor boundary | Prevents cleanup from tangling with behavior. | It says "refactor as needed". | It blocks tiny enabling cleanup required for proof. | "Refactor only if tiny, local, required, and protected; otherwise split." |
| Proof-failure classification | Stops tooling from expanding the mission. | The agent fixes unrelated failures. | The agent stops on every in-slice failure. | "Classify failures before fixing: in-slice, adjacent, changed commitment, environment/tooling." |

## 7. Stop / Ask / Continue Logic

| Situation | Agent Should | Why | Resume / Continue When |
| --- | --- | --- | --- |
| Cannot state one behavior/support proof. | Ask or propose a narrower slice. | The work is still a project bucket. | Proof target, non-goals, likely area, and validation target are concrete. |
| Success criteria are ambiguous. | Ask or narrow. | Done cannot be proved. | There is a pass/fail outcome to run or inspect. |
| Ordinary technique is uncertain but the slice is clear. | Continue. | Technique belongs to the agent inside the locked slice. | No user input needed unless scope, proof, or commitment changes. |
| Search/exploration spreads beyond the expected area. | Re-bound before continuing. | Exploration spread is early evidence of scope drift. | The touched/search area ties back to the locked proof. |
| A second independent concept appears. | Split, ask, or record follow-up. | The active diff is no longer one concept. | Active work returns to one concept or broader scope is approved. |
| Non-required variation appears. | Record follow-up and continue on required cases. | Optional breadth should not expand the run. | Required acceptance remains covered. |
| Broad refactor is needed. | Ask or split unless it is tiny, local, required, and protected. | Cleanup can obscure behavior correctness. | Refactor is approved, separated, or proven necessary for the slice. |
| Proof fails inside the locked slice. | Fix and re-prove. | This is normal implementation feedback. | The proof passes or reveals a different classification. |
| Proof failure points outside the slice. | Stop widening and classify. | Tool feedback should not silently change the mission. | Failure is in-scope, a new slice is approved, or it is recorded as adjacent/blocking. |
| Walking skeleton would alter architecture, dependency, tooling, public contract, data, security, or privacy semantics. | Ask. | This crosses a commitment boundary. | User approves or a smaller local path is chosen. |
| Support work lacks an unblocker/de-risking purpose. | Ask or narrow. | Support work without a proof purpose is drift. | Purpose and validation are explicit. |
| Helper agents produce adjacent opportunities. | Integrate only assigned evidence; record the rest. | Parallelism should not widen the slice. | Adjacent opportunity becomes an approved slice. |

## 8. Runtime vs Support Placement

| Material | Runtime / Support / Research / Elsewhere | Why |
| --- | --- | --- |
| Slice lock before editing | Runtime | Every run needs this boundary to avoid wandering. |
| `bounded slice` | Runtime | Central leading word for the facet. |
| `tracer bullet` | Runtime or short support-backed pointer | Useful leading word, but final wording must guard against prototype drift. |
| `support slice` | Runtime plus support | Runtime needs the distinction; support can hold taxonomy and examples. |
| One real path over breadth | Runtime | Directly changes implementation behavior. |
| One concept plus one proof story | Runtime | Strong completion pressure and split test. |
| File spread as scope evidence | Runtime | Mid-run warning that broad touched areas need justification. |
| Proof-failure classification | Runtime | Prevents failed checks from changing scope. |
| Conditional walking skeleton | Support with tiny runtime pointer | Important branch, too nuanced for default inline procedure. |
| Support-slice taxonomy | Support | Helpful only when classifying non-behavior work. |
| Weak/no-op phrase table | Support or research | Useful for Prompt 08 pruning, not runtime behavior. |
| Small-batch economics | Research/support caution | Explains rationale; runtime should not teach delivery theory. |
| Speed/merge-time claims | Research-only rejection | The selected evidence cautions against this claim. |
| TDD and proof mechanics | Elsewhere | `$tdd` and Facet 5 own this. |
| Baseline and fixed point | Elsewhere | Facet 2 owns dirty-work preservation and review start. |
| Commitment authority | Elsewhere | Facet 4 and repo engineering contract own user-vs-agent decisions. |
| Seam depth / load-bearing internals | Elsewhere | Facet 6 and `codebase-design` own this. |
| Protected simplification | Elsewhere | Facet 7 owns simplification after proof. |
| Review, implementation note, residual risk, commit | Elsewhere | Facet 8 and `$review` own closing behavior. |
| Multi-agent offload controls | Support | Only relevant when delegation happens. |

## 9. Rejected Or Deferred Options

| Option | Reject / Defer | Why | Revive Only If |
| --- | --- | --- | --- |
| "Keep it small" as runtime wording | Reject | Too vague and size-only. | It becomes one concept plus related proof and in-scope touched areas. |
| Raw "vertical slice" wording | Defer/translate | Product slogan risk; can import story-mapping baggage. | It names a caller/operator path and proof without product ceremony. |
| Mandatory walking skeleton | Reject | Too heavy for routine implementation. | System shape or feedback path is genuinely uncertain. |
| Full story mapping or backlog planning | Reject | Upstream product/issue creation work. | The skill scope expands beyond one ready issue. |
| Full TDD procedure | Defer elsewhere | `$tdd` and Facet 5 own red-green-refactor and proof modes. | Prompt 05 for Semantic Proof decides invocation wording. |
| Full fixed-point review procedure | Defer elsewhere | `$review` and Facet 8 own review/lock. | Later synthesis needs a pointer. |
| Hard LOC/file-count thresholds | Reject | Numeric policy misses cross-cutting necessity and hidden complexity. | Repo-specific policy explicitly requires it. |
| Ask whenever scope feels uncertain | Reject | Creates timid over-asking inside normal implementation technique. | Uncertainty changes commitment, proof target, or slice boundary. |
| Require approval for any file spread | Reject | File spread is evidence to justify, not a numeric or approval policy. | Spread reveals a second concept or changed commitment. |
| Ask before every refactor | Reject | Tiny, local, required, protected refactors belong inside the slice. | Refactor becomes broad or independently valuable. |
| Automatically fix every failed check | Reject | Failed proof must be classified before fixing. | Failure is proven in-slice. |
| Split every coupled edit mechanically | Reject | Legitimately coupled edits may be required for one proof story. | The edit introduces an independent concept. |
| "Small changes merge faster" rationale | Reject | Evidence does not support using this as a general claim. | New source support is added and triaged. |
| Refactor-as-you-go doctrine | Reject | Encourages cleanup drift. | Refactor is tiny, local, required, and protected by this slice. |
| Broad helper-agent workflow | Defer support | Delegation is conditional and can cause sprawl. | User or runtime explicitly asks for helpers. |
| ACI / benchmark / framework vocabulary | Reject | Does not improve runtime execution. | Translated into plain search/edit/prove/stop action. |

## 10. Design Questions

| Question | Why It Matters | Suggested Resolution |
| --- | --- | --- |
| Should `tracer bullet` survive inline? | It is strong but can be misread as incomplete or throwaway. | Keep the term if paired with "real production-shaped path"; otherwise translate to "one real path" and put the term in support. |
| Where should support-slice taxonomy live? | Runtime needs the distinction, but examples can bloat the skill. | Use one runtime sentence plus a context pointer to support taxonomy if later prompts create support docs. |
| How much file-spread language belongs inline? | It is useful pressure but can become numeric policy. | Keep "file spread is scope evidence" plus "justify touched areas"; avoid counts. |
| How should highest useful proof be phrased? | It overlaps Facets 5 and 6. | Say only that the proof must exercise the selected boundary; leave proof mechanics and seam theory elsewhere. |
| Should walking skeleton be named at runtime? | It helps uncertain new paths but tempts architecture work. | Mention only under an uncertainty branch or support pointer, with commitment-boundary ask rules. |
| How should Prompt 08 avoid over-asking? | Strong stop rules can make the agent timid. | Keep one explicit continue rule: ordinary technique belongs to the agent when the slice is clear. |

## 11. Verbose Draft Notes

The agent should think of the selected issue as a bounded slice: one
behavior/support proof that can be implemented, proved, and explained without
absorbing adjacent work. Before editing, it should name the path or support
purpose, what proof will show, what is out of scope, and where it expects to
work. This is a lightweight lock, not a planning ceremony.

For behavior work, the agent should look for a tracer bullet: one real path
through the system that can produce meaningful feedback for the selected case.
The path should be production-shaped and proved through the highest useful
boundary available. It should not become a fake prototype, broken middle, or
layer-only claim.

For support work, the agent should stop pretending it is a user-facing behavior
slice. A support slice is legitimate when it names what it unblocks or de-risks
and has observable validation. Docs, config, test harnesses, refactors, and
fixtures can all be implementation work when they have this proof boundary.

While editing, the agent should keep asking whether the diff is still one
concept plus one proof story. File spread, new variants, broad cleanup, and
second concepts are signals, not automatic failures. The right response is to
justify them against the locked proof, split them out, ask when the commitment
changes, or record a follow-up.

When checks fail, the agent should not blindly repair everything the tools show.
It should classify the feedback. In-slice failures are normal and should be
fixed. Adjacent defects, changed commitments, and environment/tooling blockers
should not quietly widen the implementation.

The facet's completion pressure is self-containment. The slice is ready for
later proof, simplification, review, and lock only when code, rationale, and
proof travel together as one concept. If that is not true, the agent should
narrow, split, ask, or hand off the unresolved risk instead of declaring the
slice done.

## 12. Compression Handoff

Chosen behavior:

- Lock one behavior/support proof before editing.
- Localize enough to find the relevant path or support surface.
- Implement one production-shaped path or honest support slice.
- Keep scope pressure active during the diff.
- Classify failed proof before fixing.
- Finish as one self-contained change and hand off to later facets.

Strongest leading words:

- `bounded slice`
- `tracer bullet`
- `support slice`
- `one self-contained change`
- `one concept`
- `file spread`
- `success criteria` / proof target

Candidate runtime wording fragments:

- "Before editing, lock the bounded slice: behavior/support proof, non-goals,
  likely area, and validation target."
- "For behavior work, prefer one real production-shaped path before breadth."
- "For support work, name the unblocker or de-risking purpose and its proof."
- "Keep the diff to one concept plus one proof story."
- "Treat file spread as scope evidence; justify touched areas against the
  locked proof."
- "Classify failed proof before fixing: in-slice, adjacent, changed commitment,
  or environment/tooling."
- "Continue on ordinary technique inside the slice; ask when proof, scope, or
  commitments change."

Blunt gates:

- No proof target, no editing.
- No support purpose, no support slice.
- No one-concept summary, split or ask.
- No in-scope reason for a touched area, re-bound.
- No proof tied to the diff, no completion.

Support/reference pointers needed:

- support-slice taxonomy;
- conditional walking-skeleton guidance;
- weak/no-op phrase table for pruning;
- boundary matrix against Facets 2-8, `$tdd`, `$review`, and the engineering
  contract;
- bounded offload note for multi-agent runs.

What stays research-only:

- story-mapping workshops and backlog procedure;
- delivery-economics theory beyond anti-overclaim caution;
- Google CL process details;
- empirical paper detail beyond behavior pressure;
- agent-framework and benchmark vocabulary;
- hard size thresholds and speed claims.

Validation tasks to remember:

- Check Prompt 08 output against the no-op phrases in triage.
- Ensure final compact language does not duplicate `$tdd`, `$review`, Facet 2,
  Facet 4, Facet 6, Facet 7, or Facet 8.
- Ensure the final wording has at least one explicit continue rule so the agent
  does not ask about ordinary implementation technique.
- Ensure every runtime gate is checkable.

Biggest compression risk:

- Compressing this into "keep it small" or "do a vertical slice" would erase the
  useful behavior. The compact pass must preserve proof target, support-slice
  honesty, one concept plus proof story, file-spread scope pressure, and failure
  classification.
