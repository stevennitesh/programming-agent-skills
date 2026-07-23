# Simplify Code Operational Decisions

All admitted work follows `Admit -> Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`. Mutation begins only after the exact starting-state caller-facing proof succeeds. Every cut remains unstaged, preserves the index and unrelated work, and must show a strict net reduction in maintenance obligations.

## B0 Omnibus

### 1. Admission and Return boundaries

Admit `parser.py`: the still-valid verified Improve Codebase candidate has precedence over the separately user-named `cache.py` and the coherent current diff in `cli.py`. The user retains authority over target, mode, budget, and commitment decisions; Simplify Code owns candidate selection, local unstaged edits, proof, and Return inside `parser.py`.

- Return the stale report to Improve Codebase unchanged.
- With no bounded target, recommend Improve Codebase and stop.
- Return the broad survey to Improve Codebase.
- Return the uncertain failing symptom to Diagnosing Bugs.
- Return the new interface decision to Codebase Design.
- Return the feature to its feature owner.
- Return staging and committing to the Git-delivery owner; do not stage or commit.

Each returned item remains owned by the named owner and is not absorbed into the simplification.

### 2. Failing starting proof

Do not edit. The failing exact starting test cannot authorize production mutation even though the proposed deletion is bounded and has a caller-facing test. Return **No safe simplification**, identify the failing baseline as the proof gap, report the starting work state unchanged, and name the proof or behavior owner as the residual owner.

### 3. Shorter code below preservation floors

Reject the rewrite. Removing trust-boundary validation, changing timeout ordering, and dropping an accessibility label violates preserved security, timing/ordering, and accessibility commitments. Line reduction does not authorize the cut. Leave state unchanged and return **No safe simplification** with those rejected effects and the corresponding security, behavior, and accessibility owners.

### 4. Bounded helper deletion

Delete the proved-safe helper in `src/a.py` and remove only the import newly stranded by that deletion in `src/a.py`. Rerun the same caller-facing proof and then the nearest relevant checks. Leave `notes.md`, untracked `scratch.tmp`, staged `logo.bin`, and the entire index exactly as found. The resulting `src/a.py` change remains unstaged. Pre-existing unrelated work remains with its existing owner.

### 5. `until-clean` budgets

For every cut, run the complete serial gate:

`Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`

After each successful Lock, record removed and introduced obligations, require a strict monotonic net reduction, decrement the successful-cut budget, and use that proved result as the next starting state. A failed attempt consumes no successful-cut budget. The formatting-only rewrite is never a progress unit.

- Budget `1`: permit one successful cut, record ledger entry 1, then stop as **Budget exhausted**. Report the three remaining eligible cuts as residuals owned by the named region owner.
- Budget `3`: permit three serial successful cuts, record ledger entries 1 through 3, then stop as **Budget exhausted**. Report the fourth eligible cut as a residual owned by the named region owner.

Do not widen or parallelize the region and do not renew either budget.

### 6. Required Return shapes

A successful-cut Return states the mode and region; selected cut; removed and introduced obligations and strict net reduction; preserved contract and caller-facing observable seam; exact before and after proof; changed paths; starting and ending work state; rejected or deferred candidates; stop reason; residuals and their owner; skipped proof or risk; and confirmation that the result is unstaged, the index is unchanged, and unrelated state is preserved.

A campaign-stop Return adds the initial and remaining finite successful-cut budget, the serial successful-cut ledger, failed-attempt accounting, the first applicable terminal classification, eligible residuals, and their owner.

An inadequate-proof Return states **No safe simplification**; the bounded region; credible candidates and rejection reasons; the exact proof gap; the available before-proof result and absence of an authorizing after-proof; unchanged work state and changed paths; exact stop reason; skipped proof or risk; and the owner of the unresolved proof or behavior. It makes no production mutation.

### 7. Dependencies

Do not add the new package: reducing 20 lines to 2 does not override the prohibition on adding a dependency. Leave the proposed replacement with the bounded-region owner.

Do not remove the installed package while the runtime-entry search is incomplete. Repository-wide source, configuration, and runtime-entry evidence is required before removal, followed by manifest, lockfile, and repository-owned installation-proof reconciliation. Preserve the package and current state; the runtime-entry and dependency owner owns the residual evidence gap.

### 8. Invocation

“Use Simplify Code on `src/a.py`” is an explicit invocation with a named bounded target, so admit it subject to Trace and Baseline.

“Could you tidy this code?” does not invoke Simplify Code because implicit invocation is disabled. Do not mutate under this skill; the request remains with the caller until the skill is explicitly invoked and the target is bounded.

## C1-01 Neutral B0 Control

Select the expired branch proved unreachable and stop after one coherent cut. The active package requires inspection in this order: Delete, Reuse, Standardize native-first, Collapse, then Shrink; the first admissible rung wins. All five offered cuts are admissible, so Delete wins even though it appears last in the packet's presentation order.

Use the shared caller-facing fixture as the exact before proof, delete only the expired branch and fallout newly created by that deletion, rerun the same fixture as after proof, then run the nearest relevant checks. Lock only if commitments and edge behavior remain preserved and the ledger shows a strict net maintenance-obligation reduction. Leave the result unstaged, preserve the index and unrelated state, defer the four unselected cuts to the bounded-region owner, and report them as residual candidates rather than combining them with this cut.

## C1-04 Campaign Budget and Terminals

The omitted numeric budget defaults to exactly `3` successful cuts. Run cuts serially through the complete gate, ledger each successful Lock, and decrement only after success. With four eligible cuts, permit three successful cuts and stop **Budget exhausted** with zero budget remaining; report the fourth eligible cut as a residual owned by the named region owner. Any failed attempt consumes no successful-cut budget.

For the independent companion cases, apply the first applicable terminal:

- Complete five-rung inspection with no admissible cut: **Clean**. Stop with no eligible cut; report any non-admissible candidates and their rejection reasons, with residuals owned by the named region owner.
- Zero remaining successful-cut budget with eligible residuals: **Budget exhausted**. Make no next cut; enumerate the eligible residuals and their region owner.
- Only a formatting or presentation change: **Diminishing return**. Count no progress unit, consume no budget, make no progress-only mutation, and leave the presentation residual with the region owner.
- A move recreates, undoes, or exchanges an earlier obligation for an equivalent one: **Oscillation**. Do not make that move; consume no budget and report the equivalent obligation as a residual owned by the region owner.
- A proof-failing attempt: **Failed cut**. Preserve the current proved state, consume no successful-cut budget, report the failed proof and work state, and name the proof or behavior owner for the residual.
- Drift, a proof limit, a region limit, or foreign ownership before the next cut: **Boundary stop**. Do not widen the region or cross ownership; consume no budget and name the foreign, proof, or region owner that owns the residual.
- Explicit user budget `2`: permit exactly two serial successful cuts, record two ledger entries, then stop **Budget exhausted** with the other two eligible cuts reported as residuals owned by the named region owner.

Every campaign Return includes the named mode and region, invariant behavior contract and caller-facing proof seam, before and after proof for each successful cut, changed paths, starting and ending work state, initial and remaining budget, serial ledger of removed and introduced obligations, failed-attempt accounting, deferred candidates, exact terminal and stop reason, residuals and their owner, skipped proof or risk, and confirmation that the result is unstaged with the index and unrelated state preserved.
