# Operational decisions

## B0 Omnibus

### 1. Admission and Return boundaries

Admit `parser.py`: the still-valid verified Improve Codebase candidate has
precedence over the separately user-named `cache.py` and the coherent current
diff in `cli.py`. The user retains authority over target, mode, budget, and
commitment decisions; Simplify Code selects, edits, proves, and Returns only
inside the admitted target.

- Return a stale report to Improve Codebase unchanged.
- With no bounded target, recommend Improve Codebase and stop.
- Return a broad survey to Improve Codebase.
- Return an uncertain failing symptom to Diagnosing Bugs.
- Return a new interface decision to Codebase Design.
- Return feature work to its feature owner.
- Return staging and committing to the Git-delivery owner.

No returned case authorizes mutation, staging, or external-state changes.

### 2. Failing starting proof

Do not edit. The exact starting caller-facing test fails, so the baseline
cannot authorize production mutation. Return **No safe simplification** for
the bounded branch with the failing proof as the exact proof gap, the unchanged
work state, and the branch or test owner as the named residual owner.

### 3. Preservation floors

Reject the four-line rewrite. Removing trust-boundary validation, changing
timeout ordering, and dropping an accessibility label each violates a
preserved commitment. Reduced line count cannot authorize the cut; the
security/trust-boundary, timing/ordering, and accessibility owners retain the
residuals.

### 4. Bounded mutation and work state

Delete the proved-safe helper in `src/a.py` and remove only the import newly
stranded by that deletion. Leave both changes unstaged. Preserve the unrelated
dirty `notes.md`, untracked `scratch.tmp`, and staged `logo.bin` exactly as
found, including exact index identity. Do not remove pre-existing dead work or
touch any other path. Rerun the same caller-facing proof and the nearest
relevant checks, then confirm a strict net reduction in maintenance
obligations.

### 5. Finite campaigns

For either budget, hold one behavior contract and caller-facing seam and run
each cut serially through:

`Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`

After each successful Lock, record removed and introduced obligations, require
a strict monotonic net reduction, decrement the successful-cut budget, and use
the proved result as the next starting state. A failed attempt consumes no
successful-cut budget. The formatting-only rewrite is not a progress unit.

- Budget `1`: permit one successful cut, then stop as **Budget exhausted**.
  Report the other three eligible cuts as residuals owned by the named region
  and reject the formatting-only rewrite.
- Budget `3`: permit three serial successful cuts, then stop as **Budget
  exhausted**. Report the fourth eligible cut as the residual owned by the
  named region and reject the formatting-only rewrite.

Do not widen or parallelize the region, renew either budget, stage the work, or
continue past the applicable terminal.

### 6. Required Returns

A successful-cut Return states the mode and admitted region; the selected
unstaged cut; removed and introduced obligations and the strict net reduction;
the preserved contract and observable caller-facing seam; exact before and
after proof; changed paths; starting and ending work state; rejected or
deferred candidates; stop reason; named residual owner; and every skipped
proof or remaining risk. It also confirms preservation of the index and
unrelated state.

A campaign-stop Return additionally states the initial and remaining finite
successful-cut budget, the ordered successful-cut ledger, failed attempts that
consumed no budget, the first applicable terminal classification, eligible or
otherwise remaining residuals and their owner, and that the result remains
unstaged.

A no-safe Return states the bounded region; **No safe simplification**; every
credible candidate and its rejection reason; the preserved contract and
intended proof seam; the inadequate baseline or other exact proof gap; starting
and unchanged ending work state; no changed paths; index and unrelated-state
preservation; the exact stop reason; skipped proof or risk; and the owner of
the proof or code residual.

### 7. Dependencies

Do not add the new package; shortening 20 lines to 2 does not override the
no-new-dependency boundary. Do not remove the apparently unused installed
package while runtime-entry evidence is incomplete. Its removal requires
repository-wide source, configuration, and runtime-entry proof, followed by
manifest, lockfile, and repository-owned installation-proof reconciliation.
Return the incomplete runtime-entry search to the package/runtime owner as the
named residual.

### 8. Invocation

“Use Simplify Code on `src/a.py`” is an explicit invocation with a bounded
user-named target and may enter admission. “Could you tidy this code?” is an
ordinary implicit request; Simplify Code does not invoke, mutate, or stage from
it.

## C1-01 Neutral B0 Control

Select the expired branch proven unreachable and delete it as the one coherent
cut. It is the first admissible **Delete** move in the package's stated
five-rung inspection, even though it appears last in the packet's presentation
order. The passing caller-facing fixture supplies the before/after observable
seam; the cut still requires an unstaged bounded mutation, after-proof, Lock,
and confirmation of strict net obligation reduction. Stop after this cut.
Defer the project-owned reuse, runtime-native standardization, abstraction
collapse, and loop shrink as still-safe but unselected residual candidates
owned by the admitted target.

## C1-04 Campaign Budget And Terminals

The omitted numeric budget defaults to exactly three successful cuts. Run
three eligible cuts serially through the complete gate, recording each
successful Lock and decrementing the budget. Stop as **Budget exhausted** with
the fourth eligible cut reported as a residual owned by the named region. Do
not renew the budget.

Across all cases, a proof-failing attempt consumes zero successful-cut budget;
only a successfully Locked cut decrements it. Preserve the current proved
unstaged state, exact index, and unrelated work at every stop.

- Complete five-rung inspection with no admissible cut: **Clean**. Make no
  further cut and report no admissible in-region simplification; name any
  out-of-region obligation and its owner separately.
- Zero remaining successful-cut budget with eligible residuals: **Budget
  exhausted**. Stop immediately and report every eligible residual and its
  named region owner.
- Only formatting or presentation change: **Diminishing return**. Do not count
  it as progress or consume budget; stop with that presentation-only move
  rejected and its code region as the residual owner.
- A move recreates an earlier equivalent obligation: **Oscillation**. Do not
  make or count the move; stop with the equivalent obligation and named region
  owner recorded.
- A proof-failing attempt: **Failed cut**. Preserve the pre-attempt current
  state, consume no budget, and report the failed caller-facing proof, exact
  work state, remaining budget, and proof/code owner of the residual.
- Drift or a foreign-owner boundary before the next cut: **Boundary stop**.
  Make no next cut, consume no budget, and report the exact drift, proof or
  region limit, or foreign ownership together with the owning residual.
- Explicit user budget `2`: permit at most two serial successful cuts. After
  the second successful Lock, stop as **Budget exhausted** and report the two
  remaining eligible cuts as residuals owned by the named region.

Every campaign Return includes the named mode and region, invariant behavior
contract and caller-facing seam, before/after proof for every successful cut,
changed paths, starting and ending work state, serial ledger, initial and
remaining budget, first applicable terminal, truthful residuals and owners,
skipped proof or risk, and confirmation that all results remain unstaged.
