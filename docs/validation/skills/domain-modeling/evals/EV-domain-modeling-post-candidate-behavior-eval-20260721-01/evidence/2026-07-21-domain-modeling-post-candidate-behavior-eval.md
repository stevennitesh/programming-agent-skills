# Domain Modeling Prompt 4 Behavioral Evaluation

Date: 2026-07-21

Decision: **ACCEPT the experimental candidate for Prompt 5 promotion**

Runtime status: inactive; canonical and installed Domain Modeling were not changed.

## Locked Packages

| Role | Package | SHA-256 tree hash |
| --- | --- | --- |
| Simplest baseline | `.tmp/mattpocock-skills/skills/engineering/domain-modeling/` | `ce2eb764d4d47a9bf39e54832a32ac11761cfb25cb523a5560f7474dd3dda430` |
| Canonical baseline, used only for the Router-removal claim | `skills/custom/domain-modeling/` | `599a98910c7b392d54e595331d114ec4e101dffe251d277ed5067b308602e045` |
| Prompt 3 candidate | `skills/experimental/domain-modeling/` before Prompt 4 repair | `a52648ce0f314980e3ede15214c10800b3b89268f70138b40eee61ae62c1c272` |
| Repaired pre-prune control | `docs/validation/evals/domain-modeling-pre-prune-cfea0f22/` | `cfea0f22106e4a8ec231912afadd09ca717189dcb4b53eadb6ec19bdde44c6e0` |
| Final pruned candidate | `skills/experimental/domain-modeling/` | `88413f471ffcedccdf8b4b3a162a3068334c7befbcd28801165add6d29e8941b` |

The pre-prune fixture differs from the final candidate only in the longer explicit list of foreign consequence owners in `SKILL.md`. Both include the same Prompt 4 authority and pattern-selection repairs.

## Audit, Repair, And Prune

The complete experimental package inventory was `SKILL.md`, `CONTEXT-FORMAT.md`, `ADR-FORMAT.md`, and `agents/openai.yaml`. Every instruction-bearing unit was reclassified against its owner, evidence, cheaper alternative, and cut test.

Two genuine omissions were admitted and repaired:

1. Direct invocation did not identify the direct user as default meaning authority when no source named another authority.
2. The Context Mapping reference named accurate patterns but did not prevent organizational dependence from being mislabeled as Conformist or a versioned schema from being mislabeled as Open-host Service.

One safe collapse remained after repair:

- Pre-prune: enumerate setup, code, spec, plan, tracker, and implementation consequences.
- Final: `Return every other consequence or residual to its owner and stop.`

No admitted mechanism was deleted. Branch mechanics remain disclosed in their two reference files; the runtime spine, authority, mutation modes, common Return, completion rule, and composition boundary remain in `SKILL.md`. Residual unavoidable load is the recognized Context Mapping vocabulary and universal ADR mechanics required by confirmed DDD and ADR contracts. The candidate is larger than the Matt baseline because it owns persistence safety and local composition contracts; no raw word-count target was used.

## Claim-To-Proof Matrix

| Claim | Control | Fixed case | Root-held pass condition |
| --- | --- | --- | --- |
| Narrow implicit routing | Matt metadata | R1-R4 | Lookup and general design stay out; durable meaning capture and settled ADR assessment route in |
| Repository routing and direct clarification | Matt package | A | Use configured record, treat code as evidence, render without inventing fallback files |
| Verified persistence and separate ADR approval | Matt package | B | Persist authorized domain truth, reread, expose code contradiction, create no ADR |
| Accurate optional patterns | Matt package | C | Published Language plus Anticorruption Layer only; Translation is a language mapping |
| Partial-failure Return | Matt package | D | Preserve verified work, stop, report exact target states, owner, impact, and re-entry |
| Composed questioning ownership | Matt package | E | Return cumulative delta before continuation; Grilling owns the next question |
| Leaf completion | current canonical | F | Return residual and stop without Router or downstream invocation |
| Pruning equivalence | repaired pre-prune fixture | G | Return every unauthorized consequence to its owner, include setup re-entry, and stop |

Case A's control already passed and therefore supplies no behavioral-improvement credit. Its candidate wording remains as a repository ownership and fallback contract. The Matt control also avoided unauthorized ADR creation; separate ADR approval is retained as a protected safety and relationship contract, not credited as an observed improvement.

## Neutral Protocol

Each arm used five fresh, isolated workers with no descendants and no mutation authority. Workers received fixed facts and a request for one compact action-and-Return packet. Expected behavior, candidate wording, conclusions, rubrics, validation evidence, synthesis, tests, manifests, peer output, and the other arm were withheld. Metadata routing was locked before assigned-package reading. The root judged all returns.

