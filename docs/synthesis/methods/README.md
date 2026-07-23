# Synthesis Methods

Methods are reusable ways to distill sources or deploy selected synthesis.

Use this folder for process docs that apply across multiple skills or skill
families.

## Files

| File | Role |
| --- | --- |
| [`deploy-prompts.md`](deploy-prompts.md) | One-skill campaign controller and bounded numbered units for synthesizing a locally intended, source-derived executable minimum, evaluating an exact candidate, promoting and installing it, and optionally delivering it through Git. |
| [`source-distillation-flow.md`](source-distillation-flow.md) | Optional flow for distilling primary and outside sources into important concepts and usable techniques. |
| [`prompts/`](prompts/) | Optional prompts supporting source distillation. |

## Routing

Use `Run Deploy Campaign on <skill>` for one initiating prompt and a fresh
Prompts 1-5 campaign epoch, including no-op promotion and installation-parity
verification when the accepted bytes are already canonical, or invoke Deploy
Prompt 1 for one manual unit. A prior campaign may supply exact reusable
artifacts and proof but cannot skip a numbered unit. The campaign root retains
transitions, verification, and user interaction; fresh-context unit owners
stop after one unit, writers are serialized, and nested workers are limited to
independent source or evaluation evidence. Bare invocation excludes Git
delivery; append `and commit` or `and push` to authorize Prompt 6.

Every path begins with Prompt 1. Its blind intent-and-evidence pass settles the
minimum local intended contract, extracts credible source mechanics, and
freezes `B0` from their intersection before opening current runtime or
synthesis conclusions. Re-entry verifies the checkpoint and revisits only
affected semantic units. Prompt 2 reconciles that skill's synthesis in place;
no pack-wide migration is required.

Route by exact campaign shape: current = B0 = C1 is
`runtime-no-change`; current != B0 = C1 is `pruning-only`; and B0 != C1 is a
`behavioral-candidate`. Classify prior evidence as exact-reusable,
lane-limited, historical-admission-only, invalidated, or missing. Pruning is a
non-regression lane and never receives mechanism-contribution credit. Exact
byte identity does not waive missing B0 proof. Inside a campaign, Prompts 3 and
4 always run; exact unchanged proof is revalidated and reused rather than
resampled.

Current runtime is an inventory and evidence source, never B0 by existence.
C1 hypotheses may originate from current retention, one concrete pack
composition gap, a credible source mechanism beyond minimum viability, or a
counterexample to settled intent. Origin triggers inspection; every admitted
hypothesis still needs an owner, expected B0 failure, cheapest expression,
wrong-condition case, and proof. A counterexample that disproves minimum
viability reopens B0 instead of becoming C1.

B0 must pass its minimum-runtime suite before C1 evaluation. Compare unproved
source steering against `D0` no-guidance and reuse the matching B0 viability
arm; independently required contracts use owner-matched proof unless efficacy
is claimed.

Use the Conditional Research Interlude only when Prompt 1 admits one exact
decision-changing source gap. Source distillation returns one evidence packet
and stops before behavior design, runtime authoring, or deployment; rerun
Prompt 1 against the unchanged checkpoint to apply only that delta. Behavioral
uncertainty waits for exact candidate bytes and candidate-owned evaluation.
Prefer relevant, verifiably acclaimed, highly rated, or widely adopted sources
that model upper-bound engineering discipline, but treat those signals as
discovery priorities rather than evidence of correctness or local fit.

Use the Conditional Behavior Decision Interlude only when Prompt 1 admits one
exact intended-contract decision: a fuzzy minimum-viability axis or a C1
hypothesis that would alter outcome, invocation, authority, Return, completion,
exclusion, or relationships. It never selects agent technique or proves
efficacy.

Use the Conditional Prototype Interlude only for one agent-owned technical
choice blocking executable B0 or C1. Its disposable runnable probe may select a
construction but is not skill-wording, production, or behavioral-effect proof.

Every leaf prompt performs one unit, recommends at most one successor, and
stops. Only an active Deploy Campaign coordinator may dispatch the verified
successor. Use the proportionate proof budget in
[`deploy-prompts.md`](deploy-prompts.md): do not run a full suite at every
documentation or construction step. Prompts 1 through 5 preserve Git HEAD and
never stage or commit; optional Prompt 6 is the sole Git-delivery owner. Load
the shared sections plus the controller or named unit, not every prompt body.

## Boundary

- Put reusable synthesis methods here.
- Put per-skill design judgment in `../skills/`.
- Put source research in `../../research/`.
- Put behavior evidence in `../../validation/`.
