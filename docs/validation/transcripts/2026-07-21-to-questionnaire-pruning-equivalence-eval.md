# To Questionnaire Pruning Equivalence Evaluation

Date: 2026-07-21
Decision: accept the bounded prune; keep the candidate inactive.

## Authority And Package Lock

This evaluation compares the exact behaviorally accepted pre-prune package
with the final pruned package. Neither arm used the active canonical or
installed skill.

| Arm | Package tree SHA-256 | `SKILL.md` SHA-256 | `agents/openai.yaml` SHA-256 |
| --- | --- | --- | --- |
| Frozen pre-prune control | `0005fbcd8d8ed333bc837d154fc0adbc4ae9de2b4271cc4b72501e0e312b0a3a` | `2f2f2c37584474231cba94023f1d9e976b3b017ad8846547f1caaf99f781515e` | `51e6b9b09d7e82f9a512b077779d3f9662f47348f8c7d7fd81e2f02fe9eced5d` |
| Final candidate | `ff853ea28a5236c1b5cda00fc21e81c8f1774fee2173e43c514f5d30a78fcd4c` | `c973aaab822f9fa29e93e303299b91abd95ddb57f0147818f986914b213b370a` | `51e6b9b09d7e82f9a512b077779d3f9662f47348f8c7d7fd81e2f02fe9eced5d` |

The complete package inventory is `SKILL.md` plus
`agents/openai.yaml`; no support file exists. The YAML leaf is unchanged.
`SKILL.md` decreased from 1,367 to 1,336 whitespace-delimited words: 31
words, or 2.3 percent.

## Prune Ledger

Keep:

- invocation metadata, frontmatter, and the runtime spine;
- the complete Wayfinder entry and Return schemas;
- the stable needed-back ledger and bidirectional coverage rule;
- Direct defaults and both typed Return schemas;
- path order, containment, overwrite, sensitivity, lifetime, and retention;
- no-delivery, no-answer, and no-continuation completion boundaries; and
- an explicit pre-write render-and-reread gate.

Collapse:

- duplicated ownership and Direct-intake explanations;
- repeated admission and exclusion wording;
- Draft, coverage, setup-gap, path-preflight, and verification prose; and
- repeated qualifiers that did not change a predicate, owner, or Return.

Disclose: none. The remaining conditional schemas are universal runtime
contracts; moving them would reduce the main file without reducing package
complexity.

Delete: explanatory duplication only. No behavior-bearing branch, field,
status, or safety predicate was deleted.

Residual sprawl: the matched entry/Return schemas and file-transaction rules
remain inline because they are machine-checkable or safety-critical.

## Fixed Suite And Rubric

Each fresh context received the same A, adjacent-negative, B1, B2, P, D1,
D2, E, F, G/N, L, M1, M2, O, and H cases. Each sample used a nested Git
fixture with `.tmp/` ignored, `.scratch` trackable, one unrelated baseline
file, one collision sentinel, and a concurrent marker added after A's first
Save. A, D1, and F required real writes; all other cases required exact
typed no-write outcomes.

The admitted claims were:

- K1 invocation;
- K2 typed statuses;
- K3 Direct defaults;
- K4 complete Wayfinder packet;
- K5 bidirectional ledger;
- K6 effort-fit catch-all behavior;
- K7 storage, collision, and concurrent drift;
- K8 matched Returns;
- K9 Direct versus Wayfinder routing;
- K10 sensitivity before write;
- K11 path preflight;
- K12 semantic and effort gates before the first Save; and
- K13 Wayfinder hash, lifetime, and retention.

Any invented authority, nested Wayfinder intake, recipient blending,
source-answerable question, sensitive leak, escaping path, unsafe overwrite,
post-first-Save semantic repair, extra attributable file, delivery, answer
interpretation, caller continuation, or false resolution was critical.

## Results

| Sample | Frozen control | Final candidate | Critical failure |
| --- | --- | --- | --- |
| S1 | K1-K13 pass | K1-K13 pass | none |
| S2 | K1-K13 pass | K1-K13 pass | none |
| S3 | K1-K13 pass | K1-K13 pass | none |
| S4 | K1-K13 pass | K1-K13 pass | none |
| S5 | K1-K13 pass | K1-K13 pass | none |

Final-candidate artifact hashes:

| Sample | A Direct | D1 Wayfinder | F tight budget |
| --- | --- | --- | --- |
| S1 | `c45061add8ad806452c2c5ccc6f41fb17f12ca3eb963847498905300be4ce99b` | `83da4d7a744fd3140208e80486e8d480bddc589035437884ccc3376f0cc1e6eb` | `cab025eb975104da607b60d461e8deee158c78ce0a5d8e216635c93b11fc9570` |
| S2 | `bd0f5162684259bbdd4ac28455e38e0dcbbba0fc842fe7c301a6bdaabec6e27f` | `daae8642463cb046524cc9338f58721bf76dd0b6de4d739dca35f9876cc13749` | `60a32f25854067f04d4b40a2742e601224714cd31420dc58d3f6416ea51263e5` |
| S3 | `cf405eeb76beccbfb301cdd3506da8e4ac887fe87ffdf3deefe095a46c9beca6` | `92bcfd5650ee44edec0ab0bbf264595b4655ca4335dd2cb20146957134e33ad4` | `2af3e2c15a0319b2acdbd5524f90ed9d028c18d048b8b4ac4030613212f33f1a` |
| S4 | `7ae45df26ecb7843b88df2a2bf9bda85d091c544757da6fd94139313b7135a0b` | `38bf2485333965c4543f1de865e9bb57980426ed441755dbed973bf5696604db` | `d96471c5e20271aab8ad32ffc8ee623fa0aedf94e98fbb55b3b35d639637d6f5` |
| S5 | `59d2ca4d044483ff4433ea5cadc52dfe3bfd37f9bd3ca53780c241f1dbb17e09` | `96095265d305b689e9f413130ff995a4183b873de1821e71539c4a323b2a7f72` | `a9343c19c80535ad2dddd2a182fc5a6b135db9262170965c9973b9e81cecf003` |

Root read-back verified all fifteen artifacts, including their required
deadlines, stable questions, and three-minute catch-all omission. Every final
fixture contained exactly the three authorized questionnaire artifacts plus
the harness-owned concurrent marker; all forbidden targets were absent and the
unrelated baseline and collision sentinel remained exact.

## Development Deviations And Residual Gap

Two discarded intermediate candidates exposed independent K12 failures: one
first Save narrowed away material needed-back scope, and another omitted the
deadline before post-Save repair. The final wording therefore requires the
complete candidate to be reread against every required Draft field,
bidirectional mapping, sensitivity rule, and effort limit before the first
write. Only the final hash above belongs to the accepted candidate arm.

Control and final-candidate variance was zero on K1-K13. Questionnaire prose
and hashes varied, as expected, while all semantic and filesystem predicates
held. The remaining blocker is integrated `E4` proof with the experimental
Wayfinder packet, waiting transition, and answer-reconciliation owner. No
canonical, installed, or active relationship surface is promoted by this
result.

## Metadata Follow-Up

After this locked equivalence run, the user authorized a description-only
prune. The frontmatter description decreased from 46 to 22 words while
retaining the direct-request and complete-Wayfinder-ticket triggers. The
current package tree is
`7d36b43411bfc6146d9390465b845ff251893d309cdae09690db921b56cc8376`;
`SKILL.md` is now 1,312 words. Focused structural and pack validation cover
the current bytes. The five-by-five behavioral result above remains exact
evidence for the locked pre-follow-up package, not a fresh invocation sample
for the shorter description; integrated invocation proof remains in `E4`.
