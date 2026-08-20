# Deepening

Load this reference only when dependency shape changes seam placement,
substitution, testing, or migration. `SKILL.md` owns the architecture decision.

## Place the seam

Classify only dependencies that can change the design:

- **In-process:** keep computation and memory inside the module unless distinct
  ownership or change rates justify separation.
- **Local-substitutable:** use a realistic local implementation when it proves
  the required behavior without widening the public interface.
- **Remote-owned:** keep domain policy local and isolate transport where it can
  vary independently.
- **True external:** isolate vendor translation at the third-party edge.

Place the narrowest seam earned by production behavior, ownership, supported
variation, or a real external boundary. Do not expose an internal seam or add
dependency injection only to make testing convenient.

## Prove through the interface

Use the deeper caller-facing interface as the normal proof boundary. Test an
internal rule directly only when it has independent meaning. Add separate
adapter or substitute proof only when fidelity, translation, or interchange
carries its own risk.

When stronger caller-facing proof covers the same meaningful behavior, remove
obsolete pass-through and implementation-detail tests. Keep distinct rules,
regressions, boundary contracts, and necessary failure isolation. Do not create
a test census or parallel proof owner merely to document the migration.

## Move callers and remove the old path

Name the first bounded caller migration and the proof that preserves accepted
behavior. Remove displaced implementations, exports, registrations, tests,
configuration, and documentation in the same supported change. Retain an old
path only for a demonstrated external compatibility, migration, recovery, or
ownership need with a removal condition.

Return the seam decision, relevant dependency consequences, caller migration,
and proof to `SKILL.md`.
