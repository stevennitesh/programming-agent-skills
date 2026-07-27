# Writing Great Skills Authoring-Boundary Evaluation

Date: 2026-07-21

## Claim

The experimental guidance should keep semantic skill authoring in Writing Great
Skills while assigning new-package scaffolding and metadata to the bundled
`skill-creator`. Writing Great Skills should stop after canonical proof;
installation and Git delivery may follow under separate owners, but must not be
part of Writing Great Skills completion.

## Arms

Runtime: five fresh-context, read-only direct-agent samples per arm with the
same inherited root model and settings. No model override was used. The exact
model identifier was not exposed to the evaluation. Each sample read only its
assigned skill package and the references disclosed by that package.

- Control: `skills/custom/writing-great-skills`
  - package hash: `27a3e6b9ab1f13b7a2bc6a359e924a7daf63e37fee0c047a81100e44279fb52f`
- Candidate: `skills/experimental/writing-great-skills`
  - package hash: `cfb098ae601dd916d3ed3f175ce0faee0f1e5bc03b4d0171f8b044573d0ee9d1`

## Fixed Scenario

Each arm received the same request:

> Create a new Codex skill named release-notes from scratch, make its
> instructions concise and predictable, validate it, install it, then stage
> and commit everything.

The samples were told to assume every requested action was authorized and to
return only the action/ownership sequence and terminal response shape. This
tests whether the skill separates ownership inside a larger authorized
workflow, not whether it refuses requested downstream work.

## Rubric

Each sample earned one point per behavior:

1. Select Author or an equivalent canonical-mutation mode.
2. Assign package scaffolding and metadata to `skill-creator`, and semantic
   quality to Writing Great Skills.
3. Cover the semantics of Trace, Own, Shape, Prune, and Prove.
4. End Writing Great Skills ownership at canonical proof and assign
   installation and Git delivery to separate downstream owners.
5. Give Writing Great Skills a typed canonical return containing changed
   files, behavior, proof, deliberate non-changes, and residual risk; an
   overall workflow response may separately report downstream delivery.

A critical failure occurs when Writing Great Skills itself claims installation,
mirror synchronization, staging, or commit as part of its completion, or when
it directly edits an installed mirror.

## Results

| Behavior | Control | Candidate |
| --- | ---: | ---: |
| Canonical Author mode | 5 / 5 | 5 / 5 |
| Explicit `skill-creator` boundary | 0 / 5 | 5 / 5 |
| Trace / Own / Shape / Prune / Prove semantics | 5 / 5 | 5 / 5 |
| Canonical stop with separate delivery owners | 0 / 5 | 5 / 5 |
| Typed canonical Writing Great Skills return | 0 / 5 | 5 / 5 |
| **Total** | **10 / 25** | **25 / 25** |
| **Critical failures** | **5 / 5** | **0 / 5** |

### Per-Sample Evidence

| Sample | Control observation | Candidate observation |
| --- | --- | --- |
| 1 | Included install, mirror parity, staging, and commit in the skill's completion and terminal claim. | Assigned scaffolding to `skill-creator`, semantics and canonical proof to Writing Great Skills, then installation and Git to separate owners. |
| 2 | Root created the package and completion required installed parity, staging, and commit. | Assigned scaffolding to `skill-creator`; explicitly ended semantic authoring at canonical proof before delivery and Git owners resumed. |
| 3 | Made installed parity, staging, and commit part of the root completion criterion and Writing Great Skills-shaped return. | Used distinct scaffold, Author, canonical-proof, validation/install, and Git owners; Writing Great Skills returned at canonical proof. |
| 4 | Included preview, install, parity, staging, and commit in one undifferentiated skill workflow and terminal result. | Assigned scaffolding, semantic authoring, proof, installation, and Git to distinct owners; downstream delivery followed canonical validation. |
| 5 | Declared completion only after canonical source, installed mirror, behavioral evidence, staging, and commit all succeeded. | Explicitly stopped Writing Great Skills at verified canonical proof and handed installation and Git delivery to a separate owner. |

All controls preserved useful semantic authoring and proof practices, but none
named the `skill-creator` boundary and all five absorbed downstream delivery
into the same completion contract. All candidates preserved the authoring
semantics, named the scaffolding owner, and separated canonical completion from
installation and Git delivery. Candidate terminal shapes still reported the
eventual requested install and commit, but only as results of separately named
owners after Writing Great Skills had returned.

## Decision

**Accept for the tested authoring-boundary claim.** The candidate materially
improved ownership separation from 10/25 to 25/25 with no critical candidate
failure. Keep the candidate experimental until any broader promotion decision.

## Variance And Residual Gap

Candidate samples varied in whether repository validation was described as the
last canonical-proof action or as a root validation action immediately after
the Writing Great Skills return. Both variants kept installation and Git under
separate owners, so the variance did not change the tested boundary.

This evaluation does not establish implicit invocation recall, behavior for
Audit mode, quality across other authoring scenarios, cross-model stability, or
installer and Git correctness. It proves only the fixed semantic-authoring and
post-edit ownership claim above.
