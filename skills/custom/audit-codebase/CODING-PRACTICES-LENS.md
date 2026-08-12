# Coding Practices Lens

Apply repository, language, framework, formatter, linter, type checker, and
test conventions before generic advice. First attribute behavior, domain, and
ownership issues to their classes; Coding Practice may still own an
independently evidenced clarity or provability item in the same subsystem.

## Questions That Find Coding-Practice Issues

- **Naming:** Do names reveal accepted meaning, units, state, and intent, or
  does an observed ambiguity burden callers or tests?
- **Valid states:** Where commitments permit, can semantics, types, or local
  state representations define needless errors out of existence, or are
  invalid states representable or transitions hidden?
- **Control flow:** Are meaningful happy, edge, cleanup, and failure paths
  visible without obscuring ordering?
- **Comments:** Do comments preserve a surprising constraint or trade-off, or
  duplicate syntax and drift from behavior?
- **Error expression:** After Reliability establishes required semantics, do
  names and structure preserve cause and caller-useful context?
- **Test portfolio:** Does each test prefer state verification through the
  Proof Seam and own a distinct supported behavior, invariant, branch, risk,
  or diagnostic responsibility? Is behavior verification limited to
  contractual interactions or necessary failure isolation?

For suspected test sprawl, map every relevant test to behavior, seam, oracle,
distinct risk, and observed cost. Admit consolidation only when overlap has no
distinct responsibility and the surviving portfolio preserves coverage and
diagnostic clarity. Different layers may deliberately prove different risks.

## Admission Boundary

Function length, nesting, magic values, comments, mutation, broad types, test
count, and suite time are discovery hints. Admit an item only when direct
evidence ties the practice to ambiguity, invalid states, duplicated expression,
change spread, proof friction, or avoidable maintenance cost in one supported
scenario.

Reliability owns validation correctness, failure semantics, concurrency
invariants, and behavioral coverage. Performance owns measured runtime and
resource claims. Coding Practice does not turn a stylistic preference into an
issue.
