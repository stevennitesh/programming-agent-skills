# Operational decisions

For every admitted cut, keep the order `Admit -> Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`. Use one caller-facing proof seam before and after the cut, require a strict net reduction in maintenance obligations, leave the result unstaged, preserve the index and unrelated work, and name the owner of every residual.

## B0 Omnibus

### 1. Admission and routing

- Admit `parser.py`. The still-valid verified Improve Codebase candidate has precedence over the separately user-named `cache.py` and the coherent current diff in `cli.py`.
- Return a stale report to Improve Codebase unchanged.
- With no bounded target, recommend `$improve-codebase` and stop.
- Return a broad survey to `$improve-codebase`; do not widen discovery inside Simplify Code.
- Return an uncertain failing symptom to `$diagnosing-bugs`.
- Return a new interface decision to `$codebase-design`.
- Return feature work to its feature owner.
- Return staging and committing to the Git-delivery owner. Do not stage or commit the simplification result.

The user retains authority over target, mode, budget, and commitment decisions. Simplify Code owns selection, local edits, proof, and Return only within the admitted region.

### 2. Failing starting proof

Do not edit. The exact starting caller-facing test fails, so the baseline cannot authorize production mutation. Return **No safe simplification** for the bounded branch-deletion candidate, identify the failing baseline as the proof gap, report unchanged work and index state, and assign the proof or behavior discrepancy to its owning code or test owner.

### 3. Shorter code below preservation floors

Do not make the rewrite. Removing trust-boundary validation, changing timeout ordering, and dropping an accessibility label changes protected commitments. Line-count reduction does not authorize the cut. Return **No safe simplification**, account for the rejected rewrite and each preserved commitment, report the unchanged state and proof boundary, and leave any commitment change with its respective security/trust-boundary, behavior/timing, or accessibility owner.

### 4. Bounded helper deletion

Delete the proved-safe helper in `src/a.py` and remove only the import newly stranded by that deletion in `src/a.py`. Run the same caller-facing proof before and after, then the nearest relevant checks, and confirm that the helper and import removal is a strict net obligation reduction.

Leave `notes.md` untouched and dirty, leave `scratch.tmp` untouched and untracked, and leave staged `logo.bin` exactly staged. Keep the simplification unstaged. Do not remove pre-existing dead work or any fallout not created by this cut. The residual owner for those unrelated items remains their existing work owner.

### 5. Finite `until-clean` budgets

For each cut, run the complete serial gate `Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`; never parallelize the region. After each successful Lock, record obligations removed and introduced, require a strict monotonic net reduction, decrement the successful-cut budget, and use the proved result as the next starting state. A failed attempt consumes no successful-cut budget. The formatting-only rewrite is not a progress unit and cannot enter the successful-cut ledger.

- With budget `1`, make at most one eligible successful cut. After its Lock, the budget is zero: stop as **Budget exhausted**, with one ledger entry, three eligible cuts reported as residuals, and the formatting-only rewrite reported as rejected. Their owner remains the named region's owner.
- With budget `3`, make at most three eligible successful cuts serially. After the third Lock, stop as **Budget exhausted**, with three ledger entries, the fourth eligible cut reported as the residual, and the formatting-only rewrite reported as rejected. Its owner remains the named region's owner.

Do not renew either budget or continue merely because another eligible cut exists.

### 6. Required Return

For a successful cut, return:

- mode and admitted region;
- the selected cut;
- the removed and introduced obligations and strict net reduction;
- preserved contract and observable caller-facing seam;
- exact before and after proof, plus nearest relevant checks and any skipped proof or risk;
- changed paths;
- starting and ending ref, status, relevant diff, staged-state shape, index state, unrelated-state preservation, and confirmation that the result is unstaged;
- rejected or deferred candidates, exact stop reason, residuals, and each residual owner.

For a campaign stop, return all of the above plus the initial finite budget, remaining successful-cut budget, ordered serial ledger for every successful Lock, failed-attempt accounting, the first applicable one of the six terminal classifications, truthful eligible and ineligible residuals, and their owners.

For a no-safe region with inadequate proof, return:

