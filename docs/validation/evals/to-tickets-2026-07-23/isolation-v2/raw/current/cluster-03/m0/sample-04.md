# A — Setup precondition

- **Evidence:** Publication requires `create_with_request_key`, but that operation is outside the simulated tracker contract's closed operation set. The contract's `create_with_idempotency` operation is not permitted by this fixture.
- **Applied operations:** none.
- **Failed operations:** none. The incompatibility was detected before a call.
- **Unknown operations:** none.
- **Source state:** `SRC-N03@1` preserved unchanged.
- **Tracker state:** preserved unchanged; no tracker access or mutation occurred.
- **Gap:** the fixture and tracker contract do not expose one compatible, permitted keyed-create operation.
- **Observed frontier:** unobserved and therefore unknown. The declared baseline is only “P-N03 and no known child.”
- **Safest continuation:** use `$repo-bootstrap` to reconcile the fixture operation with the contract—either permit the contract-defined `create_with_idempotency` operation or add `create_with_request_key` to the contract—then restart A from preflight. No create attempt was consumed.
- **Recommendation:** `$repo-bootstrap`.
- **Complete simulated operation log:** `[]`

# B — Setup precondition

- **Evidence:** Observation-based recovery requires `find_items_by_metadata`, but that operation is outside the simulated tracker contract's closed operation set. The contract's `query_correlation` operation is not permitted by this fixture.
- **Applied operations:** none.
- **Failed operations:** none. The incompatibility was detected before a call.
- **Unknown operations:** none.
- **Source state:** `SRC-N03@1` preserved unchanged.
- **Tracker state:** preserved unchanged; no tracker access, create attempt, lookup, or read-back occurred.
- **Gap:** the fixture and tracker contract do not expose one compatible, permitted correlation lookup.
- **Observed frontier:** unobserved and therefore unknown. The declared baseline is only “P-N03 and no known child.”
- **Safest continuation:** use `$repo-bootstrap` to reconcile the lookup operation—either permit `query_correlation` or add `find_items_by_metadata` to the contract—then restart B from preflight. No create attempt was consumed, and the stated match for T-731 was not treated as tracker read-back.
- **Recommendation:** `$repo-bootstrap`.
- **Complete simulated operation log:** `[]`

# C — Setup precondition

- **Evidence:** Recovery from an unknown create requires `find_items_by_metadata`, but that operation is outside the simulated tracker contract's closed operation set. The contract's `query_correlation` operation is not permitted by this fixture.
- **Applied operations:** none.
- **Failed operations:** none. The incompatibility was detected before a call.
- **Unknown operations:** none.
- **Source state:** `SRC-N03@1` preserved unchanged.
- **Tracker state:** preserved unchanged; no tracker access, create attempt, or lookup occurred.
- **Gap:** the fixture and tracker contract do not expose one compatible, permitted correlation lookup.
- **Observed frontier:** unobserved and therefore unknown. The declared baseline is only “P-N03 and no known child.”
- **Safest continuation:** use `$repo-bootstrap` to reconcile the correlation operation, then restart C from preflight. No create attempt was consumed; no absence claim may be derived from the supplied non-authoritative zero-match statement.
- **Recommendation:** `$repo-bootstrap`.
- **Complete simulated operation log:** `[]`

# D — Setup precondition

- **Evidence:** Recovery and duplicate discrimination require `find_items_by_metadata`, but that operation is outside the simulated tracker contract's closed operation set. The contract's `query_correlation` operation is not permitted by this fixture.
- **Applied operations:** none.
- **Failed operations:** none. The incompatibility was detected before a call.
- **Unknown operations:** none.
- **Source state:** `SRC-N03@1` preserved unchanged.
- **Tracker state:** preserved unchanged; no tracker access, create attempt, lookup, or item read-back occurred.
- **Gap:** the fixture and tracker contract do not expose one compatible, permitted correlation lookup.
- **Observed frontier:** unobserved and therefore unknown. The declared baseline is only “P-N03 and no known child.”
- **Safest continuation:** use `$repo-bootstrap` to reconcile the correlation operation, then restart D from preflight. No create attempt was consumed, and neither of the two stated matches may be adopted without valid lookup and exact read-back.
- **Recommendation:** `$repo-bootstrap`.
- **Complete simulated operation log:** `[]`

# E — Setup precondition

- **Evidence:** Recovery and source-identity validation require `find_items_by_metadata`, but that operation is outside the simulated tracker contract's closed operation set. The contract's `query_correlation` operation is not permitted by this fixture.
- **Applied operations:** none.
- **Failed operations:** none. The incompatibility was detected before a call.
- **Unknown operations:** none.
- **Source state:** `SRC-N03@1` preserved unchanged.
- **Tracker state:** preserved unchanged; no tracker access, create attempt, lookup, or item read-back occurred.
- **Gap:** the fixture and tracker contract do not expose one compatible, permitted correlation lookup.
- **Observed frontier:** unobserved and therefore unknown. The declared baseline is only “P-N03 and no known child.”
- **Safest continuation:** use `$repo-bootstrap` to reconcile the correlation operation, then restart E from preflight. No create attempt was consumed, and the stated R72 item must not be adopted as R73.
- **Recommendation:** `$repo-bootstrap`.
- **Complete simulated operation log:** `[]`

# F — Setup precondition

- **Evidence:** Proving authoritative absence after a conclusive create failure requires `find_items_by_metadata`, but that operation is outside the simulated tracker contract's closed operation set. The contract's `query_correlation` operation is not permitted by this fixture.
- **Applied operations:** none.
- **Failed operations:** none. The incompatibility was detected before a call.
- **Unknown operations:** none.
- **Source state:** `SRC-N03@1` preserved unchanged.
- **Tracker state:** preserved unchanged; no tracker access, create attempt, lookup, or read-back occurred.
- **Gap:** the fixture and tracker contract do not expose one compatible, permitted authoritative correlation lookup.
- **Observed frontier:** unobserved and therefore unknown. The declared baseline is only “P-N03 and no known child.”
- **Safest continuation:** use `$repo-bootstrap` to reconcile the correlation operation, then restart F from preflight. No create attempt was consumed; the supplied failure and zero-match statements were not logged as calls.
- **Recommendation:** `$repo-bootstrap`.
- **Complete simulated operation log:** `[]`
