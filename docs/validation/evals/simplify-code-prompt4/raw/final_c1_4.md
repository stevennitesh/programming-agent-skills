# Operational Decisions

## B0 Omnibus

### 1. Admission and Return

Admit `parser.py`. The still-valid verified Improve Codebase candidate has
precedence over the separately user-named `cache.py` target and the coherent
current diff in `cli.py`. Do not modify `cache.py` or `cli.py`; their residual
owner remains the user.

- Return a stale report to Improve Codebase unchanged.
- With no bounded target, recommend Improve Codebase and stop.
- Return a broad survey to Improve Codebase.
- Return an uncertain failing symptom to Diagnosing Bugs.
- Return a new interface decision to Codebase Design.
- Return feature work to the feature owner.
- Return staging and committing to the Git delivery owner.

None of those returns authorizes copying the other owner's procedure or
mutating production code, the index, trackers, installed state, or external
state.

### 2. Red baseline

Do not edit. The exact starting caller-facing test fails, so the baseline
cannot authorize the branch deletion. Return **No safe simplification** for the
bounded branch, identify the failing test as the proof gap, report the starting
work state unchanged, and leave the proof residual with the repository's test
owner.

### 3. Preservation floors

Reject the four-line rewrite. Reduced line count does not authorize removing
trust-boundary validation, changing timeout ordering, or dropping an
accessibility label. Preserve those commitments and leave the rewrite residual
with the owners of security validation, timing compatibility, and
accessibility.

### 4. Bounded deletion and work state

Delete the proved-safe helper in `src/a.py` and remove only the import in
`src/a.py` newly stranded by that deletion. Make the cut unstaged. Do not alter
the pre-existing dirty `notes.md`, the untracked `scratch.tmp`, or staged
`logo.bin`; preserve the index exactly, including the staged identity of
`logo.bin`. Run the same caller-facing proof before and after the cut, then the
nearest relevant checks. Refresh `src/a.py` and work state after proof and
account for the helper and import removed, with no transferred obligation.
Any unrelated dirty or untracked work remains owned by the user.

### 5. Explicit finite campaigns

For either budget, hold one behavior contract and caller-facing proof seam and
run, serially, one cut at a time:

`Trace -> Baseline -> Choose -> Cut -> Prove -> Lock`

After each successful Lock, record removed and introduced obligations, require
a strict monotonic net reduction, decrement the successful-cut budget, and use
the proved unstaged result as the next starting state. A failed attempt consumes
no successful-cut budget and stops as **Failed cut**, with current state,
failed proof, and the proof owner recorded. The formatting-only rewrite is not
a progress unit and never consumes budget.

- With budget `1`, make one eligible successful cut, record ledger entry 1, and
  stop as **Budget exhausted**. Report the other three eligible cuts as
  residuals owned by the user for a separately authorized campaign.
- With budget `3`, make three eligible successful cuts, record ledger entries
  1 through 3, and stop as **Budget exhausted**. Report the fourth eligible cut
  as a residual owned by the user for a separately authorized campaign.

Do not renew either budget, widen or parallelize the region, or continue into
the formatting-only rewrite.

### 6. Required Return shapes

For a successful single cut, return: single-cut mode and bounded region; the
selected cut; strict net obligation reduction; preserved contract and
observable caller-facing seam; exact before and after proof; changed paths;
starting and ending status, diff, and staged-state shape; rejected or deferred
candidates; residual owner; skipped proof or risk; and confirmation that the
result is unstaged and the index and unrelated state remain as found.

For a campaign stop, return all of the preceding applicable fields plus:
`until-clean` mode; named region; initial and remaining successful-cut budget;
the serial ledger of each successful cut's removed and introduced obligations;
the exact first-applicable terminal classification and stop reason; truthful
eligible residuals and their owner; and current unstaged work state.

For a region with inadequate proof, return **No safe simplification** with:
the bounded region; credible candidates and their rejection reasons; preserved
contract and intended seam; exact proof gap; starting and ending work state;
changed paths, which are none; residual proof owner; skipped proof or risk; and
confirmation that no mutation occurred.

### 7. Dependencies

Do not add the new package merely to shorten 20 lines to 2. Adding a dependency
is outside the permitted cut.

