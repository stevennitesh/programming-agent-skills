# B0 Omnibus - Simplify Code Decisions

All decisions below are read-only. No production file, index entry, tracker,
installed package, or external state is mutated.

1. **Target admission and Returns.** Admit `parser.py`: the still-valid verified
   Improve Codebase candidate outranks the separately user-named `cache.py`,
   which outranks the coherent `cli.py` diff. Authority is limited to selecting,
   locally simplifying, proving, and returning one cut in `parser.py`; the user
   retains target, mode, budget, and commitment authority. Before any authorized
   cut, trace its callers and commitments, capture ref/status/diff/index shape,
   and pass the smallest caller-facing baseline; afterward rerun that proof and
   relevant checks and require a strict net obligation reduction. Mutation here:
   none. Any later cut must remain unstaged and preserve unrelated state.
   Return a stale report unchanged to Improve Codebase; with no bounded target,
   recommend Improve Codebase and stop; return a broad survey to Improve
   Codebase, an uncertain failing symptom to Diagnosing Bugs, a new-interface
   decision to Codebase Design, feature work to its feature owner, and
   stage/commit work to Git delivery. Completion requires the admitted region,
   proof, candidate accounting, work state, changed paths, residuals, and
   outcome to agree. Invocation classification: only an explicit Simplify Code
   invocation is admitted.

2. **Red baseline.** Do not delete the branch. The exact starting
   caller-facing test fails, so no production mutation is authorized even if
   the candidate is bounded. Mutation and staged-state change: none. Return
   **No safe simplification** for the named region with the failing before
   proof as the exact gap, preserved contract/seam, starting and ending work
   state, zero changed paths, candidate rejection, skipped after-proof, risk,
   and the proof/defect owner as residual owner. Completion is the fully
   accounted no-safe result, not an edit. Invocation classification: explicit
   invocation may run this decision but cannot override the proof gate.

3. **Behavior floors beat line count.** Reject the rewrite. Removing
   trust-boundary validation, changing timeout ordering, and dropping an
   accessibility label each violate preserved commitments; four lines is only
   a count, not proof of simplification. Authority permits no such tradeoff.
   Mutation and work-state change: none. Return **No safe simplification** with
   all three rejection reasons, the caller-facing proof needed before and
   after any alternative, no net reduction claim, unchanged paths/state, and
   the respective security/product/accessibility commitment owners as
   residuals. Completion requires those candidates to remain rejected.
   Invocation classification: explicit invocation does not authorize contract
   changes.

4. **Bounded helper cut.** The only authorized mutation is deletion of the
   proved-safe helper in `src/a.py` plus its newly stranded import in that same
   file. First record the exact state and pass the caller-facing baseline; then
   make the cut, rerun the same proof and nearby checks, and establish strict
   net obligation reduction. Do not touch pre-existing `notes.md`,
   `scratch.tmp`, or staged `logo.bin`; do not stage the cut. Mutation here:
   none because this is a read-only decision. Return the preserved contract
   and seam, before/after proof, `src/a.py` as the sole changed path, obligation
   reduction, starting/ending state, rejected/deferred candidates, stop
   reason, residual owner, and risks. Complete only if the index and unrelated
   dirty/untracked state exactly retain their starting shape. Invocation
   classification: actionable only under explicit invocation.

5. **Finite `until-clean` campaigns.** Authority exists because the request
   explicitly names `src/parser/` and supplies positive budgets; it does not
   extend outside that region or permit budget renewal. Hold one behavior
   contract and caller-facing seam, then run serially for each cut:
   `Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`. Each successful Lock
   records removed and introduced obligations, requires a strict monotonic net
   reduction, preserves unstaged/unrelated state, decrements the budget, and
   makes the proved result the next starting state. With budget **1**, perform
   at most one eligible cut and stop on budget exhaustion even though three
   eligible cuts remain. With budget **3**, perform at most three eligible cuts
   and stop on budget exhaustion even though one remains. The formatting-only
   rewrite never counts as progress or consumes a successful-cut slot. Earlier
   proof failure, drift, oscillation, no admissible cut, or foreign boundary
   stops either campaign immediately. Mutation here: none. Return mode, region,
   initial/final state, per-cut before/after proof and ledger, remaining budget,
   terminal reason, deferred cuts, changed paths, preserved index, risks, and
   the owner of each residual. Completion additionally requires the finite
   budget, serial ledger, and terminal reason to agree. Invocation
   classification: explicit `until-clean`; ordinary simplification authority
   is insufficient.

6. **Required Returns.** For a successful cut, return mode/region, the cut,
   strict net obligation reduction, preserved contract and observable seam,
   before/after proof, changed paths, starting/ending work and index state,
   rejected/deferred candidates, exact stop reason, residual owner, and skipped
   proof/risk; confirm it remains unstaged. For a campaign stop, add the initial
   finite budget, remaining budget, serial successful-cut ledger, per-cut
   proof, and truthful terminal reason. For inadequate proof, return **No safe
   simplification**, the bounded region and candidates, rejection reasons,
   exact proof gap, unchanged paths/state, no reduction claim, and the owner of
   the proof residual. Mutation here: none. Completion occurs only when every
   returned fact agrees with current evidence; inadequate proof completes only
   the no-safe outcome. Invocation classification follows the requested mode:
   explicit one-cut or explicit finite `until-clean`.

7. **Dependencies.** Reject adding the new package: Simplify Code has no
   authority to add a dependency merely to reduce 20 lines to 2, and transferred
   dependency/operational burden defeats a demonstrated strict net reduction.
   Also do not remove the apparently unused installed package: incomplete
   runtime-entry evidence cannot prove repository-wide nonuse. Mutation to
   source, manifest, lockfile, installed state, index, and external state:
   none. Return **No safe simplification** for both candidates with the
   caller-facing baseline/after-proof requirements, dependency and runtime
   evidence gaps, unchanged work state and paths, rejection reasons, risks,
   and dependency/runtime owners as residuals. Completion requires both
   rejections to be accounted; removal becomes eligible only after complete
   source, configuration, and runtime-entry proof and would then require
   manifest, lockfile, and repository-owned installation proof reconciliation.
   Invocation classification: explicit invocation can assess but cannot relax
   dependency rules.

8. **Invocation classification.** "Use Simplify Code on `src/a.py`" is an
   explicit invocation with a user-named bounded target; it authorizes the
   read-only admit/trace/baseline decision and, only after a green credible
   baseline, one bounded unstaged behavior-preserving cut plus proof and Return.
   "Could you tidy this code?" is an ordinary implicit request and must not
   invoke Simplify Code because implicit invocation is disabled; no tracing,
   proof run, or mutation is authorized under this skill. Mutation here: none.
   In the explicit case, completion still requires strict net reduction,
   caller-facing before/after proof, exact work-state preservation, changed
   paths, residual ownership, and the full Return. In the implicit case, return
   the invocation boundary and leave ownership with the ordinary request
   handler until the user explicitly invokes the skill.
