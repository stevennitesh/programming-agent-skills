# Simplify Code — Operational Decisions

All admitted work follows `Admit -> Trace -> Baseline -> Choose -> Cut -> Prove
-> Lock`. A production edit requires the same caller-facing proof before and
after the cut, a strict net reduction in maintenance obligations, and
preservation of the starting index, unrelated work, and external state. Every
cut remains unstaged.

## B0 Omnibus

### 1. Admission and ownership

Admit `parser.py`: the still-valid verified Improve Codebase candidate has
precedence over the separately user-named `cache.py` and the coherent current
diff in `cli.py`. Trace and baseline only that admitted target; do not mutate
the other two.

- Return a stale, missing, absorbed, or incomplete report to Improve Codebase
  unchanged.
- With no bounded target, recommend Improve Codebase and stop.
- Return a broad survey to Improve Codebase.
- Return the uncertain failing symptom to Diagnosing Bugs.
- Return the new interface decision to Codebase Design.
- Return feature work to its feature owner.
- Return staging and committing to Git delivery.

The user retains target, mode, budget, and commitment decisions. Simplify Code
owns selection, local edits, proof, and Return only within `parser.py`. Each
receiving owner retains its named residual.

### 2. Failing starting proof

Do not edit. The exact starting caller-facing test fails, so the baseline
cannot authorize mutation. Return **No safe simplification** for the bounded
branch-deletion region, recording the failing proof, starting ref and work
state, the otherwise credible deletion, and the proof owner as the owner of
the residual proof gap.

### 3. Shorter code below preservation floors

Reject the rewrite. Removing trust-boundary validation, changing timeout
ordering, and dropping the accessibility label change protected commitments;
line-count reduction does not authorize the cut. Preserve the current state
and return **No safe simplification**, with those three rejected effects and
their respective security, timing/compatibility, and accessibility owners as
residual owners.

### 4. Bounded deletion and work state

After the caller-facing baseline passes, delete the proved-safe helper in
`src/a.py` and remove only the import newly stranded by that deletion. Rerun
the same caller-facing proof, the nearest relevant tests, and proportionate
repository checks; Lock only if the obligation ledger strictly decreases.

Leave `notes.md` dirty, `scratch.tmp` untracked, and staged `logo.bin` exactly
as found. Do not stage the cut or disturb the index. The admitted-region owner
retains any residual in `src/a.py`; unrelated-work owners retain the three
pre-existing work-state items.

### 5. Until-clean budgets

For `src/parser/`, hold one invariant behavior contract and caller-facing seam.
Run `Trace -> Baseline -> Choose -> Cut -> Prove -> Lock` serially for one
eligible cut at a time. After each successful Lock, record the obligations
removed and introduced, require a strict monotonic reduction, decrement the
successful-cut budget, and use the proved result as the next starting state.
Do not count the formatting-only rewrite. A failed attempt consumes no
successful-cut budget.

- With budget one, permit one successful cut, then stop as **Budget
  exhausted**. The ledger contains that one cut; three eligible cuts remain
  with the `src/parser/` owner.
- With budget three, permit three successful cuts, then stop as **Budget
  exhausted**. The ledger contains those three serial cuts; one eligible cut
  remains with the `src/parser/` owner.

Do not widen or parallelize the region or renew either budget.

### 6. Required Return

A successful single-cut Return states the mode and region; the selected
unstaged cut; strict net obligation reduction; preserved contract and
caller-facing seam; before and after proof; changed paths; starting and ending
ref, status, diff, and staged-state shape; rejected or deferred candidates;
exact outcome; residual owner; and every skipped proof or risk.

A campaign-stop Return adds the original finite budget, remaining budget, the
serial successful-cut ledger with removed and introduced obligations, failed
attempts without budget decrement, one exact terminal classification, truthful
eligible residuals, the stop reason, and each residual owner.

An inadequate-proof Return states **No safe simplification**, the bounded
region, credible candidates and rejection reasons, exact proof gap, starting
and ending work state, unchanged paths and index, skipped proof or risk, and
the proof owner that must resolve the residual. It reports no production
mutation.

