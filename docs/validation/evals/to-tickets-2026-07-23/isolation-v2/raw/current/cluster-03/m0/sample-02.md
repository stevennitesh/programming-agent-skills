# Common frozen design R73

Source: `SRC-N03@1`, owned by Eli (audit owner), under parent `P-N03`.

Ordered ticket 1, metadata `RUN-73` / `ITEM-1`: **Enforce 30-day audit-record retention**

- Work-unit form: one vertical implementation slice.
- Desired behavior: the scheduled retention run deletes audit records older than 30 days while retaining records exactly at the 30-day boundary and all newer records.
- Edge and error acceptance: the integration fixture proves the cutoff boundary on both sides; a scheduler or deletion failure must be observable and must not be reported as a successful retention run.
- Source Trace: `SRC-N03@1` commitment C1; acceptance clauses “scheduled proof deletes records older than 30 days” and “records at the boundary and newer remain”; proof seam “retention scheduler integration fixture.”
- Blockers: none.
- Proof lane: retention-scheduler integration fixture. Verification authority: Eli, audit owner. Required evidence: a passing scheduled-run fixture showing deletion beyond the cutoff, preservation at and inside the cutoff, and observable failure behavior.
- Expected durable write scope: retention-policy configuration/scheduler behavior and deletion of qualifying audit records only.
- Scope fence: no unrelated audit behavior, no alternate retention duration, no duplicate tracker item, no live-provider contact, and no implementation outside the retention-policy slice.
- Role and state: authorized category role `enhancement`; `ready-for-agent` only after the complete item and its parent association read back exactly.
- Execution profile: audit-retention semantics are owned by Eli; production writes are limited to the retention scheduler/policy and qualifying record deletions; the scheduler integration fixture is the proof seam and scarce proof resource. With no sibling ticket there is no parallel execution opportunity. Treat scheduler mutation and cutoff proof as serial within this item.
- Parallel safety: serial single-item execution; no independence claim is needed or evidenced.
- Stateful boundary matrix:

  | Boundary | Supported branch / required behavior |
  |---|---|
  | Absent or initial | No enforced policy; install the settled 30-day behavior and prove its first scheduled run. |
  | Current reusable | An already-correct 30-day configuration may be reused only when the same boundary behavior passes the integration fixture. |
  | Legacy or incompatible | Any other cutoff behavior is incompatible and must not be treated as satisfying R73. |
  | Public access paths | Not applicable; the source authorizes the scheduled retention path only. |
  | Supported variants | One variant: 30 days, with records exactly on the boundary retained. |
  | Lifecycle transitions | Configure/reuse → scheduled run → qualifying deletion or observable failure → integration verification. |

Coverage is exhaustive: C1 maps to ticket 1; the two source acceptance clauses map to its cutoff proof; `retention policy` is its scope; duplicate items and live-provider contact remain explicit exclusions. There are no deferrals or uncovered commitments. The dependency graph is a single node with no edges.

## A — Published graph

Evidence: the provider documents keyed creation; `create_with_request_key` succeeds for R73 and the returned item reads back exactly.

- Applied operations: keyed creation of the one frozen R73 item.
- Failed operations: none.
- Unknown operations: none.
- Observed tracker state: `P-N03` exists and the exactly read-back R73 child is present with the frozen body, metadata, parent, authorized `enhancement` role, and `ready-for-agent` state.
- Ordered ticket references: the fixture-returned item ID (ticket 1).
- Coverage and graph: C1 is covered by ticket 1; graph `ticket 1` with no blocker edges.
- Observed frontier: the fixture-returned ticket 1 is the sole ready item.
- Mutation read-back: exact.
- Safest continuation: use the verified item; do not issue another create.
- Recommendation: `$implement`.

Complete simulated operation log:

1. `get_setup` → setup complete and compatible.
2. `get_parent(P-N03)` → exact parent observed.
3. `create_with_request_key(request_key=RUN-73, metadata={RUN-73, ITEM-1}, design=R73)` → success; one fixture ID returned.
4. `get_item(<returned fixture ID>)` → exact R73 item read-back.

## B — Published graph

Evidence: ordinary creation has an initially unknown application status; metadata lookup returns exactly `T-731`, and `get_item(T-731)` exactly matches frozen design R73.

- Applied operations: the ordinary create is recovered as applied to `T-731`.
- Failed operations: none.
- Unknown operations: none after recovery.
- Observed tracker state: `P-N03` exists and `T-731` is its exactly read-back R73 child with the frozen body, metadata, authorized `enhancement` role, and `ready-for-agent` state.
- Ordered ticket references: `T-731`.
- Coverage and graph: C1 is covered by `T-731`; graph `T-731` with no blocker edges.
- Observed frontier: `T-731` is the sole ready item.
- Mutation read-back: exact.
- Safest continuation: adopt `T-731`; do not retry creation.
- Recommendation: `$implement`.

Complete simulated operation log:

