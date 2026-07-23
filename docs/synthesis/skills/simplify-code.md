# Simplify Code Promoted Runtime Synthesis

## Current Decision

Status: promoted in the fresh Deploy Campaign epoch started 2026-07-23.
The pruning-complete C1 package is now the canonical Simplify Code runtime.
It remains explicit-only and owns one bounded, behavior-preserving, unstaged
complexity cut; an explicitly requested finite serial `until-clean` campaign
inside one named region; or a fully accounted **No safe simplification**
result.

```text
current != B0 != C1
campaign shape = behavioral-candidate
Prompt 4 decision = accepted
Pruning Pass = pruning-not-needed
canonical runtime = exact C1
```

Canonical package identity:

- package: `skills/custom/simplify-code`;
- inventory: `SKILL.md`, `agents/openai.yaml`;
- tree SHA-256:
  `f3fa29e016e1ad88f77088e7b001f80db4a139b51d7da2125146fdda5c8cef06`;
- `SKILL.md` SHA-256:
  `97c2ab427bd71154c1f04bc72a1ba3e632c72406be52a88c633af86a3d2e68c4`;
- `agents/openai.yaml` SHA-256:
  `8ef184a5a1fdf5bb4b325c1e9ec5019bb2ad5536aa583d806c2bc6e1cc3c2a14`.

The promoted package is byte-identical to the Prompt 4-accepted and
pruning-complete C1. The accepted behavior proof therefore remains exact; the
lifecycle transition creates no reason to rerun it.

## Runtime Contract

The runtime has eight source-derived minimum units:

1. **Bounded admission and owner routes.** Admit a still-valid verified
   Improve Codebase candidate, user-named target, or one coherent current diff,
   in that order. Return absent or invalid targets and foreign work to the
   appropriate owner without copying that owner's procedure.
2. **Trace and before proof.** Trace authoritative commitments, operational
   paths, relevant work state, and one caller-facing seam. A failing,
   ambiguous, or semantically inadequate baseline prevents production
   mutation.
3. **Safe-cut selection.** Choose one coherent cut only when preserved
   behavior, proof, scope, strict burden reduction, and work-state boundaries
   are credible.
4. **Commitment and safety floor.** Preserve product intent, accepted
   behavior, public and data contracts, domain decisions, trust-boundary and
   data-loss controls, security, privacy, accessibility, concurrency,
   durability, ordering, timing, and compatibility.
5. **One unstaged cut.** Remove only fallout created by that cut while
   preserving correct proof, pre-existing dead work, unrelated work, the
   index, trackers, installed state, and external state.
6. **After proof and net reduction.** Rerun the same focused seam, widen
   checks proportionately, and establish a strict reduction in maintenance
   obligations. Counts are receipts, not correctness or productivity proof.
7. **Finite serial campaign.** Enter only for an explicit `until-clean`
   request in one named region with a finite successful-cut budget, one
   invariant contract and seam, and a monotonic obligation ledger.
8. **Evidence-bearing Return and completion.** Reconcile proof, obligation
   reduction, paths, work state, residuals, and the selected terminal outcome;
   return the result unstaged.

The irreversible order is:

```text
Admit -> Trace -> Baseline -> Choose -> Cut -> Prove -> Lock
```

The promoted C1 adds exactly two behavior-proven units to B0:

- **C1-01 ordered selection:** inspect `Delete -> Reuse -> Standardize,
  native-first -> Collapse -> Shrink`; the first admissible rung wins.
- **C1-04 finite campaign completion:** use exactly three successful cuts when
  the user omits a budget and classify the first applicable terminal as
  `Clean`, `Budget exhausted`, `Diminishing return`, `Oscillation`,
  `Failed cut`, or `Boundary stop`.

## Source And Decision Basis

The source-first checkpoint was frozen before the previous canonical runtime
or synthesis conclusions were opened:

```text
checkpoint SHA-256:
76300e21e94700b0a702be25a1f0a36071188380da3e51ef814152b6239028e8

intent manifest SHA-256:
ee19da0dc1117e4b096f0de7c53fa7ec819a440c52f4472412f760065ddc62a8

source manifest SHA-256:
3477ae076ceef1f527e9c1162da2172ead4f07603582ecdd9c2353d35e16bd74
```