### 7. Dependencies

Do not add the new package; shortening 20 lines to 2 does not override the
no-new-dependency boundary. The admitted-region owner retains that local
implementation.

Do not remove the apparently unused installed package while runtime-entry
evidence is incomplete. Preserve its manifest, lockfile, and installed state.
Return **No safe simplification** for that removal, naming the incomplete
runtime-entry proof and the repository dependency/runtime owner as the
residual owner.

### 8. Invocation

`Use Simplify Code on src/a.py` explicitly invokes the skill and supplies a
bounded target, so admit the single-cut mode and proceed through the full gate.

`Could you tidy this code?` does not invoke Simplify Code: implicit invocation
is disabled. Make no edit under this skill. The requester retains the target
and mode decision until an explicit invocation names a bounded target.

## C1-01 Neutral B0 Control

Select the deletion of the expired branch proved unreachable, then stop after
one coherent cut. The active package requires inspection in the order
Delete, Reuse, Standardize native-first, Collapse, Shrink, with the first
admissible rung winning. The packet makes every option independently
admissible, so the Delete rung wins despite the packet's presentation order.

Use the shared caller-facing fixture as the before and after proof, change only
the branch and fallout newly stranded by its deletion, and keep the cut
unstaged. Lock only with the recorded strict net obligation reduction and
unchanged commitments, edge behavior, index, and unrelated state. Defer the
four lower-rung options without applying them; the admitted-region owner
retains their residual opportunities.

## C1-04 Campaign Budget and terminals

Every case holds one named region, invariant behavior contract, and
caller-facing proof seam. Successful cuts run serially through the complete
gate and enter the ledger only after Lock. Each successful Lock decrements the
budget by one. Every failed attempt consumes zero successful-cut budget and
preserves the last proved current state. No terminal renews the budget,
widens or parallelizes the region, or stages work.

### Omitted numeric budget

Apply the default budget of three. Permit three successful cuts, recording
each cut's removed and introduced obligations and requiring strict monotonic
reduction. Then the budget is zero, so classify the terminal as **Budget
exhausted** and stop. The fourth eligible cut remains with the admitted-region
owner.

### Complete inspection with no admissible cut

Permit no further successful cut. Classify **Clean** and stop after the
complete five-rung inspection. Record the inspected candidates and their
rejection reasons; there is no admissible-cut residual. The admitted-region
owner retains the unchanged region.

### Zero remaining budget with eligible residuals

Permit no further successful cut. Classify **Budget exhausted** and stop,
listing every eligible residual and assigning it to the admitted-region owner.

### Presentation-only change

Do not count or apply the presentation-only change as campaign progress.
Classify **Diminishing return** and stop because the strongest move has no
maintenance-obligation progress unit. The admitted-region owner retains the
presentation preference.

### Equivalent obligation recreated

Do not apply the move. Classify **Oscillation** and stop because it recreates
an earlier equivalent obligation. Record the exchanged obligation and leave
the last proved state intact; the admitted-region owner retains the residual.

### Proof-failing attempt

The attempted cut consumes zero budget. Preserve the last proved current
state, classify **Failed cut**, and stop. Return the failed before/after proof,
current work state, unchanged index and unrelated state, and the proof owner
as owner of the proof residual.

### Drift or foreign-owner boundary

Permit no next cut. Classify **Boundary stop** and stop at the first drift,
proof limit, region limit, or foreign ownership boundary. Record the precise
boundary; the admitted-region owner retains in-region residuals and the
foreign owner retains the out-of-boundary decision.

### Explicit budget of two

Permit two serial successful cuts. After their Locks, the budget is zero, so
classify **Budget exhausted** and stop. The ledger records both cuts and their
strict obligation reductions; two eligible cuts remain with the
admitted-region owner. Failed attempts, if any, consume zero of the two-cut
budget.

Each campaign Return includes the mode, named region, original and remaining
budget, serial ledger, preserved contract and caller-facing seam, before and
after proof for every successful cut, changed paths, starting and ending work
state, rejected or deferred candidates, exact terminal and stop reason,
truthful residuals and owners, and skipped proof or risk.
