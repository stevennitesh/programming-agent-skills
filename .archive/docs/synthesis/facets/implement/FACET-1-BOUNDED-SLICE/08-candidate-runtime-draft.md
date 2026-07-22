# Facet 1: Bounded Slice Compact Draft

Historical source-to-skill Prompt 08 artifact for `implement` Facet 1, using
the latest Prompt 09 revision feedback recorded at the time.

## Prompt Inputs

Skill: `implement`

Skill path: `skills/custom/implement/SKILL.md`

Facet or scope: `1. Bounded Slice`

Generous synthesis:
[`07-full-behavior-synthesis.md`](07-full-behavior-synthesis.md)

Behavior flow:
[`06-agent-bridge.md`](06-agent-bridge.md)

Existing skill text to preserve: `skills/custom/implement/SKILL.md`,
especially issue selection, baseline capture, context intake, `.tmp/`
exploration and cleanup, TDD/proof handoff, simplification, fixed-point review,
commit, and implementation-note behavior.

Revision feedback: Prompt 09 audit decision was `revise-before-validation`.
Use the audit-approved line set. Revise only B1, B2/B5, P5, and F3c before
validation so scratch/probe discovery does not duplicate generic cleanup or
block Explore, completion wording stays local to the step, and adjacent/tooling
proof-feedback routing uses the existing commitment-boundary owner.

## 1. Compact Draft Scope

This draft compacts Facet 1, `Bounded Slice`, into revised candidate runtime
wording for the existing `implement` skill.

Synthesis input used:

- Prompt 06 agent bridge;
- Prompt 07 full behavior synthesis;
- Prompt 09 detailed skill-context draft revision feedback;
- existing `skills/custom/implement/SKILL.md`;
- `docs/agents/engineering-contract.md` as an ownership check.

Existing skill behavior that must be preserved:

- select one ready issue and stop after one issue;
- capture baseline before editing;
- read issue/spec/acceptance context;
- keep read-only discovery, `.tmp/` spikes, copied references, experiments,
  rough notes, throwaway repros, and tiny reversible seam probes available
  during `Orient And Explore`;
- delete scratch artifacts before final delivery unless the user asks to
  preserve them;
- use `$tdd` where practical;
- prove semantic correctness through the best available seam;
- simplify only while behavior is protected;
- run `$review` from the starting ref;
- commit and leave an implementation note.

This draft must make one behavior predictable: after one issue is selected, the
agent keeps implementation as one bounded behavior/support proof instead of
absorbing adjacent work.

This draft must not decide final runtime text, edit `SKILL.md`, add support
docs, change invocation policy, define full proof mechanics, define baseline
mechanics, or duplicate later facets.

## 2. Compression Principles

Strong leading words to preserve:

- `bounded slice`
- `tracer bullet`
- `support slice`
- `one concept`
- `one proof story`
- `file spread`
- `proof target`

Explanatory prose cut:

- source rationale for small batches, reviewability, and story splitting;
- product-slicing history;
- empirical-study detail;
- agent-framework vocabulary;
- why each later facet owns its own procedure.

Belongs behind context pointers only if later validation proves the need:

- support-slice taxonomy;
- conditional walking-skeleton guidance;
- bounded helper-agent/offload guidance;
- ownership-boundary examples.

Blunt gates needed:

- No checkable proof target, no selected-slice implementation edit.
- No support purpose and validation, no support slice.
- No named discovery/evidence target, no unknown edit surface.
- No remaining changed file/module/artifact without an in-scope reason.
- No named proof/acceptance/affected-proof-surface coupling, no required
  coupled edit.
- No focused-check classification, no widening.

Research-only material:

- story-mapping workshops;
- delivery-economics theory;
- Google CL process details;
- hard LOC/file thresholds;
- speed/merge-time claims;
- ACI, benchmark, and framework terminology.

## 3. Candidate Invocation / Description Wording

No invocation wording change proposed.

The current description already invokes `implement` for one ready-for-agent
issue through implementation, verification, review, commit, and note. Facet 1
changes runtime behavior after invocation, not trigger matching.

Risk to audit: if later facets broaden `implement` invocation, this no-change
decision should be rechecked at whole-skill integration.

## 4. Candidate Runtime Steps

### Bound The Slice

Use inspection, read-only discovery, scratch work, and tiny reversible Explore
probes to resolve slice-lock or proof uncertainty, including which seam and
evidence will prove the slice. Keep scratch disposable under the existing
scratch cleanup rule unless it is promoted with a named in-scope proof reason.