- mode and bounded region;
- **No safe simplification**;
- every credible candidate and its rejection reason;
- preserved contract and intended observable seam;
- the exact baseline or proof gap and any skipped proof or risk;
- no production changed paths;
- unchanged starting and ending work state, index, staged shape, and unrelated state;
- exact stop reason and the owner responsible for resolving the proof gap or remaining behavior decision.

### 7. Dependencies

- Do not add the new package. Reducing 20 lines to 2 does not override the no-new-dependency boundary. Leave the candidate with the admitted region's implementation owner or return any required dependency commitment to its owner.
- Do not remove the installed package while runtime-entry evidence is incomplete. Repository-wide source, configuration, and runtime-entry evidence must establish no remaining use before removal, followed by manifest, lockfile, and repository-owned installation proof reconciliation. Until then, return **No safe simplification** for that candidate, name the incomplete runtime-entry search as the proof gap, preserve installed and work state, and assign the evidence gap to the package/runtime owner.

### 8. Invocation

- `Use Simplify Code on src/a.py` is an explicit invocation. Admit `src/a.py` as the user-named bounded target, subject to the remaining gates.
- `Could you tidy this code?` does not invoke Simplify Code. Its policy disallows implicit invocation; make no Simplify Code mutation and leave routing or target selection with the requester.

## C1-01 Neutral B0 Control

Select the deletion of the expired branch proven unreachable, then stop after that one coherent cut.

The active package supplies an explicit selection order: Delete, Reuse an existing project owner, Standardize native-first, Collapse, then Shrink. The deletion is admissible and therefore wins at the first rung; the presentation order of the five options does not control selection. Record the other four independently safe options as deferred candidates, not additional cuts. Preserve the shared fixture as the caller-facing before/after proof, verify the strict net obligation reduction, keep the change inside the bounded target and unstaged, and leave the deferred candidates with the bounded target's owner.

## C1-04 Campaign Budget And Terminals

The omitted numeric budget defaults to exactly `3` successful cuts. Run three eligible cuts serially through `Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`, recording removed and introduced obligations after each Lock and decrementing only after a successful Lock. With the fourth eligible cut still available and zero budget remaining, stop as **Budget exhausted**. Report the fourth cut as an eligible residual owned by the named region's owner. Do not renew the budget.

A proof-failing attempt consumes no successful-cut budget in any campaign case. Preserve the current proved state, index, unrelated work, and unstaged boundary after an unsuccessful attempt.

The independent terminal cases are:

- **Clean:** A complete five-rung inspection finds no admissible cut. Make no further mutation, report no eligible simplification residual, and leave any non-simplification work with its existing owner.
- **Budget exhausted:** Zero successful-cut budget remains while eligible cuts remain. Stop without attempting them, report each eligible residual and its region owner, and do not renew the budget.
- **Diminishing return:** Only a formatting or presentation change remains. Do not count or make it as campaign progress; report it as an ineligible residual owned by the region owner and stop.
- **Oscillation:** The next move recreates, undoes, or exchanges an earlier obligation for an equivalent one. Do not make it; identify the corresponding earlier ledger obligation, report the oscillating candidate as a residual owned by the region owner, and stop.
- **Failed cut:** An attempted cut fails its after-proof. It consumes no successful-cut budget. Preserve the current proved state, report the exact failed proof and work state, and assign the failed candidate or proof discrepancy to the owning code or test owner.
- **Boundary stop:** Drift, proof limits, region limits, or foreign ownership prevents the next cut. Do not widen the region or cross ownership. Report the exact boundary, the blocked candidate as a residual, and the foreign or proof-boundary owner.
- With an explicit budget of `2`, make at most two eligible successful cuts serially. After the second Lock, zero budget remains, so stop as **Budget exhausted** and report the two still-eligible cuts as residuals owned by the named region's owner. Failed attempts before either successful Lock do not decrement the budget.

Every campaign Return includes the named mode and region, preserved invariant contract and caller-facing seam, before/after proof for each successful cut, changed paths, starting and ending work state, index and unrelated-state preservation, the unstaged result, initial and remaining budget, ordered successful-cut ledger, failed-attempt accounting, rejected or deferred candidates, exact terminal classification, truthful residuals and owners, and skipped proof or risk.
