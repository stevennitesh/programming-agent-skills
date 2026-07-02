# Facet 1: Bounded Slice Behavior Audit

This reruns
[`docs/synthesis/methods/prompts/09-behavior-audit.md`](../../../methods/prompts/09-behavior-audit.md)
for `implement` Facet 1 after the B1/B2/B5, P5, and F3c compact-draft
revision.

## 1. Audit Scope

Facet audited: `implement` Facet 1, `Bounded Slice`.

Compact draft audited:
[`08-compact-draft.md`](08-compact-draft.md).

Generous synthesis reference:
[`07-generous-synthesis.md`](07-generous-synthesis.md).

Existing behavior that must not regress:

- select one ready issue and stop after one issue;
- capture baseline and preserve unrelated work before editing;
- read issue, spec, acceptance criteria, blockers, and out-of-scope boundaries;
- keep read-only discovery, `.tmp` spikes, copied references, experiments,
  rough notes, throwaway repros, and tiny reversible seam probes available when
  useful;
- delete scratch artifacts before final delivery unless the user asks to
  preserve them;
- use `$tdd` where practical and prove semantic correctness through useful
  seams;
- simplify only while behavior is protected;
- run `$review` from the starting ref;
- commit and leave an implementation note.

Related owners checked:

- `skills/current/implement/SKILL.md`;
- `docs/agents/engineering-contract.md`;
- `skills/current/tdd/SKILL.md`;
- `skills/current/review/SKILL.md`.

This audit does not validate against real tasks, final-prune runtime text, edit
`SKILL.md`, add support docs, or change invocation policy.

## 2. Candidate Line Inventory

| Line ID | Candidate Line | Section | Type |
| --- | --- | --- | --- |
| I1 | No invocation wording change proposed. | Candidate Invocation / Description Wording | invocation |
| B1 | Use inspection, read-only discovery, scratch work, and tiny reversible Explore probes to resolve slice-lock or proof uncertainty, including which seam and evidence will prove the slice. Keep scratch disposable under the existing scratch cleanup rule unless it is promoted with a named in-scope proof reason. | Bound The Slice | step |
| B2 | Before edits intended to implement the selected slice, lock the bounded slice: behavior path or support purpose, checkable proof target, non-goals, expected edit surface, and focused check or evidence target. If the edit surface is unknown, name the exact discovery question or evidence action, then use read-only discovery or a tiny reversible Explore probe only to find the real seam; update the lock before selected-slice implementation edits. | Bound The Slice | gate |
| B3 | For support work, name the exact unblocker or risk and the validation signal that proves it. No support purpose and validation, no support slice. | Bound The Slice | gate |
| B4 | If the proof target is not checkable, narrow or ask before selected-slice implementation edits. | Bound The Slice | stop/ask rule |
| B5 | Done when the slice lock is complete, including a checkable proof target and expected edit surface; a discovery question does not count as a completed lock until the lock is updated. | Bound The Slice | completion criterion |
| P1 | For behavior work, implement one real production-shaped tracer-bullet path before breadth unless acceptance criteria or proof needs require breadth. | Implement One Path | step |
| P2 | For support work, change only what is needed to prove the named unblocker or risk; move optional cleanup to follow-up. | Implement One Path | gate |
| P3 | Inside the locked slice, choose the tools, local implementation route, and sequencing of edits and checks without asking. | Implement One Path | step |
| P4 | If that choice would change the locked slice, proof target, acceptance, or another user-owned commitment, stop and apply the existing commitment-boundary rule. | Implement One Path | stop/ask rule |
| P5 | The active diff remains in scope only while it can be summarized as one concept tied to one proof story; if it cannot, narrow, split, record a follow-up, or ask before continuing. | Implement One Path | scope gate |
| S1 | When file spread, optional variants, broad refactors, or a second concept appears, re-check the active implementation diff and each remaining changed file/module/artifact against the locked slice's proof target and proof story. Do not count disposable scratch discovery as implementation spread while it remains throwaway; before delivery, delete scratch or promote it only with a named in-scope proof reason. | Keep Scope Pressure | step |
| S2 | No remaining changed file/module/artifact without an in-scope reason tied to the proof target, proof story, acceptance criteria, or a required coupled edit. | Keep Scope Pressure | gate |
| S3 | A required coupled edit is a change needed to preserve the named proof target, satisfy a named acceptance criterion, or keep a named affected check, command, generated artifact, or build path valid for this slice. Keep it only when that coupling is named; otherwise split it, record a follow-up, or ask. | Keep Scope Pressure | gate |
| S4 | Refactor only when protected, behavior-preserving, in-scope, and needed to preserve or prove this slice's proof target. Refactors that are merely generally cleaner or more maintainable are outside this slice; split, record a follow-up, or ask. Leave refactor procedure to protected simplification and `$tdd`. | Keep Scope Pressure | gate |
| S5 | Done when every remaining changed file/module/artifact has an in-scope reason and the active diff remains one concept with one proof story. | Keep Scope Pressure | completion criterion |
| F1 | When a focused check fails during implementation, classify it before widening the diff: `in-slice`, `adjacent`, `changed commitment`, or `environment/tooling`. | Classify Proof Feedback | step |
| F2 | Fix and rerun `in-slice` failures inside the current slice. | Classify Proof Feedback | step |
| F3a | For `changed commitment` focused-check failures, stop and apply the existing commitment-boundary rule. | Classify Proof Feedback | stop/ask rule |
| F3b | For `adjacent` or `environment/tooling` focused-check failures, choose one branch before widening. | Classify Proof Feedback | gate |
| F3c | Branches: if the locked slice cannot be proven without the fix and no commitment changes, make the smallest local proof-unblocking fix and rerun; if it would change a commitment covered by the commitment-boundary rule, stop and apply that rule; if the slice can still be proven without the fix, do not fix it in this slice and split, follow up, ask, or report the blocker. | Classify Proof Feedback | stop/ask rule |
| F4 | Do not use this mid-run classification for fixed-point review findings; `Converge` owns those. | Classify Proof Feedback | ownership guard |
| F5 | Done when any failed focused check that would widen, redirect, or exit the slice has an explicit outcome: `fix-in-slice`, commitment-boundary, split, follow-up, ask, or blocker. | Classify Proof Feedback | completion criterion |
| CP1 | No runtime pointer proposed yet. | Context Pointer Candidates | context pointer |