Before edits intended to implement the selected slice, lock the bounded slice:
behavior path or support purpose, checkable proof target, non-goals, expected
edit surface, and focused check or evidence target. If the edit surface is
unknown, name the exact discovery question or evidence action, then use
read-only discovery or a tiny reversible Explore probe only to find the real
seam; update the lock before selected-slice implementation edits.

For support work, name the exact unblocker or risk and the validation signal
that proves it. No support purpose and validation, no support slice.

If the proof target is not checkable, narrow or ask before selected-slice
implementation edits.

Done when the slice lock is complete, including a checkable proof target and
expected edit surface; a discovery question does not count as a completed lock
until the lock is updated.

### Implement One Path

For behavior work, implement one real production-shaped tracer-bullet path
before breadth unless acceptance criteria or proof needs require breadth.

For support work, change only what is needed to prove the named unblocker or
risk; move optional cleanup to follow-up.

Inside the locked slice, choose the tools, local implementation route, and
sequencing of edits and checks without asking.

If that choice would change the locked slice, proof target, acceptance, or
another user-owned commitment, stop and apply the existing commitment-boundary
rule.

The active diff remains in scope only while it can be summarized as one concept
tied to one proof story; if it cannot, narrow, split, record a follow-up, or ask
before continuing.

### Keep Scope Pressure

When file spread, optional variants, broad refactors, or a second concept
appears, re-check the active implementation diff and each remaining changed
file/module/artifact against the locked slice's proof target and proof story.
Do not count disposable scratch discovery as implementation spread while it
remains throwaway; before delivery, delete scratch or promote it only with a
named in-scope proof reason.

No remaining changed file/module/artifact without an in-scope reason tied to
the proof target, proof story, acceptance criteria, or a required coupled edit.

A required coupled edit is a change needed to preserve the named proof target,
satisfy a named acceptance criterion, or keep a named affected check, command,
generated artifact, or build path valid for this slice. Keep it only when that
coupling is named; otherwise split it, record a follow-up, or ask.

Refactor only when protected, behavior-preserving, in-scope, and needed to
preserve or prove this slice's proof target. Refactors that are merely
generally cleaner or more maintainable are outside this slice; split, record a
follow-up, or ask. Leave refactor procedure to protected
simplification and `$tdd`.

Done when every remaining changed file/module/artifact has an in-scope reason
and the active diff remains one concept with one proof story.

### Classify Proof Feedback

When a focused check fails during implementation, classify it before widening
the diff: `in-slice`, `adjacent`, `changed commitment`, or
`environment/tooling`.

Fix and rerun `in-slice` failures inside the current slice.

For `changed commitment` focused-check failures, stop and apply the existing
commitment-boundary rule.

For `adjacent` or `environment/tooling` focused-check failures, choose one
branch before widening:

- If the locked slice cannot be proven without the fix, and the fix does not
  change a commitment covered by the commitment-boundary rule: make the smallest
  local fix needed to unblock that proof, then rerun the focused check.
- If the locked slice cannot be proven without the fix, but the fix would change
  a commitment covered by the commitment-boundary rule: stop and apply that
  rule.
- If the locked slice can still be proven without the fix: do not fix it in this
  slice; split it, record a follow-up, ask, or report the blocker.

Do not use this mid-run classification for fixed-point review findings;
`Converge` owns those.

Done when any failed focused check that would widen, redirect, or exit the
slice has an explicit outcome: `fix-in-slice`, commitment-boundary, split,
follow-up, ask, or blocker.

## 5. Candidate Rules / Gates

