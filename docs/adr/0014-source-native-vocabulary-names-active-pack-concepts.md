# Source-Native Vocabulary Names Active Pack Concepts

The active pack accumulated local labels that now obscure established
configuration-management, verification-and-validation, catalog, and testing
meanings. In particular, `Lock` names several different actions, `Release`
names a canonical-source promotion that performs no distribution, and `Deploy
Campaign` names a controllerless authoring method that performs no deployment.
The Pack Composition artifact and evidence index are now materialized, so their
current behavior can be named more precisely without changing their authority.

**Status**: accepted

## Decision

Active human-facing vocabulary uses established terms when they preserve the
repository behavior:

- **Pack Composition Baseline** replaces Pack Composition Contract.
- **Evidence Catalog** and **Evidence Record** replace Research Catalog and
  Research Card.
- **Skill Change-Control Method** replaces Deploy Campaign.
- Its four ordered obligations are **Define and Authorize Change**, **Baseline
  and Verify Candidate**, conditional **Validate Behavior**, and **Promote
  Canonical Skill**.
- **Traceability** replaces Source Trace in human-facing runtime language.
- **Repository-owned proof mechanism**, or the concrete fixture, check,
  workflow, or artifact, replaces Proof Lane.
- **Removal condition** replaces Removal Trigger.
- The phrase “smallest repository-native path through the current behavior
  owner and real callers” replaces Integrated shape.
- Generic capitalized `Lock` is retired from shared vocabulary. Each owner names
  the actual action: define, authorize, baseline, freeze, verify, record
  acceptance, promote, or close out.

Use **verification** for conformance to specified deterministic requirements
and **validation** for intended behavior or effect.

Fresh Composition Epoch, Proof Seam, and Change Closure remain repository-local
terms because each compresses a distinct behavior that the established
alternatives do not preserve. The Fresh Composition Epoch is a pack-wide
evidence reset and recomposition boundary. A Proof Seam is the caller-facing
boundary where meaning is verified, not the test that exercises it. Change
Closure removes or justifies displaced, redundant, or contradictory paths.

Stable machine identities remain compatible: existing schema IDs, v1 paths,
module names, `RC-*`, `FCE-*`, `source_trace`, and `epoch_lock` identifiers are
not renamed by this decision. Historical ADRs, research, validation, synthesis,
and run evidence retain the vocabulary they recorded.

The marker-bounded Pack Composition payload is a frozen accepted baseline.
Replacing embedded legacy vocabulary requires a revision-plus-one amendment and
regeneration of affected semantic fingerprints and integration evidence. Until
that migration completes, legacy tokens in active machine contracts are
compatibility aliases, not preferred human-facing terms.

This ADR supersedes only the nomenclature in ADR-0009 and ADR-0010. Their Fresh
Composition Epoch boundary, historical-by-default evidence policy,
controllerless method, proof ordering, authorities, and stopping behavior
remain accepted.

## Considered Options

- Retain every local label. Rejected because overloaded `Lock`, `Release`, and
  `Deploy` language hides materially different responsibilities.
- Rename machine identifiers and historical evidence immediately. Rejected
  because it adds compatibility work without changing current behavior and
  would rewrite provenance.
- Replace every repository-local term. Rejected because Fresh Composition
  Epoch, Proof Seam, and Change Closure carry narrower behavior than the
  available established alternatives.
- Enforce preferred language through validators. Rejected because validators
  own machine-checkable publishing and structural hygiene, not prose style.

## Consequences

- `CONTEXT.md` owns the preferred pack vocabulary and compatibility boundary.
- The canonical engineering contract will own Traceability and the remaining
  shared runtime-language changes when its two managed copies are updated
  atomically.
- Active method, skill, test, and documentation callers migrate under their
  existing owners; historical artifacts remain unchanged.
- `docs/synthesis/skill-pack.md` is recognized as the current Pack Composition
  Baseline owner rather than an artifact still awaiting materialization.
- No vocabulary rename changes routing, authority, completion, Return, proof,
  installation, or Git-delivery behavior by itself.