## 3. Line-By-Line Behavior Audit

| Line ID | Behavior Changed? | Failure Prevented | Evidence Required | Verdict | Reason |
| --- | --- | --- | --- | --- | --- |
| I1 | No. | Invocation drift while auditing one runtime facet. | Current description still targets one issue through implementation, verification, review, commit, and note. | keep | Facet 1 changes post-invocation behavior, not trigger matching. |
| B1 | Yes. | Scratch/probe discovery either being banned or becoming hidden implementation spread. | Scratch remains disposable or is promoted with a named in-scope proof reason. | keep | It preserves Explore while narrowing scratch/probes to slice-lock or proof uncertainty and points to the existing cleanup owner. |
| B2 | Yes. | Issue-title implementation and implementation edits before a proof boundary exists. | Named behavior/support path, proof target, non-goals, expected edit surface, and focused check/evidence target. | keep | Core lock gate; it also preserves read-only discovery and tiny reversible Explore probes without letting them become implementation permission. |
| B3 | Yes. | Support work pretending to be behavior value. | Named unblocker/risk plus observable validation signal. | keep | Strong support-slice gate with low duplication. |
| B4 | Yes. | Implementing when done cannot be checked. | Narrowed proof target or explicit user answer. | keep | Blunt enforcement line for B2's checkable-proof requirement. |
| B5 | Yes. | Treating a discovery question as a completed lock. | Completed checkable lock with known edit surface after any discovery/probe. | keep | Local completion criterion for Bound The Slice; no whole-skill done confusion. |
| P1 | Yes. | Horizontal breadth and component masquerade. | One production-shaped path tied to acceptance or proof need. | keep | Allows acceptance/proof-driven breadth while preserving tracer-bullet pressure. |
| P2 | Yes. | Optional support cleanup expanding the slice. | Change tied to named unblocker/risk proof. | keep | Good support-slice pressure, not mere duplication. |
| P3 | Yes. | Timid over-asking inside a locked slice. | Choice stays inside locked commitments and proof story. | keep | Duplicates the engineering contract lightly, but preserves critical runtime autonomy. |
| P4 | Yes. | Unauthorized commitment changes. | Changed commitment identified and existing commitment-boundary rule applied. | keep | Proper pointer to the existing owner. |
| P5 | Yes. | Multiple concepts being narrated as one slice. | Active diff remains one concept tied to one proof story, or it is narrowed/split/followed up/asked about. | keep | Reworked as a mid-implementation scope gate, not a completion criterion. |
| S1 | Yes. | File spread, optional variants, broad refactors, or second concepts becoming silent scope expansion. | Active implementation diff and remaining artifacts checked against proof target/story; scratch deleted or promoted before delivery. | keep | Prior S1 scratch concern remains resolved. |
| S2 | Yes. | Broad edits hidden behind low line count. | In-scope reason for every remaining changed file/module/artifact. | keep | Strong observable gate not owned elsewhere at this specificity. |
| S3 | Yes. | Coupled edits becoming a sprawl escape hatch. | Named proof target, acceptance criterion, affected check, command, generated artifact, or build path. | keep | Prior S3 concern remains resolved; coupling is now narrow and checkable. |
| S4 | Yes. | General maintainability cleanup tangling with behavior. | Refactor is protected, behavior-preserving, in-scope, and preserving/proving this proof target. | keep | Prior S4 concern remains resolved; final sentence is an ownership guard. |
| S5 | Yes. | Finishing scope pressure while artifacts remain unexplained. | Remaining artifact mapping plus one-concept proof-story summary. | keep | Slightly redundant with S2/P5, but useful as local completion pressure. |
| F1 | Yes. | Chasing unrelated failures before classification. | Failure classified before widening. | keep | Strong mid-run gate. |
| F2 | Yes. | Treating ordinary in-slice failure as scope ambiguity. | Failure fixed and rerun inside current slice. | keep | Direct and non-ceremonial. |
| F3a | Yes. | Changed-commitment failures falling through to tooling/adjacent handling. | Commitment-boundary rule applied. | keep | Direct route now exists and avoids duplicating taxonomy. |
| F3b | Yes. | Adjacent/tooling failures widening the diff without a branch decision. | Branch chosen before widening. | keep | Useful inline routing. |
| F3c | Yes. | Broad proof-required rationalization, unrelated failure chasing, and commitment-changing local fixes. | Proof-blocking necessity, commitment impact, and explicit outcome. | keep | It now fixes only proof blockers, points commitment changes to the existing rule, and avoids repeating the commitment taxonomy. |
| F4 | Yes, as an ownership guard. | Mid-run proof-feedback classification absorbing `$review` findings. | Fixed-point findings remain in `Converge`. | keep | Keep through validation; possible final-prune if placement makes ownership obvious. |
| F5 | Yes. | Failed checks causing silent widening, redirect, or exit. | Explicit `fix-in-slice`, commitment-boundary, split, follow-up, ask, or blocker outcome. | keep | The qualifier avoids making every normal red/green failure bureaucratic. |
| CP1 | Yes, by refusing a pointer for now. | Premature support-doc sprawl. | Prompt 10/final prune proves a pointer is needed before one is created. | keep | No branch-specific reference has earned disclosure yet. |