| Candidate Line | Purpose | Failure Prevented |
| --- | --- | --- |
| No checkable proof target, no edit intended to complete the selected slice. | Preserve discovery and tiny Explore probes while blocking production implementation before a proof boundary exists. | Issue-title implementation and premature production edits. |
| Scratch/read-only discovery can answer slice-lock or proof uncertainty, but it does not complete the lock by itself. | Preserve useful discovery without turning scratch into implementation permission. | Scratch as scope drift or premature scratch bans. |
| Unknown edit surface allows only named read-only discovery or a tiny reversible Explore probe to find the real seam; update the lock before selected-slice implementation edits. | Preserve the engineering-contract Explore exception without weakening the lock. | Blocking legitimate seam probes, or using probes as implementation. |
| Bound The Slice is complete only when the lock is checkable, the expected edit surface is known, and any discovery/probe used to find it has been folded back into the lock. | Avoid restating the full lock while preventing discovery from substituting for a completed lock. | Treating a discovery question as a finished slice lock. |
| No support purpose and validation, no support slice. | Keep docs/config/tests/refactors/harness work honest. | Technical drift disguised as implementation. |
| One real production-shaped tracer-bullet path before breadth unless acceptance or proof requires breadth. | Prefer one meaningful path over horizontal surface area. | Component masquerade and whole-feature expansion. |
| Tool choice, local route, and sequencing belong to the agent inside the locked slice. | Preserve autonomy inside a clear boundary. | Timid over-asking. |
| Changed slice, proof target, acceptance, or user-owned commitment uses the existing commitment-boundary rule. | Avoid duplicating commitment authority. | Unauthorized commitment changes and weaker ask logic. |
| Active diff remains in scope only while it is one concept tied to one proof story. | Turn one-concept pressure into a mid-implementation scope gate, not whole-skill completion. | Multiple concepts being narrated as one slice or completion being claimed before proof/review/lock. |
| Scope-pressure recheck applies to the active implementation diff and remaining changed artifacts, not disposable scratch discovery. | Preserve useful exploration while keeping implementation spread tied to the locked slice's proof target/proof story. | Scratch bans, hidden file spread, and leftover throwaway artifacts. |
| No remaining changed file/module/artifact without an in-scope reason. | Make file spread observable without treating disposable scratch as implementation spread. | Broad rewrites hidden behind low LOC. |
| No named proof/acceptance/affected-proof-surface coupling, no required coupled edit. | Keep coupled edits from becoming a sprawl escape hatch. | Optional breadth hidden as necessary coupling. |
| No protected, behavior-preserving, in-scope relation to preserving or proving this slice's proof target, no refactor. | Allow proof-protecting refactors without opening general cleanup. | General maintainability drift tangling with behavior, or necessary proof-preserving refactors being blocked. |
| No focused-check classification, no widening. | Keep mid-run tool feedback inside scope. | Chasing unrelated failures. |
| No failed focused check that would widen, redirect, or exit the slice without an explicit `fix-in-slice`, commitment-boundary, split, follow-up, ask, or blocker outcome. | Force proof feedback into a bounded decision. | Failed checks becoming silent scope expansion. |
| No direct changed-commitment focused-check failure without stopping at the existing commitment-boundary rule. | Preserve the ask boundary without duplicating commitment authority. | Named commitment failures falling through to adjacent/tooling routing. |
| No adjacent/environment-tooling fix unless the locked slice cannot be proven without it and it changes no commitment covered by the commitment-boundary rule; commitment-changing fixes stop at that rule, and non-proof-blocking failures split, record a follow-up, ask, or report a blocker. | Preserve the ask boundary while allowing only proof-blocking local fixes. | Tooling fixes becoming unauthorized commitment changes, unrelated failure chasing, or broad "proof-required" rationalization. |
| Fixed-point review findings stay in `Converge`. | Keep mid-run proof feedback separate from final review. | `$review` duplication. |

## 6. Context Pointer Candidates

| Pointer Text | Target Support Doc | Why It Should Be Disclosed | When Agent Should Open It |
| --- | --- | --- | --- |
| No runtime pointer proposed yet. | None. | Prompt 09 found possible support value but not enough evidence to create or point to a support doc before validation. | Reconsider only if Prompt 10 or final prune proves taxonomy, walking-skeleton nuance, ownership examples, or offload caveats are needed. |

Do not create support docs in Prompt 08. Cut the prior source/no-op research
pointer; research history belongs to the prompt pipeline, not runtime support.

## 7. Cut / Preserve Log