Do not remove the installed package while runtime-entry evidence is incomplete.
Repository-wide source, configuration, and runtime-entry evidence must prove
that no use remains before removal, after which the manifest, lockfile, and
repository-owned installation proof would also have to be reconciled. Return
**No safe simplification**, name the incomplete runtime-entry search as the
proof gap, preserve installed and work state, and leave the residual with the
repository dependency/runtime owner.

### 8. Invocation

“Use Simplify Code on `src/a.py`” is an explicit invocation and admits
`src/a.py` as the user-named bounded target, subject to the baseline and the
remaining gates.

“Could you tidy this code?” is an ordinary implicit request and does not invoke
Simplify Code because implicit invocation is disabled. Make no Simplify Code
mutation; the user retains authority to invoke it explicitly and name a bounded
target.

## C1-01 Neutral B0 Control

Select the proved deletion of the expired unreachable branch and stop after
that one coherent cut. The active package supplies the selection order:
Delete, Reuse, Standardize native-first, Collapse, then Shrink, and says that
the first admissible rung wins. All five candidates are independently
admissible, so the Delete candidate precedes the project-owner reuse,
runtime-native standardization, abstraction collapse, and loop shrink
candidates regardless of their presentation order.

Use the stated caller-facing fixture before mutation and rerun the same fixture
afterward, then run the nearest relevant checks. Confirm a strict net reduction
from removing the expired branch without introducing or transferring an
obligation. Leave the other four candidates deferred, keep the selected result
unstaged, preserve the index and unrelated state, and leave any further-cut
authority with the user.

## C1-04 Campaign Budget and Terminals

Every case is serial within the one named region, retains one invariant
behavior contract and proof seam, and leaves successful cuts unstaged. A
successful cut decrements budget only after Lock and a ledger entry showing
removed and introduced obligations with strict monotonic reduction. A failed
attempt never consumes successful-cut budget. The first applicable terminal
stops the campaign; no terminal widens the region, renews the budget, or
authorizes work owned elsewhere.

### Omitted numeric budget

Use the default budget of exactly `3` successful cuts. Make and prove three
eligible cuts serially, producing three ledger entries. The fourth eligible cut
remains a truthful residual. With zero budget remaining, stop as **Budget
exhausted** and leave that residual with the user for a separately authorized
campaign.

### Complete inspection with no admissible cut

Permit zero further successful cuts and stop as **Clean** after one complete
five-rung inspection. Report that there are no admissible cut residuals.
Rejected candidates and their reasons remain in the Return; no mutation occurs.

### Zero remaining budget with eligible residuals

Permit zero further successful cuts and stop as **Budget exhausted**. List each
eligible residual without executing it and leave renewal authority with the
user. Preserve the proved current unstaged state.

### Formatting or presentation only

Permit zero successful cuts for the offered move and stop as **Diminishing
return** because it supplies no progress unit and changes presentation only.
Do not count or apply it as campaign progress. Leave presentation-only work
with the ordinary formatting/style owner.

### Equivalent obligation recreated

Permit zero successful cuts for the offered move and stop as **Oscillation**.
Do not apply a move that recreates, undoes, or exchanges an earlier obligation
for an equivalent one. Record the equivalence in the ledger context and leave
the rejected residual with the region maintainer.

### Proof-failing attempt

The attempt consumes zero successful-cut budget. Stop as **Failed cut**,
preserve the current state from before the attempt, and report the attempted
cut, exact failed proof, remaining budget, work state, and proof residual owned
by the repository's test/proof owner. Do not proceed to another candidate.

### Drift or foreign-owner boundary

Permit no next cut and stop as **Boundary stop**. Report whether region drift,
proof limits, region limits, or foreign ownership blocked the next cut; name
the affected residual and its repository owner; and preserve current work,
index, unrelated, installed, tracker, and external state.

### Explicit budget of two

Permit exactly two eligible successful cuts. Prove and Lock them serially,
record two ledger entries, and decrement the budget to zero. Stop as **Budget
exhausted** with the other two eligible cuts listed as residuals owned by the
user for a separately authorized campaign. Any proof-failing attempt before
that terminal consumes no successful-cut budget and instead stops immediately
as **Failed cut**.

For every campaign terminal, Return the mode and region; successful cuts or
**No safe simplification** result; net obligation reduction; preserved
contract and observable seam; before and after proof; changed paths; starting
and ending work state; initial and remaining budget; serial ledger; rejected or
deferred candidates; exact terminal and stop reason; residuals and their named
owner; skipped proof or risk; and confirmation that the result remains unstaged
with the index and unrelated state preserved.