## 4. No-Op And Weak Language Check

| Line ID | Weakness | Why It Is Weak | Stronger Direction |
| --- | --- | --- | --- |
| B1 | Possible overlap with existing scratch text. | Existing `implement` already allows `.tmp` scratch and cleanup. | Keep for validation because this line adds slice/proof uncertainty and promotion criteria. |
| B2 | `tiny reversible Explore probe` could become a loophole. | An agent might treat probe work as implementation permission. | Validate that probes only find the seam and update the lock before implementation edits. |
| B5 | `lock is complete` could be hand-wavy. | A completed lock needs concrete fields, not a feeling. | Validate against B2 fields: proof target, edit surface, and focused check/evidence target. |
| P1 | `proof needs require breadth`. | Could justify extra cases too easily. | Validate that breadth is tied to the locked proof target or acceptance. |
| P3 | Duplicates autonomy contract. | The engineering contract already says technique belongs to the agent. | Keep for validation because it prevents over-asking inside this runtime step. |
| P5 | `one concept` / `one proof story` can be over-narrated. | An agent can explain two concepts as one story unless the proof target anchors it. | Validate with multi-concept diffs. |
| S1 | Scratch distinction duplicates cleanup. | Generic cleanup already exists. | Keep because it prevents disposable scratch from counting as implementation spread. |
| S4 | Ownership sentence may be extra. | `$tdd` and protected simplification own procedure. | Keep through validation; final-prune if integration placement makes it obvious. |
| F3c | `report the blocker` in a non-proof-blocking branch. | If the locked slice can still be proven, blocker wording could invite stopping unnecessarily. | Validate that report/blocker does not halt a provable slice unless there is a real blocker outside the slice. |
| F4 | Possible ownership no-op. | If placed before `Converge`, `$review` ownership may already be obvious. | Keep through validation; final-prune if redundant. |

