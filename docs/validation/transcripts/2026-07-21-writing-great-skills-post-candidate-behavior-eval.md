# Writing Great Skills Post-Candidate Behavioral Evaluation

Date: 2026-07-21

## Decision

**Accept the inactive experimental candidate** at tree hash
`9822b2eb486e7e4a31589cd02a0667981639ef3c2df810da3d6945f6e650f77c`.
The candidate materially improved the failures exposed by the refreshed
upstream baseline, matched the admitted pre-prune package in every fixed case,
and introduced no observed critical failure. Acceptance is not promotion; the
canonical package, installed mirror, callers, and delivery state remain
unchanged by Deploy Prompt 4.

## Commit Preflight Normalization

The sampled hashes above remain the exact Prompt 4 arms. Before Git delivery,
the staged whitespace check found one trailing blank line in each of the
candidate's `GLOSSARY.md` and `BEHAVIOR-EVALS.md`. Removing only those blank
lines changed the candidate tree hash to
`c7c02f4f9896cd5bf6e6c25886e77785a9f80c0ccea0d02f7aaa6fc85076dcc4`
without changing any instruction-bearing text.

The same preflight found that the frozen fixture's three copied support files
had been decoded through the console instead of copied from UTF-8 source bytes.
They were rebuilt from the candidate source bytes and normalized to one final
newline. Their normalized text now matches the candidate support files exactly;
the pre-prune `SKILL.md` is unchanged. The corrected fixture hash is
`23fb951a230df6c929803f02d3ad16586471a14f4169632eddaf39c725c34bc2`.
The current packages contain 304 lines and 3,716 words for the candidate and
400 lines and 4,039 words for the pre-prune control.

These are encoding and EOF repairs, not a new behavioral candidate. The fixed
tasks, gates, pointers, policy, and rubric remain identical, so the Prompt 4
acceptance transfers to the normalized current candidate without another
behavioral wave.

## Authority And Refreshed Baselines

Prompt 4 used Writing Great Skills in Author mode only for the inactive
candidate, its isolated evaluation fixture, this evidence record, and the
directly affected synthesis. It authorized no canonical edit, relationship
migration, installation, promotion, or Git delivery.

Live fetch on 2026-07-21 confirmed the simplest credible baseline remains Matt
Pocock's upstream `writing-great-skills` at
`ed37663cc5fbef691ddfecd080dff42f7e7e350d`.

| Package | Tree hash | Files | Lines | Words | Role |
| --- | --- | ---: | ---: | ---: | --- |
| Refreshed upstream | `5f5f4331f16c0d42f2fce38967e5e4841d5893cea98de0649060070f61dbab70` | 3 | 289 | 4,478 | Control for local mechanisms and routing |
| Current active local | `f70d6c83d49800a11ea4c51e5ea87b601d12755e587bd28a8ee32f956a7682ba` | 4 | 294 | 3,670 | Current-state evidence only |
| Frozen admitted pre-prune | `208491d50213134b0190143e7928319dcba2ddc0313e47539df068f8593e52af` | 4 | 405 | 4,040 | Pruning-equivalence control |
| Final experimental candidate | `9822b2eb486e7e4a31589cd02a0667981639ef3c2df810da3d6945f6e650f77c` | 4 | 306 | 3,716 | Accepted inactive result |

Counts are diagnostic. The final package removes 324 words and 99 lines from
the admitted pre-prune package and remains 762 words smaller than upstream.

## Complete-Package And Admission Audit

The Prompt 3 inventory was refreshed rather than assumed. The final package is
still exactly `SKILL.md`, `GLOSSARY.md`, `BEHAVIOR-EVALS.md`, and
`agents/openai.yaml`. There are no scripts, templates, assets, machine schemas,
or additional references. The relationship map already contains the actual
`skill-creator` boundary; no relationship edge changed.

No synthesis omission survived the audit. No repair generation was needed.

