# Advance

Load only when Orient selects `Advance` for one frontier ticket or one Waiting
or Blocked ticket whose supplied evidence can answer its exact condition.
Otherwise do not load it.

1. **Select.** Use the named eligible ticket or the frontier head. Otherwise
   return its state and the actual frontier.
2. **Freeze.** Lock the map identity and open state, ticket contract,
   dependencies, eligibility, and commit-point fields.
3. **Resolve.** Through the Mutation Gate, exclusively claim and read back the
   ticket before invoking its locked resolver or validating the attributable
   return. Missing explicit target approval returns `incomplete` before shared
   mutation.
4. **Commit.** After resolver work, acquire the map claim with the same token,
   refresh the frozen fields, apply the Mutation Gate's Advance drift rule,
   normalize the intact Return, and Reconcile.
5. **Complete.** Read back the outcome or wait, pointers, graph, fog,
   allowance, and frontier; let the Mutation Gate release both claims, prove
   absence, and Orient.

Return after one resolver Return becomes one outcome, one verified wait, or
one bounded replacement graph, with no retained claim.