## 5. Gate Strength Check

| Line ID | Gate | Too Weak If | Too Heavy If | Revision Direction |
| --- | --- | --- | --- | --- |
| B2 | No implementation edit before lock or named discovery/probe action. | Probe work becomes implementation permission. | Tiny safe seam probes are blocked. | Keep; validate probe boundary. |
| B3 | No support purpose and validation, no support slice. | Support work proceeds with vague cleanup intent. | Legit support work with clear validation is blocked. | Keep. |
| B4 | No checkable proof target, narrow or ask. | Agent proceeds with untestable proof. | Agent asks instead of doing obvious narrowing. | Keep. |
| B5 | Bound The Slice is not complete until the lock is concrete. | Discovery target substitutes for completed lock. | Tiny issues must fill a planning essay. | Keep; validate tiny-issue compression. |
| P1 | One production-shaped tracer-bullet path before breadth. | Component work counts as a path. | Needed acceptance/proof breadth is blocked. | Keep; validate acceptance/proof breadth. |
| P4 | Changed commitment uses existing commitment-boundary rule. | Agent changes commitments as technique. | Internal technique choices trigger asks. | Keep. |
| P5 | Active diff remains in scope only while one concept has one proof story. | Two concepts are narrated as one. | Necessary coupled edits are split apart. | Keep; validate against coupled-edit cases. |
| S1 | Scope-pressure recheck over active implementation diff and remaining artifacts. | Scratch survives without deletion/promotion or file spread is not mapped to proof. | Disposable scratch is banned during discovery. | Keep. |
| S3 | No named proof/acceptance/affected-proof-surface coupling, no required coupled edit. | `build path` is named vaguely. | Required generated/config/build updates are blocked. | Keep; validate. |
| S4 | No refactor without preserve/prove relation to this slice's proof target. | General maintainability counts as preserving/proving. | Proof-protecting refactor is blocked. | Keep; validate. |
| F1 | No focused-check classification, no widening. | Classification is skipped. | Every ordinary red/green failure needs ceremony. | Keep; applies to failures that would widen, redirect, or exit. |
| F3c | Adjacent/environment-tooling fix only when the locked slice cannot be proven without it and no commitment changes. | Proof-blocking is asserted without necessity. | Local proof-blocking fixes are blocked. | Keep; validate. |
| F5 | No failed check outcome, no widening/redirect/exit. | Outcome can be implicit. | Every small test failure needs reporting. | Keep. |

## 6. Ownership / Duplication Check

| Line ID | Possible Duplicate Owner | Conflict Or Duplication | Action |
| --- | --- | --- | --- |
| B1 | Current `implement`; engineering contract Exploration. | Generic scratch cleanup is owned elsewhere, but slice/proof uncertainty role is local. | Keep; final-prune only if integration makes it redundant. |
| B2-B5 | Current `implement` Orient and Explore; engineering contract Orient/Explore/Choose. | Sharpens selected-slice lock without replacing issue/spec intake. | Keep. |
| P1 | `$tdd`; engineering contract Slicing. | Must not define TDD mechanics. | Keep as slice-shape line. |
| P3-P4 | Engineering contract Autonomy And Commitment. | P4 points to existing owner. | Keep adjacent; do not expand taxonomy. |
| S1-S5 | Current `implement`; engineering contract slicing/simplification/proof. | Operational gates are useful; avoid re-teaching broad contract rules. | Keep through validation. |
| S4 | `$tdd`; protected simplification; later facets. | Final ownership sentence is guard, not procedure. | Keep through validation; possible final-prune. |
| F3a/F3c | Current `implement` ask rule; engineering contract commitments. | Points to commitment-boundary owner without restating taxonomy. | Keep. |
| F4 | `$review`; current `implement` Converge. | Ownership guard may duplicate final placement. | Keep through validation; possible final-prune. |
| CP1 | Support docs. | No support doc earned yet. | Keep no-pointer decision. |

