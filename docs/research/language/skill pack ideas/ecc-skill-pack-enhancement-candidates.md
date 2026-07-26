# ECC Enhancements For Matt-Pocock-Derived Skills

Status: answered

Freshness: ECC commit `ac30ff3ea249bf5f94dbc5e9b18ab681cc9af91d`
and local skill owners verified 2026-07-25

## Decision

ECC is useful only as an idea source. Import no inspected ECC skill unchanged
and add no deploy stage.

Two mechanics could strengthen Matt-Pocock-derived skills:

| Mechanic | What It Enhances | Local Use | Decision |
| --- | --- | --- | --- |
| Prompt-pressure testing | Predictable invocation and behavior under realistic task wording | Add an optional pressure dimension to behavioral evaluation when a skill claims invocation resilience | Import the idea |
| Prior-art search | Small composable skills with one clear owner and little duplication | Search briefly for an existing skill before admitting new pack-derived behavior | Import the idea |

## 1. Pressure-Test Invocation Claims

ECC's `skill-comply` runs the same task with:

- supportive wording that names the skill;
- neutral wording that does not; and
- competing wording that encourages a shortcut.

This usefully extends Matt's invocation and context-economics lens: a good skill
should recruit the intended behavior without needing the task prompt to repeat
its instructions.
(`skills/skill-comply/SKILL.md:11-17,45-55`;
`skills/skill-comply/prompts/scenario_generator.md:2-50`)

Apply it only when a candidate claims invocation resilience. Keep the current
M0/H1 controls, wrong-condition cases, five-sample floor, fixed rubric, and root
judgment
(`skills/custom/writing-great-skills/BEHAVIOR-EVALS.md:3-64`).

Do not import ECC's runner, generated specifications, three-scenario minimum,
simple compliance percentage, or hook-promotion logic.

## 2. Search Before Adding Skill Behavior

ECC's `skill-scout` searches local, marketplace, GitHub, and web skill sources,
then checks external matches for risky commands, writes, networking,
credentials, and installs (`skills/skill-scout/SKILL.md:28-93`).

Use this as a bounded lane inside the existing Research Pass: after blind
independent discovery, inspect only the strongest exact or near-exact skill
matches and classify their useful behavior as:

- `Import`;
- `Already present`; or
- `Deliberately reject`.

This supports Matt-style composition by preventing duplicate skills and
clarifying which skill owns the behavior. It should not become a mandatory
stage, popularity ranking, result catalog, or use/fork/create checkpoint.
(`docs/synthesis/methods/deploy-prompts.md:535-602`)

## Deploy Campaign Integration

These ideas fit inside existing campaign units:

| Unit | Enhancement | Boundary |
| --- | --- | --- |
| Research Pass | After blind independent discovery, search briefly for the strongest matching skills and record source identity, risky operations, and useful mechanics | No new source quota or mandatory marketplace sweep |
| Prompt 2 | Classify each useful mechanic as `Import`, `Already present`, or `Deliberately reject`; admit only a concrete H1 contribution | Source popularity and repetition do not justify admission |
| Prompt 3 | When an admitted H1 claims invocation resilience, freeze supportive, neutral, and competing pressure as one optional fixture dimension while keeping task facts and runtime arms fixed | Do not create pressure cases for unrelated claims |
| Prompt 4 | Run those cases through the existing adaptive M0/H1 gate and fixed rubric | Do not use ECC's standalone compliance percentage or a separate evaluation wave |
| Pruning Pass | Reuse the pressure cases only when a cut changes invocation-bearing wording | Unaffected cuts reuse their existing proof lanes |

Prompts 1, 5, and 6 need no ECC-derived change. This improves source coverage
and invocation proof while preserving the current campaign sequence and
complexity ratchet.

## Deliberately Reject

`skill-stocktake`, `context-budget`, `rules-distill`, and
`agent-self-evaluation` add no necessary skill behavior. Their useful concerns
are already covered by local ownership, freshness, runtime-load, pruning,
review, and evaluation contracts.

## Evidence Boundary

The inspected ECC subset establishes intended mechanics, not behavioral
effectiveness. No ECC compliance run was performed, the rest of ECC was not
audited, and both retained ideas still require separately authorized wording
and candidate-owned proof.

Source: clean clone at `.tmp/repos/ECC`, revision
`ac30ff3ea249bf5f94dbc5e9b18ab681cc9af91d`.

Final decision: `source-packet-complete`

Return owner: the user
