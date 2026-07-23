# B0 Omnibus — Operational Decisions

All cases are executed as read-only decisions. The irreversible order is
`Admit -> Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`; no described
cut is actually applied here.

1. **Target precedence and returns.** **Authority:** Admit `parser.py`, because
   the still-valid verified Improve Codebase candidate outranks the separately
   user-named `cache.py` and the coherent `cli.py` diff. The user supplies
   target/mode/budget/commitment authority; Simplify Code selects and proves
   only within the admitted target. **Proof:** trace `parser.py` callers,
   commitments, work state, and a caller-facing seam; require a passing exact
   baseline and the same after-proof plus relevant checks and strict net
   obligation reduction. **Mutation/state:** none in this decision; any
   authorized cut would be bounded, unstaged, and preserve the index and
   unrelated state. **Return/completion:** return a stale or incomplete report
   unchanged to Improve Codebase; for no bounded target, recommend Improve
   Codebase and stop; return a broad survey to Improve Codebase, an uncertain
   failing symptom to Diagnosing Bugs, a new interface decision to Codebase
   Design, a feature to its feature owner, and staging/commit to Git delivery.
   Completion requires current evidence for the admitted region and all
   accounting fields. **Invocation:** explicit, read-only Simplify Code
   decision.

2. **Failing starting proof.** **Authority:** the bounded branch is admissible,
   but the baseline gate controls mutation. **Proof:** the caller-facing test
   fails against the exact starting state, so it cannot authorize a behavior-
   preserving cut. **Mutation/state:** do not edit; preserve the worktree,
   index, unrelated files, installed state, and external state exactly.
   **Return/completion:** return **No safe simplification**, naming the branch
   region, candidate, failing baseline and exact proof gap, starting/ending
   state, skipped after-proof, and the test/behavior owner as residual owner;
   this is complete only when that no-safe accounting agrees with current
   evidence. **Invocation:** explicit, read-only Simplify Code decision.

3. **Shorter but behavior-changing rewrite.** **Authority:** line-count
   reduction cannot override trust-boundary, ordering/timing, or accessibility
   commitments. **Proof:** the proposed observable behavior differs at the
   caller-facing seam; therefore it cannot pass the same before/after proof or
   establish a valid net reduction. **Mutation/state:** reject all four lines;
   no mutation and no state change. **Return/completion:** return **No safe
   simplification** with all three rejected changes, preserved commitments,
   work state, proof mismatch, and the respective security/domain,
   timing/behavior, and accessibility owners as residual owners. **Invocation:**
   explicit, read-only Simplify Code decision.

4. **Bounded helper fallout.** **Authority:** only the proved helper deletion in
   `src/a.py` and fallout newly created by that deletion are in scope.
   **Proof:** retain the passing exact caller-facing baseline, rerun the same
   proof after the proposed deletion, then relevant tests/checks, and confirm a
   strict net obligation reduction. **Mutation/state:** the authorized
   hypothetical cut deletes the helper and its newly stranded import in
   `src/a.py`; this decision applies neither. It must remain unstaged, leave
   dirty `notes.md` and untracked `scratch.tmp` untouched, and preserve staged
   `logo.bin` and the index exactly. **Return/completion:** report the cut,
   removed helper/import obligations, no introduced burden, proof before/after,
   changed path `src/a.py`, identical unrelated/index state, rejected/deferred
   candidates, and any residual owned by the `src/a.py` maintainer; complete
   only after Lock verifies every item. **Invocation:** explicit, read-only
   Simplify Code decision.

5. **Finite `until-clean` campaigns.** **Authority:** the user explicitly names
   `src/parser/` and finite positive successful-cut budgets, so the campaign is
   admitted only within that region and invariant behavior contract.
   **Proof:** run `Trace -> Baseline -> Choose -> Cut -> Prove -> Lock` serially
   for one cut at a time, using the same caller-facing seam; each proved result
   becomes the next starting state. **Mutation/state:** none here; in execution
   every cut is unstaged and preserves the index/unrelated state. The ledger
   records removed and introduced obligations after each Lock and must show
   strict monotonic reduction; formatting-only work never counts. With budget
   1, Lock one eligible cut, decrement to zero, and stop with three eligible
   cuts residual. With budget 3, Lock three eligible cuts serially, decrement
   after each, and stop at zero with one eligible cut residual. Never widen,
   parallelize, renew the budget, or consume a slot for formatting. Stop
   earlier on no admissible cut, proof failure, drift, oscillation, or a foreign
   boundary. **Return/completion:** return region/mode, original and remaining
   budget, serial ledger, proofs, state, changed paths, exact stop reason, and
   remaining `src/parser/` maintainer-owned candidates/risks. Completion also
   requires truthful campaign termination. **Invocation:** explicit
   `until-clean`, handled here read-only.

6. **Required Returns.** **Authority:** Return may claim only evidence inside
   the admitted region and selected mode. **Proof:** every successful result
   names the same caller-facing before/after proof; inadequate proof is an
   explicit gap, never inferred success. **Mutation/state:** none here; all
   successful-cut paths would be unstaged, with starting/ending work state,
   index preservation, unrelated-state preservation, and changed paths stated.
   **Return/completion:** a successful cut returns mode/region, cut, strict net
   obligation reduction, preserved contract/seam, before/after proof, changed
   paths, both work states, rejected/deferred candidates, stop reason,
   maintainer-owned residuals, and skipped proof/risk. A campaign stop adds
   finite budget, remaining budget, serial successful-cut ledger, and exact
   terminal reason. A proof-inadequate region returns **No safe
   simplification**, credible candidates and rejection reasons, exact proof
   gap, unchanged states/paths, risk, stop reason, and the proof/behavior owner.
   Complete only when all returned facts agree with current evidence.
   **Invocation:** explicit, read-only Simplify Code decision.

7. **Dependencies.** **Authority:** Simplify Code may not add a dependency, and
   may remove one only after repository-wide source, configuration, and
   runtime-entry evidence proves no use. **Proof:** reducing 20 lines to 2 does
   not justify the new package; the installed package lacks complete
   runtime-entry proof, so non-use is unproved. **Mutation/state:** neither add
   the new package nor remove/reconcile the installed one; leave manifests,
   lockfiles, repository-owned installation proof, installed state, worktree,
   and index unchanged. **Return/completion:** return **No safe
   simplification** for both candidates, with rejection reasons, proof gaps,
   unchanged state, and dependency/runtime-entry owners as residual owners;
   completion is the fully accounted no-safe result. **Invocation:** explicit,
   read-only Simplify Code decision.

8. **Invocation classification.** **Authority:** `allow_implicit_invocation` is
   false. “Use Simplify Code on `src/a.py`” is an explicit invocation with a
   user-named bounded target; “Could you tidy this code?” is ordinary implicit
   wording and does not invoke the skill. **Proof:** for the explicit request,
   trace the named region and require the exact caller-facing baseline and
   after-proof plus strict net reduction; for the implicit request, run no
   Simplify Code gates or proof. **Mutation/state:** none in either read-only
   decision; no unstaged patch, index change, or external change. **Return/
   completion:** the explicit case may complete only with a fully accounted
   cut or **No safe simplification** result and named `src/a.py` residual owner;
   the implicit case stops without claiming Simplify Code completion and
   leaves ownership with the requester until they explicitly invoke it and
   bound the target. **Invocation:** first explicit/admitted; second
   implicit/not invoked.