| Material | Cut / Preserve / Move | Why |
| --- | --- | --- |
| `bounded slice` | Preserve | Core execution handle. |
| `tracer bullet` | Preserve | Strong leading word for one real path; paired with production-shaped wording. |
| `support slice` | Preserve | Prevents fake behavior language for support work. |
| `one concept` / `one proof story` | Preserve | Best compact completion and split pressure. |
| `file spread` | Preserve as action gate | Useful only when it triggers remaining implementation diff recheck, not disposable scratch discovery. |
| Active implementation diff scope pressure | Preserve / sharpen | Prompt 09 feedback requires scope pressure to check the active implementation diff and remaining artifacts, not planned/contextual work or disposable scratch. |
| Generic scratch cleanup detail | Cut / owned elsewhere | Current `implement` and the engineering contract already own generic scratch allowance and cleanup; Facet 1 only needs the slice/proof uncertainty role and scratch-spread boundary. |
| `explicit unknown` | Cut / translate | Too vague; replaced with a named discovery/evidence action, then an updated expected edit surface before selected-slice implementation edits. |
| `likely touched area` | Cut / translate | Too vague; replaced with expected edit surface. |
| Discovery target as completed lock | Cut / translate | Discovery can be the next action, but the lock must be updated before implementation edits. |
| Discovery target as edit-surface substitute | Cut / translate | Discovery cannot stand in for a completed slice lock; replaced with required expected edit surface plus a next-action discovery/update-lock rule. |
| Implementation-edit lock versus Explore probes | Preserve / sharpen | The lock blocks edits intended to complete the selected slice, while read-only discovery and tiny reversible seam probes remain available to find the real seam. |
| `ordinary implementation technique` / `agent-owned technique` | Cut / translate | Weak phrase; replaced with tool choice, local route, and sequencing. |
| `smallest` support wording | Cut / translate | Subjective; replaced with what proves the named unblocker or risk. |
| `No in-scope reason, no touch` | Cut / translate | `Touch` can include exploration; replaced with changed file/module/artifact gate. |
| Standalone scope-evidence line | Cut / merge | Descriptive alone; behavior lives in changed-file/module/artifact recheck. |
| Bare `required coupled edit` | Cut / define | Replaced with named proof/acceptance coupling or a named affected check, command, generated artifact, or build path. |
| `locked proof` | Cut / translate | Too loose; replaced with locked slice's proof target and proof story. |
| Broad integrity phrase | Cut / translate | Too broad; replaced with named affected check, command, generated artifact, or build path. |
| Named affected proof surface | Preserve / sharpen | Prompt 09 feedback requires coupled edits to name an affected check, command, generated artifact, or build path rather than claiming broad integrity. |
| Slippery refactor-protection phrase | Cut / translate | Replaced with preserving or proving this slice's proof target. |
| Preserve or prove this slice's proof target | Preserve / sharpen | Prompt 09 feedback requires refactors to stay tied to preserving or proving this slice's proof target, with procedure left elsewhere. |
| General maintainability refactor rationale | Cut | General cleanup can be valuable, but it is not part of this bounded slice unless needed to preserve or prove the slice proof target. |
| Disposable scratch discovery as scope-pressure surface | Cut | Scratch remains available for discovery; S1 applies to the active implementation diff and artifacts that remain after cleanup. |
| `changed file/module/artifact` | Preserve / qualify | Use `remaining changed file/module/artifact` for implementation-scope gates so throwaway scratch is not mistaken for slice spread. |
| `classification and disposition` | Cut / translate | Bureaucratic; replaced with explicit fix-in-slice/commitment-boundary/split/follow-up/ask/blocker outcomes and adjacent/tooling routing. |
| `ask-rule commitments` / ambiguous `Otherwise` | Cut / translate | Replaced with repo-native user-owned commitment language and explicit F3 branches: fix/rerun, commitment-boundary, or split/follow-up/ask/blocker. |
| Direct `changed commitment` category | Preserve / route | Prompt 09 found the category useful but dangling; route it to the existing commitment-boundary rule instead of adding new commitment taxonomy. |
| `Proof-required` adjacent/tooling branch | Cut / translate | Too easy to rationalize broadly; replaced with "locked slice cannot be proven without the fix." |
| Duplicated commitment examples in F3c | Cut / point | Commitment taxonomy belongs to the commitment-boundary rule; F3c should point there instead of restating dependency/tooling/security/slice examples. |
| Whole-skill `Done only when` wording | Cut / translate | P5 is a local implementation-step completion gate, not the whole-skill completion criterion. |
| Phase-bound scratch cutoff | Cut / translate | Too narrow; scratch remains available when it clarifies the bounded slice, proof target, or validation evidence and is cleaned before final delivery. |
| Runtime source/no-op pointer | Cut | Prompt-pipeline material, not runtime support. |
| Walking-skeleton nuance | Move | Too conditional for default runtime line. |
| TDD mechanics | Move elsewhere | `$tdd` and Facet 5 own it. |
| Fixed-point review | Move elsewhere | `$review` and Facet 8 own it. |
| Baseline capture | Move elsewhere | Facet 2 owns it. |
| Commitment-boundary detail | Move elsewhere | Facet 4 and engineering contract own it. |
| Protected simplification procedure | Move elsewhere | Facet 7 owns it. |
| Commit/note behavior | Move elsewhere | Facet 8 owns it. |

