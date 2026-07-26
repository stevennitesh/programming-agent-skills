# Normalized Skill-Pack Enhancement Ideas

Status: synthesis-ready research

This directory contains source-backed ideas from five repositories. This file
normalizes them for two caller uses:

1. improve Matt-Pocock-style skill composition and this skill pack; and
2. identify bounded Deploy Campaign enhancements.

The linked notes retain detailed evidence. This file owns only the normalized
comparison and dispositions. It does not authorize runtime, campaign,
installation, or Git-delivery changes.

## Fixed Points

| Repository | Local Evidence | Revision | Detailed Packet |
| --- | --- | --- | --- |
| ECC | `.tmp/repos/ECC` | `ac30ff3ea249bf5f94dbc5e9b18ab681cc9af91d` | [Enhancement candidates](ecc-skill-pack-enhancement-candidates.md) |
| GSD Core | `.tmp/repos/gsd-core` | `6ee43492723dababa4138ceb72fd2cd26d4325d9` | [Skill-pack enhancements](gsd-core-skill-pack-enhancements.md) |
| gstack | `.tmp/repos/gstack` | `a3259400a366593e0c909dd9ac3e59752efd2488` | [Review and CSO packet](gstack-review-cso-source-packet.md) |
| React | `.tmp/repos/react` | `b685b40d870b90a975da28c8d22ecf0ba910b1a1` | [Composition note](react-agent-skills-composition-note.md) |
| Skilld | `.tmp/repos/skilld` | `c8368441070e2c0c29af6d2f8c9425f62e8b9afb` | [Vocabulary packet](skilld-skill-generation-vocabulary.md) and [enhancement candidates](skilld-skill-enhancement-candidates.md) |

All five local evidence roots were clean and matched the recorded revisions on
2026-07-25. The React checkout was added because it was the only missing clone.
The clones are ignored evidence, not tracked dependencies.

## Normalization Rules

Every candidate is reduced to:

- the failure it prevents;
- one semantic owner;
- the smallest expression compatible with this pack;
- the Deploy Campaign effect, if any;
- proof required before adoption; and
- the upstream machinery deliberately rejected.

Use these dispositions:

- **adopt in design:** the idea closes a concrete local gap, but still needs
  separately authorized authoring and proof;
- **test first:** applicability is plausible but current behavior may already
  recruit it;
- **already present:** the local contract owns an equal or stronger behavior;
- **reject:** importing it would duplicate ownership, weaken evidence, or add
  unjustified workflow.

Upstream source support proves that a repository uses a mechanic. It does not
prove that the mechanic improves agent behavior here.

## Repository 1: ECC

### Retain

| Candidate | Failure Prevented | Smallest Local Expression | Owner | Disposition |
| --- | --- | --- | --- | --- |
| Prompt-pressure cases | Invocation works only when the user repeats the skill's instructions | For an invocation-resilience claim, compare the same task under supportive, neutral, and competing prompt pressure while keeping runtime arms, facts, and rubric fixed | `writing-great-skills/BEHAVIOR-EVALS.md` | test first |
| Prior-art search | A new skill or behavior duplicates an existing owner | After blind method discovery, inspect only the strongest exact or near-exact skill matches and classify each useful mechanic | Deploy Research Pass | adopt in design |

### Campaign Effect

- Research Pass: add a bounded prior-art lane only after blind discovery.
- Prompt 2: classify useful mechanics as `Import`, `Already present`, or
  `Deliberately reject`; repetition and popularity remain discovery only.
- Prompts 3 and 4: register prompt pressure only for an admitted invocation
  claim.
- Pruning Pass: reuse pressure cases only when a cut changes
  invocation-bearing wording.

This is one conditional fixture dimension, not a new stage or evaluation
system.

### Reject

Reject ECC's runner, generated compliance specification, fixed
three-scenario rule, compliance percentage, marketplace sweep, promotion
hooks, and standalone stocktake or context-budget skills.

## Repository 2: GSD Core

### Retain