Exact model identifier, reasoning setting, token count, latency, and cost were unavailable. Workers inherited the session runtime and had read-only package access. Because the cases simulated persistence rather than mutating a disposable repository, filesystem effects remain a residual evidence gap.

## Control Locks

Workers: `dm_control_1` through `dm_control_5`.

| Case | Per-sample result | Pass rate | Lock |
| --- | --- | --- | --- |
| R1 ordinary lookup | P P P P P | 5/5 | Healthy default; preserve |
| R2 settle and persist term | P P P P P | 5/5 | Healthy default; preserve |
| R3 REST versus GraphQL | P P P P P | 5/5 | Healthy default; preserve |
| R4 settled ADR assessment | 2 P, 3 F | 2/5 | Control failure exposed |
| A configured path/direct clarification | P P P P P | 5/5 | No improvement claim admitted |
| B persistence verification | 1 P, 4 F | 1/5 | Read-back/complete Return failure exposed |
| C Context Mapping | F F F F F | 0/5 | All treated Translation as a pattern |
| D partial failure | 2 P, 3 F | 2/5 | Complete blocker/impact/re-entry failure exposed |
| E composed callbacks | 2 P, 3 F | 2/5 | Question ownership ambiguous or wrong |
| F canonical leaf Return | F F F F F | 0/5 | All invoked implicit Skill Router |

For rows recorded only as counts, the root's contemporaneous judgments preserve every sample outcome but the compact ledger does not assign the pass subset to worker number. No conclusion depends on that assignment.

## Initial Final-Candidate Arm

Workers: `dm_candidate_1` through `dm_candidate_5`. Package hash before the pattern repair was `d793b1771b59970a2369b7431657449864cd1689113aa91608ae24d794d93770`.

| Case | Samples 1-5 | Result |
| --- | --- | --- |
| R1-R4 | P P P P P for every route | 5/5; R4 improved from 2/5 |
| A | P P P P P | Baseline behavior preserved; no improvement credit |
| B | P P P P P | Verified reread, no code edit, no unauthorized ADR |
| C | P P F F F | **Critical failure:** false Conformist; sample 5 also false Open-host Service |
| D | P P P P P | Partial state and re-entry complete |
| E | P P P P P | Grilling retained question ownership |
| F | P P P P P | Leaf Return; no Router or downstream work |
| G | P P P P P | Initial pruning equivalence 5/5 |

Acceptance paused on Case C. The narrow repair added selection tests to `CONTEXT-FORMAT.md`: translation into a distinct local model establishes Anticorruption Layer rather than Conformist for that interaction, and a versioned schema alone does not establish Open-host Service. No confirmed decision changed.

## Affected-Arm Rerun

The repair changed both the final package and the exact repaired pre-prune fixture. Unchanged baseline controls and unaffected candidate cases were preserved. Only Context Mapping and pruning equivalence were rerun.

| Arm | Workers | Case | Samples 1-5 | Result |
| --- | --- | --- | --- | --- |
| Repaired pre-prune | `dm_preprune_repair_1` through `_5` | G | P P P P P | 5/5 |
| Final candidate | `dm_candidate_repair_1` through `_5` | C | P P P P P | 5/5; Published Language + Anticorruption Layer only |
| Final candidate | same five contexts | G | P P P P P | 5/5; pruning outcome equivalent |

The earlier pre-prune G wave also passed 5/5. It was superseded for hash identity after the Context Mapping repair, not because of a behavioral failure.

## Judgment

Accepted. The worst final result is 5/5 on every eligible candidate case, with zero critical failures after the narrow repair. The final prune preserved its admitted outcome at 5/5 versus 5/5. Mechanical package validation and repository tests are recorded at handoff.

Residual gaps:

- persistence and permission failure were simulated; no disposable filesystem target was mutated;
- Context Mapping accuracy was tested with one high-risk translation scenario, not every recognized pattern;
- implicit invocation was evaluated as catalog routing choice, not autonomous production telemetry;
- exact runtime cost and latency telemetry were unavailable.

These gaps do not reverse the observed claims, but promotion must preserve the exact final candidate bytes. Any behavioral change requires a new affected-arm evaluation.

## Mechanical Proof

- Focused experimental contract tests: `9 passed`.
- Full repository suite: `191 passed, 4 skipped`.
- Skill-pack validation: passed after evidence formatting repair.
- Candidate tree hash equals the experimental manifest hash.
- Repaired pre-prune fixture tree hash equals its recorded identity.
- Canonical Domain Modeling diff: empty.
- Worktree and staged whitespace checks: passed.