## 7. Context Pointer Check

| Line ID | Inline Or Pointer? | Target If Pointer | Why | Risk |
| --- | --- | --- | --- | --- |
| B1-B5 | Inline. | None. | Most `implement` runs need bounded-slice setup. | Too much inline ceremony if final integration does not compress. |
| P1-P5 | Inline. | None. | One-path pressure is core runtime behavior. | Pointer would hide the main behavior. |
| S1-S5 | Inline for validation. | Possible future examples support doc only. | Scope pressure must be visible during implementation. | Examples could bloat runtime. |
| F1-F5 | Inline for validation. | Possible future proof-feedback examples. | Focused-check failures need immediate routing. | Branch examples could bloat runtime. |
| CP1 | No pointer. | None yet. | Support taxonomy, walking-skeleton nuance, delegation, and ownership examples are not proven necessary. | Prompt 10 may reveal a missing branch-specific pointer. |

## 8. Leading Word Check

| Line ID | Leading Word | Strong / Weak | Why | Action |
| --- | --- | --- | --- | --- |
| B1-B5 | `bounded slice`, `proof target`, `seam` | Strong | Recruits slicing, proof, and localizing priors without long explanation. | Keep. |
| P1 | `tracer-bullet path` | Strong | Anchors one real vertical path before breadth. | Keep. |
| P2/B3 | `support work` / `support slice` | Strong | Prevents fake behavior language for support work. | Keep. |
| P5/S5 | `one concept`, `one proof story` | Strong | Compact pressure against sprawl. | Keep; validate narration risk. |
| S1 | `file spread` | Strong | Makes scope pressure visible and binds it to proof target/story. | Keep. |
| S3 | `required coupled edit` | Strong after definition | Converts a possible loophole into a named gate. | Keep. |
| F1-F5 | `in-slice`, `adjacent`, `changed commitment`, `environment/tooling` | Strong enough | Operational routing categories with explicit outcomes. | Keep. |

## 9. Regression Check

| Existing Behavior | Preserved? | Candidate Line(s) | Risk |
| --- | --- | --- | --- |
| One issue only. | Yes. | P1, P5, S1-S5 | Final integration must not imply multiple tracer bullets or support slices. |
| Baseline capture before edits. | Yes, by omission. | None | Facet 1 must not move or weaken baseline behavior. |
| Full issue/spec/acceptance intake. | Yes, by omission. | B2-B5 | Bound The Slice must not replace reading issue context. |
| `.tmp` exploration and scratch cleanup. | Yes. | B1, S1 | Generic cleanup remains owned by current `implement`; validation should watch for duplication. |
| Tiny reversible Explore edits. | Yes. | B1, B2 | Validate that probes do not become implementation permission. |
| TDD handoff and semantic proof. | Yes. | P1, S4 | Do not let tracer-bullet/refactor wording replace `$tdd` mechanics. |
| Protected simplification. | Yes. | S4 | S4 allows proof-target-preserving refactor while rejecting general cleanup drift. |
| `$review` from starting ref. | Yes. | F4 | F4 must not duplicate fixed-point review procedure. |
| Commit and issue note. | Yes, by omission. | None | Later `implement` sections keep ownership. |
| Preserving unrelated work. | Yes. | S2-S5 | Changed-artifact gates must not encourage touching unrelated dirty work. |
| Ask boundary for commitments. | Yes. | P4, F3a, F3c | F3c points to the existing commitment-boundary owner. |

## 10. Revised Candidate Line Set

### Keep

- I1: No invocation wording change proposed.
- B1: Use inspection, read-only discovery, scratch work, and tiny reversible
  Explore probes to resolve slice-lock or proof uncertainty, including which
  seam and evidence will prove the slice. Keep scratch disposable under the
  existing scratch cleanup rule unless it is promoted with a named in-scope
  proof reason.
