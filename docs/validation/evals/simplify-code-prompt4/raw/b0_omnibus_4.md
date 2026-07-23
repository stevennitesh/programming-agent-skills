# B0 Omnibus — Operational Decisions

These are read-only action decisions. No production mutation is performed. Any
later authorized cut must preserve the irreversible order `Admit -> Trace ->
Baseline -> Choose -> Cut -> Prove -> Lock`, use caller-facing before/after
proof, produce a strict net maintenance-obligation reduction, remain unstaged,
and name the owner of every residual.

1. **Target admission and Returns.** Admit `parser.py`: the still-valid verified
   Improve Codebase candidate outranks the separately user-named `cache.py`,
   which outranks the coherent `cli.py` diff. Authority covers one bounded
   behavior-preserving cut in `parser.py`, not either lower-precedence target.
   Trace its callers and commitments, establish a caller-facing baseline, and
   mutate only after a candidate passes the reduction gate; keep the result
   unstaged and report the complete Return before completion. Return a stale
   report unchanged to Improve Codebase; with no bounded target, recommend
   Improve Codebase and stop; return a broad survey to Improve Codebase,
   uncertain failure diagnosis to `$diagnosing-bugs`, a new interface decision
   to `$codebase-design`, feature work to its feature owner, and staging or
   committing to the Git-delivery owner. None of those companion cases
   authorizes mutation.

2. **Failed starting proof.** Do not delete the branch. The exact pre-mutation
   caller-facing test already fails, so the baseline cannot distinguish a
   behavior-preserving cut. Return **No safe simplification** for the bounded
   branch region, with the failing proof and unchanged work/index state; the
   residual belongs to `$diagnosing-bugs` or the baseline owner. Completion is
   the fully accounted no-safe result, not an edit.

3. **Shorter but behavior-changing rewrite.** Reject the rewrite without
   mutation. Line count cannot override trust-boundary validation, timeout
   ordering, or accessibility commitments, and therefore cannot establish
   preserved behavior or a strict obligation reduction. Return **No safe
   simplification**, record all three rejected effects and the unchanged state,
   and assign the residual to the relevant security/behavior/accessibility
   owners.

4. **Bounded helper deletion.** After a passing caller-facing baseline, the only
   authorized mutation is the proved helper deletion in `src/a.py` plus removal
   of the import that this deletion newly strands in that same file. Rerun the
   same proof, then nearby tests and proportionate checks, and verify a strict
   net reduction. Leave `notes.md` dirty, `scratch.tmp` untracked, `logo.bin`
   staged, and the entire index exactly as found; the `src/a.py` result stays
   unstaged. Return the proof, obligation delta, sole changed path, starting and
   ending state, and any residual owner; complete only when refreshed state
   confirms those boundaries.

5. **Finite `until-clean` campaigns.** Authority is limited to
   `src/parser/` and the explicitly chosen positive budget. Hold one invariant
   contract and proof seam, and run `Trace -> Baseline -> Choose -> Cut -> Prove
   -> Lock` serially for each cut. After every successful Lock, append removed
   and introduced obligations to the ledger, require a strict monotonic net
   reduction, decrement the budget, and use that proved state as the next
   baseline. With budget **one**, make at most one eligible successful cut and
   stop for budget exhaustion, leaving three eligible cuts as owned residuals.
   With budget **three**, make at most three eligible successful cuts and stop
   for budget exhaustion, leaving one eligible cut as a residual. The
   formatting-only rewrite is never a successful cut and never consumes or
   renews budget. Either campaign stops earlier on no admissible cut, proof
   failure, drift, oscillation, or an externally owned boundary. All cuts remain
   unstaged; completion requires the finite budget, serial ledger, before/after
   proof for each cut, refreshed state, and truthful terminal reason.

6. **Required Returns.**
   - A successful-cut Return states single-cut mode and region; the cut; net
     obligation reduction; preserved contract and observable caller-facing
     seam; before/after proof; changed paths; starting/ending work and index
     state; rejected/deferred candidates; stop reason; residual owner; and
     skipped proof or risk. It explicitly says the result is unstaged.
   - A campaign-stop Return additionally states the initial and remaining
     finite budget, ordered successful-cut ledger, invariant contract/proof
     seam, and exact terminal reason, including unspent candidates and their
     owners. Completion requires every serial Lock and current-state agreement.
   - An inadequate-proof Return states **No safe simplification**, names the
     bounded region and proof gap, accounts for credible candidates and their
     rejection reasons, records unchanged paths and starting/ending work/index
     state, names the proof/diagnosis owner, and reports skipped proof or risk.
     Completion is permitted only when that no-mutation accounting agrees with
     current evidence.

7. **Dependencies.** Reject the new package: Simplify Code may not add a
   dependency even if it reduces 20 lines to 2, so there is no authorized
   mutation; return the proposal to the dependency/design owner. Do not remove
   the apparently unused installed package either: incomplete runtime-entry
   evidence cannot prove repository-wide non-use. Return **No safe
   simplification** with the incomplete search as the exact proof gap,
   unchanged manifest/lockfile/installed and work state, and the
   runtime-entry/dependency owner as the residual. Removal could be reconsidered
   only after source, configuration, and runtime-entry evidence proves no use
   and repository-owned installation proof can be reconciled.

8. **Invocation classification.** “Use Simplify Code on `src/a.py`” is an
   explicit invocation with a bounded target, so Admit may proceed, subject to
   trace, baseline, candidate, proof, reduction, unstaged-state, Return, and
   completion gates. “Could you tidy this code?” is an ordinary implicit
   request and does **not** invoke Simplify Code because implicit invocation is
   disabled; perform no mutation and leave routing/explicit authorization with
   the user.