| Source | Exact identity | Accepted pressure and limit |
| --- | --- | --- |
| Matt Pocock Skills | `ed37663cc5fbef691ddfecd080dff42f7e7e350d` | Bounded engineering and proof vocabulary only; no direct simplification executor or efficacy claim. |
| Superpowers | `d884ae04edebef577e82ff7c4e143debd0bbec99` | Before/after verification pressure only; it does not set the local runtime contract. |
| Ponytail | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b` | Ordered elimination, reuse, native capability, deletion, and safety floors; persistent modes, scoring, volume pressure, and wholesale package behavior were not adopted. |
| Local intent authorities | Intent manifest above | Invocation, outcome, authority, mutation, Return, completion, routes, and protected safety behavior. |
| Previous canonical runtime | Tree `030c31bf4f880f1d0c66005482ff6aa7b4382bd301dd491563491fd195964054` | Compatibility inventory and C1 origins only; presence did not establish protection or efficacy. |

No network refresh was performed. These identities describe the inspected
local revisions, not later remote state.

## Candidate Decisions

| Unit | Origin | Registered B0 failure | Decision and promoted effect |
| --- | --- | --- | --- |
| `C1-01` ordered selection | source mechanism | A later local move can beat an admissible deletion or existing owner. | `accepted`; B0 complied 3/5 with two later-rung choices, while C1 complied 5/5 with one observed choice. |
| `C1-02` characterization support | current retention | B0 might refuse a cut despite an independent observable oracle. | `rejected-no-control-failure`; B0 licensed the valid oracle and refused the wrong condition 10/10. |
| `C1-03` exact index identity wording | current retention and safety | B0 might accept equal status shape despite changed staged bytes. | `rejected-no-control-failure`; B0 refused equal-status drift and inadequate late snapshots 10/10. The work-state outcome remains protected. |
| `C1-04` default budget and terminals | intent counterexample | Omitted budget and terminal distinctions vary or permit unbounded continuation. | `accepted`; B0 failed the omitted-budget claim 5/5, while C1 used default three and all six terminals correctly 5/5. |
| `C1-05` attempt-owned recovery | intent counterexample | Failure recovery might overwrite pre-existing or concurrent work. | `rejected-no-control-failure`; B0 handled the isolated and refusal cases 25/25. The non-destructive outcome remains protected. |

Prompt 4 also removed an unproven B0 sentence preferring source-supported
deletion or an already-sufficient owner/native capability: D0 and rebuilt B0
both selected deletion 5/5, with no variance benefit. The independently
required coherence, proof, safety, strict-reduction, and work-state gates
remain.

The Pruning Pass classified every instruction-bearing passage exactly once.
No passage qualified for collapse, disclosure, or deletion without removing
protected meaning or changing exact accepted behavior. Its disposition was
`pruning-not-needed`.

## Relationships And Ownership

| Caller or owner | Relationship | Trigger and Return |
| --- | --- | --- |
| Human | Invoke | Explicitly names Simplify Code and a bounded target; names `until-clean` and optionally a finite budget for campaign mode; receives an unstaged result. |
| `$skill-router` | Recommend and stop | Selects one bounded behavior-preserving simplification. |
| `$tdd` | Recommend and stop | Settled GREEN work exposes separate bounded cleanup. |
| `$improve-codebase` | Recommend and stop | A verified `Eliminate` candidate is selected; Simplify Code returns stale, absorbed, or incomplete reports unchanged. |
| Simplify Code | Recommend and stop | Wide discovery or multi-region sequencing goes to Improve Codebase. |
| Simplify Code | Recommend and stop | A new interface, dependency direction, proof seam, or ownership decision goes to Codebase Design. |
| Simplify Code | Return and stop | Uncertain bug facts go to Diagnosing Bugs; feature, public-contract, review, Git, tracker, installation, and external work return to their owners. |

Relationship delta is none. The provider interface and explicit-only policy
also remain byte-identical to the previous canonical package, B0, D0, and C1.

## Exact Proof

The accepted behavior record is
[2026-07-23-simplify-code-behavior-eval.md](../../validation/transcripts/2026-07-23-simplify-code-behavior-eval.md).
It owns the fixed protocol, raw-output pointers, sample judgments, variance,
worst results, deviations, and telemetry limits. The pruning record is
[2026-07-23-simplify-code-pruning.md](../../validation/transcripts/2026-07-23-simplify-code-pruning.md).

Exact identities:

| Package | Tree SHA-256 | Role |
| --- | --- | --- |
| Previous canonical | `030c31bf4f880f1d0c66005482ff6aa7b4382bd301dd491563491fd195964054` | Compatibility inventory |
| Final B0 and D0 | `54aac31397e2a5ab10daf78420906a24459622f144631e0c61e8e02888acd434` | Viable minimum and no-guidance control |
| Promoted canonical C1 | `f3fa29e016e1ad88f77088e7b001f80db4a139b51d7da2125146fdda5c8cef06` | Accepted final runtime |

Five fresh integrated C1 samples passed all protected B0 families, ordered
selection, default and explicit budgets, all six terminals, work-state and
dependency boundaries, and explicit-only invocation. Aggregate: 5/5; zero
outcome variance; worst result passed; zero protected-behavior regressions or
critical failures.

This lane used read-only synthetic action decisions. It does not prove live
source mutation, real concurrent interleaving, arbitrary tasks or hosts, or
later model/runtime builds.

## Deliberate Non-Changes And Residuals

Rejected for this campaign: automation, numeric scoring, source or candidate
catalogs, parallel cuts, whole-tree cleanup, persistent debt tracking,
automatic downstream execution, dependency addition, Git delivery, tracker
mutation, and external mutation.

Deferred pending a later source-first admission and exact failure:

- a ceiling-and-revisit comment rule;
- disclosure of campaign behavior into `UNTIL-CLEAN.md`; and
- a larger structured Return.

Deliberately preserved: explicit-only and unstaged operation; caller-facing
before/after proof; commitment and safety floors; report pickup and owner
routes; finite serial campaigning with a monotonic ledger; index and unrelated
work safety; first-class no-safe completion; dependency no-addition; and
repository-wide non-use evidence plus manifest, lock, and repository-owned
installation proof before dependency removal.

Residual gaps are live filesystem mutation and concurrent-interleaving proof,
generalization beyond the fixed packets and worker runtime, upstream remote
freshness, and unavailable backend model, reasoning, token, latency, and host
invocation telemetry.

## Lifecycle

| Unit | Current epoch state |
| --- | --- |
| Prompt 1 | Passed; source-first checkpoint frozen. |
| Prompt 2 | Passed; decision-complete synthesis recorded. |
| Prompt 3 | Passed; B0, D0, and C1 constructed with exact identities. |
| Prompt 4 | Accepted; B0 viable, `C1-01` and `C1-04` accepted, three hypotheses rejected without control failure. |
| Pruning Pass | Complete; `pruning-not-needed`; exact C1 retained byte-identically. |
| Prompt 5 canonical phase | Passed; exact C1 promoted and canonical proof completed. |
| Prompt 5 installation phase | Recorded in the promotion/install transcript after managed parity proof. |
| Git delivery | Bare mode; pending and outside Prompt 5. |
