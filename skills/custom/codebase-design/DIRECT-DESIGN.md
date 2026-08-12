# Direct Design Pass

Use this branch for one bounded module, shallow cluster, seam, or interface
question. [`SKILL.md`](SKILL.md) owns vocabulary, taste, and the read-only
boundary.

Orient -> Diagnose -> Shape -> Compare -> Recommend.

## 1. Orient

Reuse a supplied **Source Trace** only when it is current, bounded, and
sufficient. Apply the caller-loaded engineering contract; otherwise read
`docs/agents/engineering-contract.md` when present. Follow
`docs/agents/domain.md` when present.

Trace the request or caller artifact, Commitment Boundary, accepted domain
terms and ADRs, current Interface and Implementation, material
Responsibilities and owners, representative callers and tests, dependencies,
operational constraints, and, when an existing path may be displaced, the first
migration edge. Inspect bounded history only when repeated change, churn, or
compatibility supports a design claim.
When observable behavior may have actual dependents, distinguish actual
dependence from the intended contract; dependence informs migration without
automatically expanding that contract.

If material behavior, ownership, authority, or compatibility cannot be
established, return `decision-needed` or `evidence-gap` with the exact missing
fact and no recommendation.

## 2. Diagnose

Name the Module, Interface, Implementation, material Responsibilities,
Invariants, state and failure policies and their owners, spread behavior or
decisions, caller and test friction, Interface pressure, deletion-test result,
real or hypothetical Seams, and relevant repeated-change hotspots. Explain the
losses in Depth or information hiding and the demonstrated change
amplification, cognitive load, or unknown unknowns; retain the current shape
when no material problem is proved.

## 3. Shape

Choose the strongest shape: deepen, merge, inline, retain, replace, or introduce
no new seam. Describe its caller-facing contract, hidden behavior and decisions,
any earned seam, adapters or substitutes, caller and test surfaces, and first
bounded change step plus migration when applicable.

For an already-needed Module, keep capabilities within current needs while
making the Interface somewhat general-purpose: remove caller-specific special
cases without adding speculative capability.

State the ordinary caller-facing contract: Responsibility and exclusions;
operations, inputs, outputs, and effects; governing Invariants and failure
policy; and the Proof Seam. A Proof Seam establishes meaning; it does not by
itself earn a design Seam or Adapter.

Add state lifecycle, ordering, Concurrency, Idempotency, Failure Atomicity, and
Recovery only when reachable state or transitions can change the requested
behavior. Add Trust Boundaries and configuration only when the design changes
or must preserve an accepted boundary. Add Observability or performance
constraints only when the accepted contract or supported measurement makes
them consequential. Add Compatibility and migration only when observable
behavior may have dependents or the design displaces an existing path. A
dormant concern creates no packet field or `N/A` entry.

When an existing shared abstraction binds different meanings, owners, change
rates, or failure modes, treat it as a wrong abstraction. Compare unsharing and
bounded duplication before adding another layer.

Where commitments permit, define errors out of existence before adding
caller-handled failure cases.

Admit **replace** only when the intended contract and actual dependence are
traceable, incremental evolution is riskier or more complicated, parity has a
proof seam, and migration, cutover, rollback, and one bounded first slice are
explicit.

For an enforceable boundary, require one **boundary proof**: a representative
allowed caller, a forbidden caller, and a red-capable check that accepts the
first and rejects the second.

Read [DEEPENING.md](DEEPENING.md) when dependency shape changes the seam,
substitute, test migration, or verification strategy.

## 4. Compare

Compare the candidate with the current shape and the simplest no-new-seam
option under the same engineering and domain obligations. When replacement is
credible, compare it explicitly with incremental evolution. Read
[DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) when the Interface is consequential,
several shapes are plausible, or migration and Compatibility risk are
meaningful.

## 5. Recommend

Choose one design, retain the current shape, or return the unresolved decision
or evidence gap. For a recommendation, explain why it wins, why credible
alternatives lose, the first bounded change step, applicable migration,
verification evidence, risks, and follow-ups.

Evidence settles current behavior and constraints. The user or caller settles
public-contract changes and accepted trade-offs.

## Design Packet

Return:

- status: `recommended | retain | decision-needed | evidence-gap`, and return
  owner;
- Source Trace, current shape, ownership, deletion-test result, and friction;
- recommended or retained shape, material Interface contract, hidden behavior,
  and caller-retained Responsibilities;
- earned Seams, dependencies, Adapters, substitutes, and Proof Seams;
- Depth, information hiding, complexity symptoms, and test responsibilities;
- credible alternatives and recommendation when applicable;
- first bounded change step when change is recommended, plus applicable
  migration, verification, Change Closure, and stop boundary, including boundary
  proof when applicable;
- for replacement, parity seam, migration, cutover, and rollback evidence;
- risks, residual gaps, follow-ups, and any domain or ADR candidate; and
- caller ownership of acceptance, implementation, and downstream mutation.

## Completion

Complete with one terminal design packet. `decision-needed` or `evidence-gap`
names the exact missing owner or fact and makes no recommendation.
`recommended` or `retain` requires a sufficient Source Trace, explicit material
Interfaces, any Seams and Adapters to be earned, caller-facing proof, current
and no-new-seam comparison, and triggered alternatives. A recommendation also
requires a bounded first change step with applicable Change Closure and, when
an existing path is displaced, a bounded migration step.
Replacement additionally requires parity, migration, cutover, and rollback
evidence. Downstream acceptance and mutation remain caller-owned.
