# Deepening

Use this branch when dependency shape changes the seam, substitute, test
migration, or verification strategy.

[`SKILL.md`](SKILL.md) owns vocabulary and taste.
[DIRECT-DESIGN.md](DIRECT-DESIGN.md) owns the direct pass and design packet.
This file owns dependency classification, Seam placement, test
responsibilities, coverage parity, Change Closure, and bounded migration.

Classify -> Place -> Substitute -> Replace -> Migrate.

## 1. Classify

Classify every dependency whose shape affects the proposed interface, seam,
substitute, migration, or proof:

| Category | Design and proof consequence |
| --- | --- |
| **In-process** | Keep computation and memory inside the module. Add no adapter; prove behavior through the deeper interface. Test an internal rule directly only when it is independently meaningful. |
| **Local-substitutable** | Use a realistic local substitute such as memory, an isolated filesystem, an emulator, SQLite, or a deterministic queue. Inject it only at a real caller concern or I/O edge. |
| **Remote-owned** | Put an interface where transport varies. Keep domain decisions in the module; use the supported transport adapter and a fake or in-memory adapter. Add contract proof when the remote contract carries risk. |
| **True external** | Put an adapter at the third-party seam. Keep vendor translation in the adapter and domain decisions in the module. Use the smallest fake, stub, or mock that proves the risk. |

## 2. Place

Place the narrowest Seam earned by locality, dependency isolation, domain
ownership, supported variation, or a real external boundary. A substitute,
emulator, or second integration can demonstrate variation; a test double alone
cannot. Keep internal Seams private and treat a test-only patch point as
Interface pressure.

When a required Seam is absent in legacy code, use the smallest
behavior-preserving enabling point that exposes it. Do not widen the public
Interface merely to make testing convenient.

## 3. Substitute

Choose substitutes by behavior risk, not convenience. Prove domain behavior
through the deeper interface. Add separate substitute or supported-adapter
contract tests only when their fidelity or translation carries independent risk.

When callers rely on implementations interchangeably, require behavioral
subtyping: substitutes must preserve applicable public preconditions,
postconditions, and class invariants. Do not require implementation matching.

## 4. Replace, Don't Layer

Establish **coverage parity** through the deeper Interface before removing
shallow tests. Map each distinct behavior, Invariant, branch, or risk to one
canonical test owner. Reuse or extend that owner before adding a test; keep a
separate test only for a distinct responsibility or necessary failure
isolation. Classify every affected test as **add, rewrite, keep, or delete**:

- **Add** caller-facing behavior proof that is missing.
- **Rewrite** behavior whose current test surface becomes obsolete.
- **Keep** dense rules, adapter contracts, regressions, or behavior not yet
  covered through the deeper interface.
- **Delete** pass-through, call-order, or implementation-detail assertions
  superseded by stronger behavior proof.

Prefer state verification through observable outcomes; use behavior
verification only when the interaction is the contract or provides necessary
failure isolation. A test that changes only because Implementation moved is
testing past the Interface.
Remove shallow implementation and test paths only after stronger proof owns their
Responsibilities.

## 5. Migrate

Name the first behavior-preserving migration step, verification evidence, applicable
Change Closure, stop boundary, and follow-ups. Account for displaced
Implementation, callers, registrations, exports, flags, tests, configuration,
docs, and migrations. A retained compatibility path needs an owner, reason,
proof, and removal condition. Keep migration inside the bounded slice.

## Contribution To The Design Packet

Return the dependency classifications; Seam, Adapters, and substitutes;
canonical test owners, test disposition, and coverage-parity evidence; bounded
migration and Change Closure; verification evidence; and stop boundary.

## Completion

Complete when every relevant dependency is classified; Seam and substitute
choices match those categories; the proposed Interface is smaller and useful;
coverage parity and canonical ownership account for every affected test;
Change Closure accounts for every displaced path; verification evidence is named;
and migration stops at the bounded-slice edge.