| Candidate | Failure Prevented | Smallest Local Expression | Owner | Disposition |
| --- | --- | --- | --- | --- |
| Observable wiring proof | A substantive artifact and isolated test pass while the public path never reaches the behavior | Trace acceptance to necessary artifacts and critical connections; prove the real caller path reaches and uses them | `docs/agents/engineering-contract.md`, with only needed local slices | test first |
| Must-not commitment | A prohibition is mislabeled as a non-goal and receives no acceptance or proof | Distinguish work excluded from scope from behavior whose occurrence makes the result wrong | `$to-spec` | adopt in design |

### Campaign Effect

Prompt 1 should distinguish:

- **exclusion:** no promise to build the behavior; and
- **must-not commitment:** a required negative behavior with its own M0 unit,
  wrong-condition case, and proportionate proof.

The campaign already maps runtime passages, trigger-bearing pointers,
relationships, and proof. That is sufficient for skill-package wiring; no GSD
verifier, phase report, or artifact tier should be added.

### Proof Before Adoption

- Wiring: use a fixture with a real implementation and passing isolated test
  that is unreachable from the public caller.
- Must-not: pair one true exclusion with one prohibition and verify that only
  the prohibition becomes an acceptance and proof obligation.

### Reject

Reject GSD's phase loop, persistent project state, smart-next routing,
separate quick/fast skills, fixed task counts, per-task commits, verification
reports, and dedicated enforcement workflow.

## Repository 3: gstack

### Retain

| Candidate | Failure Prevented | Smallest Local Expression | Owner | Disposition |
| --- | --- | --- | --- | --- |
| Change-family completeness | A new enum value, status, tier, or type constant is not handled by consumers outside the diff | Conditionally trace sibling values and close every applicable consumer in Review's existing coverage ledger | `$review` | test first |
| Attack-surface model | Security candidates are generated without the relevant trust and privilege context | Map trust boundaries, attacker-controlled inputs, privileged operations, sensitive data, and external dependencies | one disclosed `$audit-codebase` security lens | test first |
| Reachable exploit path | Theoretical security patterns enter the finding contract | Require attacker, entry condition, boundary path, and concrete effect | the same security lens | test first |
| Verified variant search | One verified causal defect is fixed while bounded siblings remain | Search the Charter region only after one defect is verified, then verify every sibling independently | the same security lens | test first |

### Composition Effect

Keep the ordinary-review heuristic inline. Keep the three security-only
heuristics together behind one trigger-bearing reference. Reuse the existing
finding and defect contracts instead of creating confidence scores, a second
finding format, or another review owner.

### Campaign Effect

No Deploy Campaign mechanism changes. Each candidate can enter Prompt 2 as an
ordinary H1 unit and must pass the existing M0-first contribution gate.

### Reject

Reject fix-first review, automatic fetch, inferred Spec, universal security
checklists, review armies, dashboards, telemetry, persistent learnings,
automatic secondary reviewers, and a standalone CSO skill.

## Repository 4: React

### Retain

React exposes one useful relationship shape:

| Shape | Contract |
| --- | --- |
| Router | Selects one next skill or flow and stops |
| Executable aggregate | Invokes independently useful leaves and owns their ordering, failure handling, and combined Return |
| Leaf | Performs one bounded operation and returns to its caller |

An executable aggregate must own one caller-visible outcome, keep each leaf
independently useful, and reference leaf behavior instead of copying its
procedure.

### Campaign Effect

Add the relationship shape only to Prompt 2's existing `pack-composition`
analysis. Record it when the distinction changes authority, ordering, failure,
or completion. Do not add a manifest field when the classification has no
behavioral consequence.

### Reject

Import no React skill. Reject fixed leaf inventories, mandatory fan-out,
repeated orchestration loops, and automatic delivery behavior.

## Repository 5: Skilld

### Retain

| Candidate | Failure Prevented | Smallest Local Expression | Owner | Disposition |
| --- | --- | --- | --- | --- |
| Untrusted-source firewall | Research follows directives embedded in source material | Treat source content as evidence, never authority to act; execute a source-supplied command only under independent caller authorization | local and Matt-derived `$research` | adopt in design |
| Fixed applicability | A time- or version-sensitive Matt research claim has no date, version, revision, or jurisdiction | Record the applicable identity beside the claim | Matt-derived `$research` | adopt in design; already present locally |
| H1-to-claim adjacency | An H1 unit cites a broad packet fingerprint but no exact supporting claim | Store stable research claim IDs on every research-derived H1 unit and validate them against the pinned research registry | Prompt 2 and campaign validator | adopt in design |