1. `get_setup` → setup complete and compatible.
2. `get_parent(P-N03)` → exact parent observed.
3. `create_item(metadata={RUN-73, ITEM-1}, design=R73)` → unknown application status.
4. `find_items_by_metadata(RUN-73, ITEM-1)` → one exact match, `T-731`.
5. `get_item(T-731)` → exact R73 item read-back; the create is recovered as applied.

## C — Partial-publication recovery

Evidence: ordinary creation has unknown application status; metadata lookup returns zero matches but is not authoritative for absence.

- Applied operations: none proven.
- Failed operations: none proven.
- Unknown operations: the single `create_item` attempt.
- Observed tracker state: `P-N03` exists; no child is observed, but an unobserved created child remains possible.
- Ordered ticket references: none safely established.
- Coverage and graph: frozen design R73 remains complete, but no complete published graph is claimable.
- Affected dependents: none.
- Observed frontier: none observed; the true frontier is unknown because the create may have applied.
- Safest continuation: preserve state and obtain authoritative provider-side correlation for `RUN-73` / `ITEM-1`; do not create again unless absence is authoritatively established and a new attempt is explicitly authorized.
- Recommendation: `none`.

Complete simulated operation log:

1. `get_setup` → setup complete and compatible.
2. `get_parent(P-N03)` → exact parent observed.
3. `create_item(metadata={RUN-73, ITEM-1}, design=R73)` → unknown application status.
4. `find_items_by_metadata(RUN-73, ITEM-1)` → zero matches; lookup is non-authoritative for absence.

## D — Partial-publication recovery

Evidence: ordinary creation has unknown application status; metadata lookup returns two matching items, so correlation is ambiguous and duplicate publication may already exist.

- Applied operations: none attributable with certainty.
- Failed operations: none proven.
- Unknown operations: the single `create_item` attempt and which, if either, matching item it produced.
- Observed tracker state: `P-N03` exists; two metadata matches are observed, with no unique R73 publication established.
- Ordered ticket references: none safely established.
- Coverage and graph: frozen design R73 remains complete, but no non-contradictory published graph is claimable.
- Affected dependents: none.
- Observed frontier: unknown; neither match can be admitted to the frontier without unique identity and exact read-back.
- Safest continuation: stop creation, preserve both matches, and require authoritative correlation plus duplicate/conflict repair before any item is marked or used as ready.
- Recommendation: `none`.

Complete simulated operation log:

1. `get_setup` → setup complete and compatible.
2. `get_parent(P-N03)` → exact parent observed.
3. `create_item(metadata={RUN-73, ITEM-1}, design=R73)` → unknown application status.
4. `find_items_by_metadata(RUN-73, ITEM-1)` → two matches; no unique correlation.

## E — Partial-publication recovery

Evidence: ordinary creation has unknown application status; metadata lookup returns one item, but exact inspection shows that its body belongs to R72 rather than R73.

- Applied operations: none proven for R73.
- Failed operations: none proven.
- Unknown operations: the single R73 `create_item` attempt.
- Observed tracker state: `P-N03` exists; one conflicting R72 item occupies the queried metadata, while the presence of a separately created R73 item is unresolved.
- Ordered ticket references: none safely established for R73.
- Coverage and graph: frozen design R73 remains complete, but the observed item cannot cover C1 and no published R73 graph is claimable.
- Affected dependents: none.
- Observed frontier: none for R73; the conflicting R72 item is excluded from this frontier.
- Safest continuation: stop creation, preserve the R72 item, repair the metadata/correlation conflict through tracker ownership, and authoritatively determine the R73 attempt’s outcome before considering a newly authorized create.
- Recommendation: `none`.

Complete simulated operation log:

1. `get_setup` → setup complete and compatible.
2. `get_parent(P-N03)` → exact parent observed.
3. `create_item(metadata={RUN-73, ITEM-1}, design=R73)` → unknown application status.
4. `find_items_by_metadata(RUN-73, ITEM-1)` → one match.
5. `get_item(<sole matching fixture ID>)` → conflicting R72 body; not R73.

## F — Partial-publication recovery

Evidence: ordinary creation conclusively fails before application, and an authoritative metadata lookup confirms zero matches.

- Applied operations: none.
- Failed operations: the single `create_item` attempt, conclusively not applied.
- Unknown operations: none.
- Observed tracker state: `P-N03` exists and no R73 child exists.
- Ordered ticket references: none.
- Coverage and graph: frozen design R73 remains complete, but nothing was published.
- Affected dependents: none.
- Observed frontier: empty.
- Safest continuation: preserve the clean tracker state; in a later run, obtain explicit authority for one new attempt and prefer documented keyed creation with `RUN-73`. No second create is authorized in this run.
- Recommendation: `none`.

Complete simulated operation log:

1. `get_setup` → setup complete and compatible.
2. `get_parent(P-N03)` → exact parent observed.
3. `create_item(metadata={RUN-73, ITEM-1}, design=R73)` → conclusive failure before application.
4. `find_items_by_metadata(RUN-73, ITEM-1)` → authoritative zero-match result.