## 8. Candidate Compact Draft

```markdown
### Bound The Slice

Use inspection, read-only discovery, scratch work, and tiny reversible Explore probes to resolve slice-lock or proof uncertainty, including which seam and evidence will prove the slice. Keep scratch disposable under the existing scratch cleanup rule unless it is promoted with a named in-scope proof reason.

Before edits intended to implement the selected slice, lock the bounded slice: behavior path or support purpose, checkable proof target, non-goals, expected edit surface, and focused check or evidence target. If the edit surface is unknown, name the exact discovery question or evidence action, then use read-only discovery or a tiny reversible Explore probe only to find the real seam; update the lock before selected-slice implementation edits.

For support work, name the exact unblocker or risk and the validation signal that proves it. No support purpose and validation, no support slice.

If the proof target is not checkable, narrow or ask before selected-slice implementation edits.

Done when the slice lock is complete, including a checkable proof target and expected edit surface; a discovery question does not count as a completed lock until the lock is updated.

### Implement One Path

For behavior work, implement one real production-shaped tracer-bullet path before breadth unless acceptance criteria or proof needs require breadth.

For support work, change only what is needed to prove the named unblocker or risk; move optional cleanup to follow-up.

Inside the locked slice, choose the tools, local implementation route, and sequencing of edits and checks without asking.

If that choice would change the locked slice, proof target, acceptance, or another user-owned commitment, stop and apply the existing commitment-boundary rule.

The active diff remains in scope only while it can be summarized as one concept tied to one proof story; if it cannot, narrow, split, record a follow-up, or ask before continuing.

### Keep Scope Pressure

When file spread, optional variants, broad refactors, or a second concept appears, re-check the active implementation diff and each remaining changed file/module/artifact against the locked slice's proof target and proof story. Do not count disposable scratch discovery as implementation spread while it remains throwaway; before delivery, delete scratch or promote it only with a named in-scope proof reason.

No remaining changed file/module/artifact without an in-scope reason tied to the proof target, proof story, acceptance criteria, or a required coupled edit.

A required coupled edit is a change needed to preserve the named proof target, satisfy a named acceptance criterion, or keep a named affected check, command, generated artifact, or build path valid for this slice. Keep it only when that coupling is named; otherwise split it, record a follow-up, or ask.

Refactor only when protected, behavior-preserving, in-scope, and needed to preserve or prove this slice's proof target. Refactors that are merely generally cleaner or more maintainable are outside this slice; split, record a follow-up, or ask. Leave refactor procedure to protected simplification and `$tdd`.

Done when every remaining changed file/module/artifact has an in-scope reason and the active diff remains one concept with one proof story.

### Classify Proof Feedback

When a focused check fails during implementation, classify it before widening the diff: `in-slice`, `adjacent`, `changed commitment`, or `environment/tooling`.

Fix and rerun `in-slice` failures inside the current slice.

For `changed commitment` focused-check failures, stop and apply the existing commitment-boundary rule.

For `adjacent` or `environment/tooling` focused-check failures, choose one branch before widening:

- If the locked slice cannot be proven without the fix, and the fix does not change a commitment covered by the commitment-boundary rule: make the smallest local fix needed to unblock that proof, then rerun the focused check.
- If the locked slice cannot be proven without the fix, but the fix would change a commitment covered by the commitment-boundary rule: stop and apply that rule.
- If the locked slice can still be proven without the fix: do not fix it in this slice; split it, record a follow-up, ask, or report the blocker.

Do not use this mid-run classification for fixed-point review findings; `Converge` owns those.

Done when any failed focused check that would widen, redirect, or exit the slice has an explicit outcome: `fix-in-slice`, commitment-boundary, split, follow-up, ask, or blocker.
```

## 9. Audit Handoff

candidate-draft decision: `ready-for-behavior-audit`

Lines most likely to be no-ops:

- B1 scratch/probe line. Audit whether the slice/proof uncertainty role is
  behaviorally needed inline, or whether existing `Orient And Explore` scratch
  text already carries it after the selected-slice edit gate is integrated.
- S1 scratch distinction. Audit whether excluding disposable scratch from
  implementation spread is needed inline or already carried by the scratch
  cleanup line.
