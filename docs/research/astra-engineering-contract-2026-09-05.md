# Astra engineering contract and bootstrap

Date: 2026-09-05. Source-based design assessment and implemented candidate.
No behavioral comparison was run. This note does not replace the active contract
or authorize installation of the candidate.

## Recommendation

Rewrite the contract selectively. Its design judgment is already useful; the
main gains are qualifying broad rules and making verification more discriminating.
Keep shared judgment in one repository-owned contract, facts and pointers in
repository instructions, and setup procedure in repo-bootstrap. Global guidance
should retain only cross-repository preferences and discovery.

The candidate is [repo-bootstrap](../../skills/astra/repo-bootstrap/SKILL.md),
with an [engineering contract seed](../../skills/astra/repo-bootstrap/templates/engineering-contract.md).
The existing active contract, custom package, installation, and global guidance
remain unchanged. Astra is outside the current managed install set.

## Local evidence

- The [current contract](../agents/engineering-contract.md) already covers
  subtraction, domain shapes, schema derivation, root causes, proportional proof,
  migrations, and conditional protection. These deserve retention.
- The [Astra assessment](gpt-6-astra-skill-pack-assessment-2026-09-05.md) identifies
  caller semantics, discriminating examples, real producer-consumer proof,
  evidence validity, and effect ownership as useful retained knowledge.
- [Implement](../../skills/custom/implement/SKILL.md) makes those proof concerns
  concrete. The candidate extracts their general decision rules without copying
  the detailed case inventory or ticket workflow.
- [GSD source intake](skill-pack-composition/sources/SRC-0003.md) identifies
  orphaned implementation as a proof gap. This is a candidate rationale, not
  demonstrated efficacy; the suggested comparative experiment was not run here.
- [UBL-24](language/validation/UBL-24-final-correction-decision.md) distinguishes
  exploratory probes from completed slices and grounds staged migration in real
  coexistence needs. It explicitly leaves behavioral claims untested.
- [Historical bootstrap synthesis](../synthesis/skills/repo-bootstrap.md)
  explains preservation and read-back controls, but its exact-delta approval
  loop belongs to the old workflow. The new candidate preserves local ownership
  without importing that approval loop for already authorized edits.

## Upstream evidence and dispositions

Inspected the refreshed local snapshots below. These are source comparisons,
not a new remote refresh or reproduction of upstream experiments.

| Source snapshot | Useful material inspected | Candidate disposition |
| --- | --- | --- |
| Matt Pocock `3cca18b368ae95cdbdebbff572ccafa662551015` | `skills/engineering/codebase-design/SKILL.md`; `setup-matt-pocock-skills/SKILL.md` | Keep caller-visible interface semantics and the abstraction deletion test. Preserve existing setup choices. Omit compulsory tracker scaffolding and repeated confirmation. |
| Pstack `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Principle skills for boundaries, types, proof, shared state, idempotency, structural enforcement, and migrating callers | Keep valid representations, actual artifacts, state ownership, recovery, and scoped migration. Qualify unconditional internal trust and automatic structural-fix campaigns. |
| Superpowers `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | `skills/verification-before-completion/SKILL.md` | Keep evidence matched to claims. Reuse still-valid evidence instead of requiring a full fresh command in every message. |
| Ponytail `974d940a1c5344210874150b98ff0d2c861fab6a` | `skills/ponytail/SKILL.md` | Keep reuse and root-cause repair. Omit persistent personas, intensity modes, and shortest-code rules. |

## What changed and why

| Decision | Failure it addresses |
| --- | --- |
| Include error, ordering, and state semantics when designing interfaces | A simple signature can still hide a difficult or unsafe caller contract. |
| Qualify reliance on types and validated data | Mutation, stored data, and concurrent writers can break a once-valid invariant. |
| Make meaningful partial outcomes and failures explicit | Fallbacks can silently report incomplete work as success. |
| Use counterexamples and independently derived expected results | A test can reproduce the implementation's mistake. |
| Exercise actual output through affected integrations | Files and isolated helpers can pass while real users cannot reach the behavior. |
| Reuse evidence according to its dependencies | Message boundaries are not a reason to rerun unchanged checks. |
| Name resource ownership and real shared state | File isolation alone does not protect shared services or cleanup on failure. |
| Reconcile setup directly within existing authority | Setup should not force a second approval for the same requested local edit. |

The contract remains guidance rather than a universal checklist. Detailed tracker,
domain, language, and deployment procedures stay with their owners. No new
validator, managed marker scheme, global template, or evaluation framework was
introduced. Bootstrap treats its seed as input to a repository-owned document,
so rerunning it should reconcile rather than overwrite local choices.

## Validation limits

Package validation and local link checks can establish packaging and pointer
integrity. They do not establish better coding outcomes. First use should inspect
the generated diff for preserved repository policy, supported commands, a usable
contract pointer, and absence of duplicate instructions. A comparative efficacy
claim would require separate behavioral evidence.