- B2: Before edits intended to implement the selected slice, lock the bounded
  slice: behavior path or support purpose, checkable proof target, non-goals,
  expected edit surface, and focused check or evidence target. If the edit
  surface is unknown, name the exact discovery question or evidence action,
  then use read-only discovery or a tiny reversible Explore probe only to find
  the real seam; update the lock before selected-slice implementation edits.
- B3: For support work, name the exact unblocker or risk and the validation
  signal that proves it. No support purpose and validation, no support slice.
- B4: If the proof target is not checkable, narrow or ask before selected-slice
  implementation edits.
- B5: Done when the slice lock is complete, including a checkable proof target
  and expected edit surface; a discovery question does not count as a completed
  lock until the lock is updated.
- P1: For behavior work, implement one real production-shaped tracer-bullet path
  before breadth unless acceptance criteria or proof needs require breadth.
- P2: For support work, change only what is needed to prove the named unblocker
  or risk; move optional cleanup to follow-up.
- P3: Inside the locked slice, choose the tools, local implementation route, and
  sequencing of edits and checks without asking.
- P4: If that choice would change the locked slice, proof target, acceptance, or
  another user-owned commitment, stop and apply the existing
  commitment-boundary rule.
- P5: The active diff remains in scope only while it can be summarized as one
  concept tied to one proof story; if it cannot, narrow, split, record a
  follow-up, or ask before continuing.
- S1: When file spread, optional variants, broad refactors, or a second concept
  appears, re-check the active implementation diff and each remaining changed
  file/module/artifact against the locked slice's proof target and proof story.
  Do not count disposable scratch discovery as implementation spread while it
  remains throwaway; before delivery, delete scratch or promote it only with a
  named in-scope proof reason.
- S2: No remaining changed file/module/artifact without an in-scope reason tied
  to the proof target, proof story, acceptance criteria, or a required coupled
  edit.
- S3: A required coupled edit is a change needed to preserve the named proof
  target, satisfy a named acceptance criterion, or keep a named affected check,
  command, generated artifact, or build path valid for this slice. Keep it only
  when that coupling is named; otherwise split it, record a follow-up, or ask.
- S4: Refactor only when protected, behavior-preserving, in-scope, and needed
  to preserve or prove this slice's proof target. Refactors that are merely
  generally cleaner or more maintainable are outside this slice; split, record a
  follow-up, or ask. Leave refactor procedure to protected simplification and
  `$tdd`.
- S5: Done when every remaining changed file/module/artifact has an in-scope
  reason and the active diff remains one concept with one proof story.
- F1: When a focused check fails during implementation, classify it before
  widening the diff: `in-slice`, `adjacent`, `changed commitment`, or
  `environment/tooling`.
- F2: Fix and rerun `in-slice` failures inside the current slice.
- F3a: For `changed commitment` focused-check failures, stop and apply the
  existing commitment-boundary rule.
- F3b: For `adjacent` or `environment/tooling` focused-check failures, choose
  one branch before widening.
- F3c: Use the three current branches: proof-blocking local fix with no
  commitment change; proof-blocking commitment change stops at the
  commitment-boundary rule; non-proof-blocking failures split, follow up, ask,
  or report the blocker.
- F4: Do not use this mid-run classification for fixed-point review findings;
  `Converge` owns those.
- F5: Done when any failed focused check that would widen, redirect, or exit the
  slice has an explicit outcome: `fix-in-slice`, commitment-boundary, split,
  follow-up, ask, or blocker.
- CP1: No runtime pointer proposed yet.

### Revise

- None before validation.

### Move To Support

- None before validation.

### Owned Elsewhere

- Generic scratch cleanup: current `implement` and engineering contract.
- Commitment taxonomy and ask procedure: engineering contract and later
  commitment-boundary facet.
- TDD mechanics: `$tdd`.
- Protected simplification procedure: current `implement`, engineering
  contract, and later simplification facet.
- Fixed-point review procedure: `$review` and current `implement` `Converge`.
- Commit and issue note behavior: current `implement` `Lock`.

### Cut

- None before validation.

## 11. Handoff To Validation

Audit decision: `ready-for-validation`.

Lines ready for validation:

- no invocation change;
- B1-B5 slice lock, scratch/probe discovery boundary, support purpose,
  checkable proof target, and completed-lock gate;
- P1-P5 production-shaped tracer-bullet path, support-work narrowness, agent
  autonomy inside the lock, commitment-boundary pointer, and one-concept scope
  gate;