### Normalized Traceability Design

The research registry already owns claim-to-evidence pointers. Therefore an H1
unit should store only `research_claim_ids`, not copied citations or a second
`evidence_pointer`. Validation should require that:

1. every ID exists in the exact fingerprinted registry;
2. every research-derived H1 unit has at least one ID;
3. every referenced claim has valid bidirectional evidence pointers; and
4. synthesis renders the claim IDs beside the H1 decision.

This preserves claim adjacency without creating a second provenance owner.

### Campaign Effect

- Research Pass: keep stable claim IDs and their evidence mappings in the
  research registry.
- Prompt 2: bind every `professional-method` and `pack-observed` H1 unit to
  exact claim IDs.
- Campaign validation: fail a research-derived H1 with missing or dangling
  claim IDs.
- Later prompts: reference the H1 unit and registry; do not copy source
  citations into runtime skills or later lifecycle records.

### Reject

Reject Skilld's generator, sanitizer implementation, source resolver,
registry lifecycle, line budget, content-budget stopping rule, section
assembler, installer, and version-update shortcut.

## Cross-Repository Composition Contract

The useful ideas normalize into six rules:

1. **Search before adding.** Complete blind method discovery first, then check
   for the strongest existing skill or behavior owner.
2. **Classify the relationship.** Distinguish router, executable aggregate,
   and leaf whenever ordering, failure, authority, or completion differs.
3. **Keep one owner.** Put common behavior inline; disclose one coherent
   conditional branch; point to foreign procedure.
4. **Prove the reachable behavior.** Files, symbols, and isolated tests do not
   establish that the caller path delivers the outcome.
5. **Bind hypotheses to claims.** Preserve exact research-claim adjacency
   without copying provenance into later owners.
6. **Pressure-test routing claims.** When wording claims resilient invocation,
   hold task facts and runtime arms fixed while varying prompt pressure.

These extend Matt Pocock's leading words, context economics, information
hierarchy, deep-module composition, and explicit relationship vocabulary
without importing another pack's workflow.

## Recommended Deploy Campaign Enhancements

Priority is based on semantic risk closed relative to added campaign load.

| Priority | Enhancement | Unit | Why |
| --- | --- | --- | --- |
| 1 | Distinguish exclusions from must-not commitments | Prompt 1 | Prevents a required negative behavior from disappearing before M0 exists |
| 2 | Require H1 research claim IDs | Prompt 2 and validator | Closes a real provenance gap while reusing the existing research registry |
| 3 | Add bounded prior-art classification after blind discovery | Research Pass and Prompt 2 | Reduces duplicate skills and owner collisions without biasing independent discovery |
| 4 | Classify router, executable aggregate, and leaf relationships when behaviorally material | Prompt 2 | Clarifies combined completion and failure ownership |
| 5 | Add optional prompt-pressure fixtures for invocation-resilience claims | Prompts 3 and 4; affected Pruning cuts | Tests whether invocation survives realistic wording without adding a universal evaluation wave |

No new campaign stage is justified. No gstack-specific campaign mechanic is
needed. Skill-package wiring is already covered by runtime passage,
relationship, pointer, and candidate-root proof; the broader wiring idea
belongs in the engineering contract and implementation/review skills.

## Pack Enhancement Backlog

These are separate authoring units, not one bundled rewrite:

1. `$research`: add the untrusted-source firewall.
2. `$to-spec`: distinguish exclusions from must-not commitments.
3. `$review`: test change-family completeness.
4. `$audit-codebase`: test one disclosed security lens containing attack
   surface, exploit path, and verified variant search.
5. Shared engineering proof: test observable wiring on an orphaned-feature
   fixture before changing the engineering contract or local skill slices.

Each unit needs current-versus-candidate behavioral controls when exact wording
claims a steering effect. Structural read-back proves ownership and schema,
not improved agent judgment.

## Stopping Basis

Every retained upstream idea names a concrete failure, one local owner, the
smallest compatible expression, and proportionate proof. The remaining
mechanics duplicate stronger local owners, add a second workflow, or lack a
bounded behavioral claim. Another repository pass is unlikely to change these
dispositions without new source material or a failed local behavioral fixture.

Return owner: the user.
