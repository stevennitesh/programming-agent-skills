# Astra prototype rewrite assessment

This records source selection and review for `skills/astra/prototype/`.
It is research evidence, not runtime instructions or proof of improved agent
performance. Prototype remains separate from codebase-design, as requested.

## Direction

Keep prototype as an optional method for gathering evidence that can change a
design decision. Its useful contribution is experimental judgment: decide what
observation matters, preserve the mechanism under investigation, distinguish a
broken harness from a failed approach, and limit conclusions to what was observed.

The main procedure frames, builds, observes, and returns an experiment. One
conditional reference covers state and integration behavior, rendered interaction,
and variable measurements. It replaces the old three branch files without
requiring agents to read unrelated methods.

Codebase-design owns the broader architecture decision. Prototype returns
evidence to that caller or to authorized implementation; it neither introduces
another approval gate nor treats a successful experiment as production readiness.
Direct requests may deliver a retained demo for later evaluation.

## Source selection

Inspected these local snapshots and verified their commits. No upstream fetch
was performed for this rewrite.

| Source and commit | Useful material | Treatment |
| --- | --- | --- |
| Matt Pocock `3cca18b368ae95cdbdebbff572ccafa662551015` | Prototype, LOGIC, UI: the question determines the artifact; visible state; domain language; easy comparison under realistic UI context. | Retain those ideas. Remove prescribed HTML, switcher mechanics, fixed variant counts, blanket test bans, mandatory branch capture, and automatic adoption. |
| Pstack `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Poteto-mode prototype playbook and exhaust-the-design-space: settle empirical forks cheaply, use matching observation surfaces, compare distinct options. | Retain evidence-first scope and easy comparison. Reject blanket bans on frameworks or assertions, unsolicited expansion into variants, and fixed prototype quotas. |
| Superpowers `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Brainstorming spike path: a small feasibility investigation can return an answer without a design document. | Keep that lightweight outcome. Reject mandatory approval before every probe and reclassification as a prerequisite for already-authorized follow-up work. |
| Ponytail `974d940a1c5344210874150b98ff0d2c861fab6a` | Main skill: reuse existing capabilities after understanding the problem; simplification must preserve the requested behavior. | Keep the cheapest valid instrument. Do not equate the shortest code with trustworthy evidence, import persistent modes, or require a universal self-test artifact. |

The local custom prototype already improves substantially on upstream: bounded
questions, criteria chosen before observation, measured variability, actual UI
inspection, effect ownership, and cleanup. These are retained with fewer routing
and artifact restrictions.

## Changes that matter

- Permit a script, harness, demo, or repository-native test according to the
  evidence needed. A human-drivable interface is useful when a human supplies
  judgment, not mandatory for every state question.
- Keep real persistence, concurrency, or protocol behavior when it is the very
  property being tested. Simplify incidental machinery rather than the source of
  uncertainty. An unavailable mechanism leaves a visible evidence gap.
- Allow revised questions during exploration, but identify the revision and
  gather appropriate evidence rather than changing a success rule silently.
- Check equivalent outputs before comparing speed. Treat differences within
  noise as inconclusive and separate possible outcomes from universal guarantees.
- Preserve requested demos pending human review and permit evidence retention
  without a new custody ceremony. Clean up owned transient resources and protect
  unrelated changes.
- Allow already-authorized implementation to continue. Reused experiment code
  needs production assessment and integration proof; neither automatic promotion
  nor rewriting everything is universally correct.

## Challenger review

Two fresh-context challengers reviewed a fixed draft independently and without
editing. One owned discovery, authority, cleanup, and composition with design;
the other owned evidence validity, omissions, and overlap with the contract.

The scope review passed. The evidence review caught an incomplete reference
trigger: "rendered interaction" could omit a static layout comparison, and logic
was not explicitly named. The trigger now matches all three reference subjects,
including visual layout and pure logic. No other defect was found within their
assigned scenarios. These were textual reviews, not executed experiments.
The evidence challenger rechecked the corrected trigger and passed it.

## Validation limits

The skill package validator, repository skill validator, local Markdown link
checks, and whitespace checks passed.

Package checks and independent textual challenges can find inconsistent rules,
missing conditions, and misleading evidence requirements. They do not establish
that this skill improves coding or experimental results over the model baseline
and engineering contract. That claim needs a separate behavioral comparison.
