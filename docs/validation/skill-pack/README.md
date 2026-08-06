# Pack-Integration Validation

`docs/validation/skill-pack` owns structural and behavioral evidence for one
`FCE-YYYYMMDD-NN` composition epoch. It records protocols, fixtures, results,
tested bounds, and residual gaps; it cannot accept the pack or declare Lock.

Before campaigns begin, an epoch directory may also contain a frozen
`schedule.json` and immutable `slices/*.json` blueprints. They prove contract
projection, fingerprints, predecessors, and acyclic order only; they do not
prove campaign readiness or behavioral efficacy.

Each epoch keeps shared inputs as separate protocol, rubric, fixture, and
tested-bound artifacts. `integration-manifest.json` stores only exact
identities, deterministic check registrations, receipts, invalidations, and
parity. `results.json` is mechanical evidence returned to the Fresh Composition
Epoch owner; pack synthesis alone interprets it.

Run the pure verifier with:

```text
python -m scripts.pack_integration <integration-manifest.json> --installed-root <managed-skill-root> --result <results.json>
```

The verifier derives coverage for all ten gates, independently derives each
terminal campaign's canonical admission slice, runs one verifier-owned,
gate-specific structural profile for each gate, and binds receipts to the exact contract,
campaign, relationship-index, managed-install-manifest, and installed-tree
identity. The installed root is an explicit runtime input and may be outside
the repository. Behavioral
evidence must preregister its protocol, rubric, fixtures, controls, repetitions,
variance, and environment bounds; the verifier checks those identities but
never reads or scores the rubric or samples. It cannot accept the pack, repair
or schedule a campaign, choose behavior, or declare Lock.

The exposed gates are:

1. contract and pointer integrity;
2. capability, authority, and mutation ownership;
3. positive, nearest-negative, and collision invocation;
4. relationship entry, wrong condition, Return, resume, and non-execution;
5. success, material failure, and completion paths;
6. context budgets and foreign-procedure absence;
7. minimal-workflow coverage across capabilities, roles, and relationships;
8. canonical, installed, manifest, and relationship parity;
9. zero unresolved essential gaps or critical collisions; and
10. behavioral evidence and validator negative controls.