| Mechanism | Prompt 4 challenge | Decision |
| --- | --- | --- |
| Implicit invocation | Upstream policy missed every natural-language positive; candidate retained all adjacent negatives | Keep |
| Codex invocation vocabulary and policy | Machine contract differs from upstream's runtime terms | Keep local adaptation |
| Trigger-only description | Metadata-only candidate classified all positive and negative cases | Keep |
| Audit and Author | Typed authority and Return distinguish advisory judgment from bounded persistence | Keep |
| Source and full-audit coverage | Upstream lacked complete surface and disposition contracts | Keep; inline full-audit branch remains cheapest |
| Single ownership and relationship facts | New-package and existing-skill cases require named owners and caller boundaries | Keep |
| Five authoring behaviors | Existing-skill case needs resolution, ownership, shaping, pruning, and proof | Keep behaviors; exact mnemonic remains deferred |
| Discoverable semantic roles | Typed returns and terminal boundaries changed observed output | Keep roles; named surface and fixed order remain deleted |
| Cut test and protected contracts | Existing-skill case preserved authority and safety while pruning | Keep |
| Counterfactual protocol | Upstream had no reproducible control, sampling, rubric, variance, or terminal decision | Keep disclosed in `BEHAVIOR-EVALS.md` |
| `skill-creator` and canonical stop | Upstream could not name the scaffolding owner or complete the owner chain | Keep |
| Typed Return and completion | Upstream produced useful prose but no stable owner-specific packet | Keep |
| Mirror inspection | Four of five upstream samples proposed default mirror comparison | Keep the explicit-request/report-only boundary |
| Evidence independence | Behavioral case required uncontaminated controls and root judgment | Keep; dispatch mechanics remain caller-owned |
| Helpers, schemas, ledgers, templates, and ceilings | No sampled failure required them | Reject |

Removing Audit/Author, typed Return, or the `skill-creator` boundary would
reverse confirmed material decisions and also discard observed behavioral
value. No minimality frontier therefore required participant resolution.

## Frozen Pre-Prune Fixture

The admitted repaired pre-prune package is frozen at
[`docs/validation/evals/writing-great-skills-pruning-pre-prune/`](../evals/writing-great-skills-pruning-pre-prune/).
It contains the same four runtime surfaces as the candidate and expands every
admitted authority, coverage, ownership, authoring, pruning, proof, Return, and
completion contract before compression. It contains neither the deferred exact
five-word mnemonic nor the deleted `Semantic Skill Surface` mechanism.

The fixture is the exact stored snapshot identified by
`208491d50213134b0190143e7928319dcba2ddc0313e47539df068f8593e52af`.
Its support-file text is semantically identical to the candidate's support
files; filesystem newline normalization is part of the fixture's exact hash.

## Independent Prompt 4 Pruning Ledger

The root re-read the frozen package and applied the cut test independently.
The groups below account for every instruction-bearing unit in that fixture;
they do not inherit Prompt 3's provisional verdicts.

### Metadata And Root Outcome

| IDs | Pre-prune units | Decision | Final destination |
| --- | --- | --- | --- |
| M01-M03 | package identity, three positive branches, four adjacent exclusions | Keep | Frontmatter, byte-equivalent semantics |
| O01 | expanded smallest-surface Predictability outcome | Collapse | Predictability leading word, cuts, and Completion |

### Authority And Coverage

| IDs | Pre-prune units | Decision | Final destination |
| --- | --- | --- | --- |
| A01-A03 | operation selector, strict Audit, bounded Author | Collapse | Authority opening and two mode bullets |
| A04 | behavior test is read-only; persistence requires Author | Keep | Authority |
| A05-A06 | `skill-creator` package owner; semantic owner and canonical stop | Collapse | Authority |
| A07 | source/authority before judgment; proof follows candidate | Collapse | Authority terminal paragraph |
| C01-C02 | resolved source set and behavior-capable bounded coverage | Collapse | Coverage opening |
| C03-C08 | package, upstream, relationship, contract, proof, and routing full-audit inventory blocks | Collapse | One conditionally inline full-audit sentence |
| C09-C10 | item and upstream-difference disposition sets | Keep | Coverage classification sentence |
| C11 | mirror only on explicit installation-state request; report, do not repair | Keep | Coverage mirror paragraph |

### Ownership And Authoring

| IDs | Pre-prune units | Decision | Final destination |
| --- | --- | --- | --- |
| W01 | one owner for rule through completion | Collapse | Ownership |
| W02 | callee, observable trigger, preserved authority, Return | Keep | Ownership |
| W03 | point to foreign procedure | Keep | Ownership |
| S01 | conditional glossary pointer and full-audit load | Keep | Authoring Contract |
| S02 | discoverable roles without named surface, headings, or fixed order | Collapse | Authoring Contract |
| S03-S04 | trigger-only description and one real branch per trigger | Collapse | Authoring Contract |
| S05 | inline common path; disclosed branch; co-location; evidence-based split | Collapse | Authoring Contract |
| S06 | useful-prior leading-word rule | Disclose | `GLOSSARY.md`; duplicate root explanation removed |

