# Fresh Composition Epochs Revalidate Skill-Pack Knowledge

Repeated skill deployments accumulated research packets, synthesis decisions,
validation records, campaign artifacts, and reused conclusions across changing
skill runtimes, source revisions, models, hosts, fixtures, and evaluation
protocols. Reusing that material by default risks compounding stale assumptions
and anchoring new research. Deleting it would discard provenance and useful
counterevidence. The one-skill Deploy Campaign also cannot by itself determine
whether the pack has the right skills, ownership boundaries, or composition.

**Status**: accepted

Per-skill campaign sequencing and research admission are superseded by
[ADR-0010](0010-deploy-campaigns-advance-through-proof-gates.md). The
pack-composition freeze, historical-by-default evidence policy, and Fresh
Composition Epoch boundary remain accepted.

A Fresh Composition Epoch is the pack-wide parent process for rebuilding
skill-pack knowledge. It freezes intended pack composition before inspecting
prior research, synthesis, validation, campaign conclusions, or current skill
bodies. It then:

1. creates a Pack Composition Contract for capabilities, skill essences,
   router, executable-aggregate, and leaf roles, boundaries, relationships,
   exclusions, collisions, gaps, and pack-level proof;
2. performs an M0-derived problem-first research pass without the local
   Research Catalog, records the independent methods and counterpressure, then
   uses the catalog as the first local research entrypoint;
3. permits at most one additional research pass for a named unknown that could
   materially change H1 admission;
4. runs one fresh Deploy Campaign per selected skill under the Pack
   Composition Contract;
5. proves pack-level routing, invocation, ownership, relationship, context-load,
   and end-to-end composition after the individual skills are proved; and
6. migrates or removes superseded material only after the new epoch reaches
   Lock.

Prior research, synthesis, validation, and campaign conclusions are
`historical-by-default`. They cannot seed independent discovery or carry
semantic decisions into the new epoch. After independent discovery, the owner
may classify an old artifact as `exact-reusable`, `method-evidence-only`,
`historical-admission-only`, `superseded`, `unverifiable`, or `duplicate`.
Behavioral evidence is rerun unless its complete claim, bytes, task, protocol,
model, host, configuration, tools, authority, evidence, runtime, rubric, and
proof-lane identity matches.

Research remains evidence authority, not adoption authority. The Research
Catalog indexes reusable Research Cards; per-skill synthesis alone decides
applicability and H1 admission. Validation owns exact behavioral proof and
tested bounds. Runtime skills remain compact executable authority. The Fresh
Composition Epoch coordinates these owners but does not become a pack-wide
Deploy Campaign or replace any one-skill campaign owner.

## Considered Options

- Reuse all prior artifacts unless they are visibly broken. Rejected because
  silent source, runtime, model, fixture, and judgment drift would enter new
  decisions before their applicability was tested.
- Delete prior artifacts and rebuild from an empty repository. Rejected because
  provenance, rejected alternatives, counterevidence, and exact reusable proof
  would be lost.
- Open the Research Catalog before external discovery. Rejected because known
  pack vocabulary and prior candidates would anchor the search. The catalog is
  first only within local research, after the independent problem-first pass is
  recorded.
- Let each one-skill Deploy Campaign infer the pack composition independently.
  Rejected because no one campaign owns cross-skill capability coverage,
  collisions, relationship topology, or pack-level integration proof.

## Consequences

- A fresh epoch costs more than resuming prior campaigns because behavioral
  proof and stale semantic decisions do not carry forward by default.
- "Best possible composition" means the strongest supported and behaviorally
  proved composition found under the frozen intended essence, explicit
  research bounds, and tested environment, not a universal optimum.
- Historical artifacts remain in place until reusable evidence is extracted,
  references are reconciled, and duplication or supersession is proved.
- A separately authorized topology migration must materialize the Research
  Catalog, Research Cards, Pack Composition Contract, skill-first research and
  validation layout, and reference updates.
- Exact card schemas, skill execution order, migration mechanics, and campaign
  automation changes remain implementation decisions under their existing
  owners.