- S1-S5 scope-pressure recheck, remaining-artifact in-scope reason, required
  coupled edit definition, proof-target-preserving refactor boundary, and local
  scope-pressure completion criterion;
- F1-F5 focused-check classification, in-slice fix/rerun, direct changed
  commitment route, adjacent/tooling proof-blocking branches, fixed-point review
  guard, and explicit outcomes;
- no runtime pointer proposed yet.

Lines that must be revised before validation:

- None.

Behaviors that need real-task validation:

- issue-title implementation stops before selected-slice implementation edits;
- read-only discovery, `.tmp` spikes, throwaway repros, later scratch proof
  work, and tiny reversible Explore probes remain available when they clarify
  slice-lock or proof uncertainty;
- tiny reversible Explore probes do not become implementation permission;
- unknown edit surface becomes a named discovery/evidence action, then an
  updated lock before implementation edits;
- support work names exact purpose and validation rather than fake user value;
- tiny obvious issues do not become over-ceremonial;
- vague `focused check or evidence target` does not pass as a real proof target;
- acceptance/proof-needed breadth remains allowed while optional variants become
  follow-ups;
- P5 cannot be used to narrate two concepts as one proof story;
- file spread causes remaining changed-file/module/artifact mapping rather than
  numeric policy;
- disposable scratch is excluded from implementation spread while throwaway,
  then deleted or promoted only with a named in-scope proof reason before
  delivery;
- coupled edits name proof/acceptance coupling or a named affected check,
  command, generated artifact, or build path;
- proof-target-preserving refactors are allowed while general maintainability
  refactors are split, followed up, asked about, or blocked;
- focused-check failures are classified before widening;
- adjacent/environment-tooling fixes are allowed only when the locked slice
  cannot be proven without them;
- `report the blocker` in the non-proof-blocking adjacent/tooling branch does
  not let the agent stop a provable slice unnecessarily;
- commitment-changing proof failures route to the existing commitment-boundary
  rule without adding a new taxonomy.

Gates that need real-task validation:

- no checkable proof target, no edit intended to implement the selected slice;
- unknown edit surface allows only named discovery/probe, then an updated lock;
- `No support purpose and validation, no support slice`;
- one production-shaped tracer-bullet path before breadth unless acceptance or
  proof requires breadth;
- active diff remains in scope only while it is one concept tied to one proof
  story;
- no remaining changed file/module/artifact without an in-scope reason;
- no required coupled edit without named proof/acceptance/affected-proof-surface
  coupling;
- no refactor without protected, behavior-preserving, in-scope relation to
  preserving or proving this slice's proof target;
- `No focused-check classification, no widening`;
- no adjacent/environment-tooling fix unless the locked slice cannot be proven
  without it and it changes no commitment covered by the commitment-boundary
  rule;
- no failed focused check that would widen, redirect, or exit the slice without
  an explicit `fix-in-slice`, commitment-boundary, split, follow-up, ask, or
  blocker outcome.

Regression risks to test:

- current issue selection, baseline, full context intake, `$tdd`, `$review`,
  commit/note, and unrelated-work preservation remain visible after integration;
- current `.tmp` cleanup behavior is preserved without being repeated into
  runtime bloat;
- tiny reversible Explore probes remain allowed but cannot become implementation
  permission;
- the facet is merged into existing `implement` bounded-slice/anti-widening
  wording rather than added as a duplicate lifecycle;
- P3 stays adjacent to P4 so "without asking" does not escape the commitment
  boundary;
- P5 does not imply whole-skill completion before validation, review, commit,
  and note;
- S4 does not absorb TDD refactor mechanics or protected simplification
  procedure;
- F3c does not grow a new commitment taxonomy;
- F4 does not duplicate fixed-point review once integrated.

Likely final-prune targets:

- B1 scratch/probe line if existing `implement` text carries generic scratch
  allowance/cleanup safely after the selected-slice edit gate is integrated;
- S1 scratch distinction if final integration already preserves the same
  disposable-scratch boundary;
- P3 autonomy reminder if validation shows it duplicates the engineering
  contract without reducing over-asking;
- S4's ownership sentence;
- F4 fixed-point review guard if placement before `Converge` makes ownership
  obvious.
