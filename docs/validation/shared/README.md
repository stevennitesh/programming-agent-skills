# Shared Validation Contracts

This lane owns mechanical contracts reused across Fresh Composition Epoch
validation:

- `docs/validation/shared/protocols` owns shared protocols;
- `docs/validation/shared/fixtures` owns compatibility and negative-control
  fixtures; and
- `docs/validation/shared/schemas` owns the versioned schema registry.

`fresh-epoch-topology.json` records routing, owner, identity, compatibility,
and public/private invariants. It contains no semantic adoption or acceptance
decision.

The registered Pack Composition Contract schema and its pure controller expose
mechanical freeze, ordering, slice, amendment, and result-validation checks.
They do not select a pack or make semantic acceptance decisions.