### Pruning, Proof, Return, And Completion

| IDs | Pre-prune units | Decision | Final destination |
| --- | --- | --- | --- |
| P01-P02 | protect contracts; restore owner; remove stale and branch-only material | Collapse | Behavior-Preserving Cuts |
| P03 | behavior-change cut question | Keep | Behavior-Preserving Cuts |
| P04 | collapse duplication; positive target and paired guardrail | Collapse | Behavior-Preserving Cuts |
| P05 | counts and headings are diagnostics | Delete | ADR 0004 and this evidence record own the non-runtime fact |
| V01 | bytes and machine contracts use structural proof | Keep | Claim-Matched Proof |
| V02 | ownership and composition use relationship trace | Keep | Claim-Matched Proof |
| V03 | behavior-change predicate loads `BEHAVIOR-EVALS.md` | Keep | Claim-Matched Proof |
| V04 | no control failure rejects guidance | Keep | Claim-Matched Proof |
| V05 | fixed fresh uncontaminated evidence; root judgment; ambient dispatch | Collapse | Claim-Matched Proof and disclosed evaluation reference |
| R01 | typed status with authority and coverage | Keep | Return |
| R02-R03 | Audit and Author field sets | Collapse | Return |
| D01 | classified coverage, one home, decided upstream, proof, checks, preserved work, canonical stop | Collapse | Completion |

### Supporting Surfaces

| IDs | Units | Decision |
| --- | --- | --- |
| G01-G32 | Every retained glossary concept, rule, caveat, failure consequence, and alias | Keep in the disclosed glossary |
| E01-E18 | Diagnose, Control, Sample, Stress, Judge, Record, and terminal evaluation decisions | Keep in the disclosed behavioral branch |
| Y01 | `policy.allow_implicit_invocation: true` | Keep as machine contract |

The final package retains no repeated pre-prune meaning that changes the fixed
cases. The only deleted runtime clause, P05, is an explanatory non-runtime fact;
the final proof and ADR still prevent count-based acceptance.

## Runtime And Sampling

- Runtime: Codex desktop fresh-context direct collaboration agents.
- Context: `fork_turns="none"`; no model or reasoning override.
- Authority: read-only simulation; samples could not mutate, invoke another
  skill, install, stage, commit, use the web, or dispatch peers.
- Root judgment: every returned table was inspected against the frozen rubric.
- Telemetry unavailable: exact model identifier, reasoning setting, token
  count, and per-sample elapsed time.
- Protocol deviation: multiple fixed cases were batched into each context;
  each behavior still appeared in five independent contexts per arm.

## Metadata Routing Study

Metadata-only contexts read frontmatter and invocation policy, not procedure
bodies. None of the nine requests explicitly named the skill. The four positive
families were create/edit, Audit, behavioral proof, and semantic pruning. The
five adjacent negatives were general prompt rewriting, ordinary code review,
plugin scaffolding, installation, and Git delivery.

| Arm | Positive recall | Adjacent-negative rejection | Total |
| --- | ---: | ---: | ---: |
| Upstream explicit-only baseline | 0 / 20 | 25 / 25 | 25 / 45 |
| Experimental candidate | 20 / 20 | 25 / 25 | 45 / 45 |

Variance was zero on the nine routing decisions. One candidate sample
mis-added its displayed totals as five invokes and four rejects; inspection of
its nine rows showed the same correct four invokes and five rejects as every
peer. The arithmetic typo was not a routing failure.

This proves metadata-level classification, not host auto-discovery of an
inactive package.

## Full-Package Behavioral Study

Each context received the same five cases:

1. strict read-only Audit with exact advisory wording;
2. bounded existing-skill Author work;
3. a new package followed by separately authorized install and Git work;
4. complete full-audit coverage with a merely present installed mirror; and
5. direct read-only testing of completion wording.

| Observable behavior | Upstream | Candidate |
| --- | ---: | ---: |
| Audit remains read-only and exact wording advisory | 5 / 5 | 5 / 5 |
| Typed Audit packet with stable evidence limits | 0 / 5 | 5 / 5 |
| Author remains inside the explicitly bounded canonical surface | 5 / 5 | 5 / 5 |
| Source, ownership, relationship, and claim-matched proof are complete | 0 / 5 | 5 / 5 |
| Typed Author packet and canonical stop | 0 / 5 | 5 / 5 |
| `skill-creator` owns new-package scaffolding and metadata | 0 / 5 | 5 / 5 |
| Installation and Git remain named downstream owners | 0 / 5 | 5 / 5 |
| Full-audit inventory and both disposition sets are complete | 0 / 5 | 5 / 5 |
| Mirror is skipped absent explicit installation-state evidence | 0 / 5 | 5 / 5 |
| Behavioral proof uses uncontaminated controls and at least five samples per arm | 0 / 5 | 5 / 5 |
| Evaluation returns one evidence-supported terminal decision | 0 / 5 | 5 / 5 |
| **Total** | **10 / 55** | **55 / 55** |