- `Do not use this mid-run classification...` Audit whether the guard is still
  necessary once the block is placed before `Converge`.

Lines most likely to duplicate another skill or contract:

- direct `changed commitment` routing and `apply the existing
  commitment-boundary rule` point to Facet 4/current
  `implement` and must not grow into a duplicate commitment list.
- F3c `commitment covered by the commitment-boundary rule` should remain a
  pointer, not a new commitment taxonomy.
- `Leave refactor procedure to protected simplification and $tdd` guards
  ownership and should not become refactor procedure.
- `Converge owns those` guards `$review` ownership and may be final-pruned if
  placement makes it redundant.

Gates most likely to be too weak:

- discovery/probe results must update the lock before implementation edits;
- adjacent/environment-tooling fixes allowed only when the locked slice cannot
  be proven without them and they change no commitment covered by the
  commitment-boundary rule;
- direct changed-commitment routing to the existing commitment-boundary rule;
- disposable scratch promotion/deletion boundary;
- named affected proof surface for coupled edits;
- preserve/prove relation to this slice's proof target;
- P5 one-concept/proof-story scope gate must trigger narrow/split/follow-up/ask,
  not become a narration loophole;
- explicit outcome: `fix-in-slice`, commitment-boundary, split, follow-up, ask,
  or blocker.

Gates most likely to be too heavy:

- `No checkable proof target, no edit intended to complete the selected slice`;
- read-only discovery and tiny reversible Explore probe exception;
- `No remaining changed file/module/artifact without an in-scope reason`;
- `No protected, behavior-preserving relation to preserving or proving this
  slice's proof target, no refactor`;
- adjacent/tooling routing with locked-slice-cannot-be-proven-without-it,
  commitment-boundary, and not-proof-blocking branches.

Context-pointer decisions to audit:

- whether support-slice examples need a runtime pointer after validation;
- whether walking-skeleton guidance should be named at all in Facet 1 runtime;
- whether delegation support belongs in this skill or only in process docs;
- whether the absence of a support pointer keeps runtime too dense or correctly
  avoids premature support-doc sprawl.

Existing skill behavior that must not regress:

- one issue only;
- baseline capture before edits;
- domain/context intake;
- `.tmp/` exploration, throwaway repros, tiny reversible Explore probes, and
  scratch cleanup;
- `$tdd` handoff and semantic proof;
- protected simplification;
- `$review`;
- commit and issue note;
- preserving unrelated work.

Validation tasks to remember:

- Test whether candidate wording stops issue-title implementation without
  blocking read-only discovery, `.tmp/` spikes, throwaway repros, later scratch
  proof work, tiny reversible Explore probes, or scratch cleanup before final
  delivery.
- Test whether unknown edit surface becomes a named discovery/evidence action,
  then an updated lock before implementation edits.
- Test whether support work names exact purpose and validation instead of fake
  user value.
- Test whether optional variants become follow-ups without dodging required
  acceptance or proof needs.
- Test whether P5 acts as a scope gate and does not imply whole-skill completion
  before validation, review, commit, and note.
- Test whether file spread causes remaining changed-file/module/artifact mapping
  rather than numeric policy.
- Test whether scope pressure checks the active implementation diff, not
  planned/contextual work or disposable scratch.
- Re-audit Prompt 09 revisions: scratch/probe discovery boundary, completed
  lock gate, P5 scope gate, and F3c proof-blocking/commitment-boundary routing.
- Test whether disposable scratch is excluded from implementation spread while
  throwaway, then deleted or promoted only with a named in-scope proof reason
  before delivery.
- Test whether coupled edits name proof/acceptance coupling or a named affected
  check, command, generated artifact, or build path.
- Test whether proof-target-preserving refactors are allowed while general
  maintainability refactors are split, followed up, asked about, or blocked.
- Test whether a focused-check failure is classified before widening and gets a
  `fix-in-slice`, commitment-boundary, split, follow-up, ask, or blocker
  outcome.
- Include one `in-slice`, one `adjacent`, one `changed commitment`, and one
  `environment/tooling` proof-feedback scenario.
- For F3, include one direct `changed commitment` failure, one local
  `environment/tooling` failure where the locked slice cannot be proven without
  the fix, one proof-blocking adjacent/tooling failure that changes a commitment
  covered by the commitment-boundary rule, and one adjacent/tooling failure where
  the locked slice can still be proven without fixing it.
- Test whether the explicit continue rule prevents over-asking inside the
  locked slice.
