# Deepening

Use this branch when dependency shape changes the seam, substitute, test migration, or validation strategy.

[`SKILL.md`](SKILL.md) owns vocabulary and taste. [DIRECT-DESIGN.md](DIRECT-DESIGN.md) owns the direct pass and design packet. This file owns dependency classification, seam placement, coverage parity, and bounded migration.

Classify -> Place -> Substitute -> Replace -> Migrate.

## 1. Classify

Classify every dependency behind or across the proposed interface:

| Category | Design and proof consequence |
| --- | --- |
| **In-process** | Keep computation and memory inside the module. Add no adapter; prove behavior through the deeper interface. Test an internal rule directly only when it is independently meaningful. |
| **Local-substitutable** | Use a realistic local substitute such as memory, an isolated filesystem, an emulator, SQLite, or a deterministic queue. Inject it only at a real caller concern or I/O edge. |
| **Remote-owned** | Put an interface where transport varies. Keep domain decisions in the module; use the production transport adapter and a fake or in-memory adapter. Add contract proof when the remote contract carries risk. |
| **True external** | Put an adapter at the third-party seam. Keep vendor translation in the adapter and domain decisions in the module. Use the smallest fake, stub, or mock that proves the risk. |

## 2. Place

Place the narrowest seam earned by locality, dependency isolation, domain ownership, or real variation. Production plus a fake, substitute, emulator, or second integration demonstrates variation. Keep internal seams private and treat a test-only patch point as interface pressure.

## 3. Substitute

Choose substitutes by behavior risk, not convenience. Prove domain behavior through the deeper interface. Add separate substitute or production-adapter contract tests only when their fidelity or translation carries independent risk.

## 4. Replace, Don't Layer

Establish **coverage parity** through the deeper interface before removing shallow tests. Classify every affected test as **add, rewrite, keep, or delete**:

- **Add** caller-facing behavior proof that is missing.
- **Rewrite** behavior whose current test surface becomes obsolete.
- **Keep** dense rules, adapter contracts, regressions, or behavior not yet covered through the deeper interface.
- **Delete** pass-through, call-order, or implementation-detail assertions superseded by stronger behavior proof.

Assert observable outcomes through the interface callers use. A test that changes only because implementation changed is testing past the interface.

## 5. Migrate

Name the first behavior-preserving migration step, validation proof, stop boundary, and follow-ups. Keep the migration inside the bounded slice.

## Contribution To The Design Packet

Return the dependency classifications; seam, adapters, and substitutes; test disposition and coverage-parity evidence; bounded migration; validation proof; and stop boundary.

## Completion

Complete when every dependency is classified; seam and substitute choices match those categories; the proposed interface is smaller and useful; coverage parity accounts for every affected test; validation proof is named; and migration stops at the bounded-slice edge.