Four upstream samples proposed comparing the mirror merely because it existed;
the fifth reported that the baseline supplied no mirror rule. All candidate
samples excluded it from default coverage. Upstream outputs preserved the
straightforward read-only and explicit write bounds supplied by the task, so
the candidate receives no behavioral credit for inventing those defaults; its
retained value is the typed operation packet, complete owner contract, proof,
and terminal boundary.

Candidate variance was zero on the rubric and the worst sample passed all five
cases. No candidate sample persisted advisory wording, absorbed installation
or Git into Writing Great Skills completion, scanned the mirror by default, or
accepted behavioral guidance without a failing control.

## Pruning Equivalence

The five final-candidate samples above also served as the final arm for the
identical five-case pruning protocol; reusing an exact fixed arm avoided a
behaviorless duplicate wave. Five new independent pre-prune controls read only
the frozen fixture.

| Case | Pre-prune control | Final candidate |
| --- | ---: | ---: |
| A: strict Audit and typed packet | 5 / 5 | 5 / 5 |
| B: bounded existing-skill Author behavior | 5 / 5 | 5 / 5 |
| C: scaffolding, semantics, canonical stop, install, and Git owners | 5 / 5 | 5 / 5 |
| D: full coverage, dispositions, and conditional mirror boundary | 5 / 5 | 5 / 5 |
| E: uncontaminated behavioral protocol and terminal decision | 5 / 5 | 5 / 5 |
| **Total** | **25 / 25** | **25 / 25** |

Variance was zero and no critical failure appeared in either arm. The final
candidate therefore preserves the admitted pre-prune behavior while reducing
aggregate runtime load.

## Residual Unavoidable Surface

The remaining 3,716 words are dominated by the baseline-derived glossary
(2,696 words) and branch-only evaluation procedure (342 words). `SKILL.md` is
675 words. The inline full-audit inventory remains the sole branch-specific
root exception because a new file plus pointer would cost more aggregate load
and weaken full-audit recall. No other mechanism earned another support file.

## Structural Proof And Limits

- Sampled candidate and then-current manifest hash:
  `9822b2eb486e7e4a31589cd02a0667981639ef3c2df810da3d6945f6e650f77c`.
- Sampled pre-prune tree hash:
  `208491d50213134b0190143e7928319dcba2ddc0313e47539df068f8593e52af`.
- Current normalized candidate and manifest hash:
  `c7c02f4f9896cd5bf6e6c25886e77785a9f80c0ccea0d02f7aaa6fc85076dcc4`.
- Current corrected pre-prune fixture hash:
  `23fb951a230df6c929803f02d3ad16586471a14f4169632eddaf39c725c34bc2`.
- `python -m scripts.validate_skills`: passed.
- Validator and experimental contracts: 28 passed, 1 skipped.
- Exact package inventory, pointers, policy, and deferred-term assertions:
  passed.
- `git diff --check` and `git diff --cached --check`: passed.
- The broader pack and full repository suites were not rerun: Prompt 4 changed
  no candidate bytes, canonical bytes, relationships, executable helper, or
  test contract. The focused structural proof covers the changed fixture,
  manifest state, and existing experimental contract.

The acceptance claim remains bounded by these limits:

- inactive-package invocation was simulated from metadata; host discovery and
  canonical caller integration remain promotion-time proof;
- action sequences and terminal packets were simulated read-only rather than
  mutating representative skill packages;
- no separate contradictory-authority Audit stress wave was run because the
  grouped suite already tested the admitted operation and typed Return, and
  another ten contexts would be disproportionate;
- installation, mirror parity, and Git delivery remain outside Prompt 4; and
- exact model, reasoning, token, and timing telemetry was unavailable.

These gaps prevent claims about platform integration or delivery. They do not
reject the inactive candidate's sampled semantic behavior.

**Decision: `accept` for experimental behavioral acceptance; stop before
promotion.**
