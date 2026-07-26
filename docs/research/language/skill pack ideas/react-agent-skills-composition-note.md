# React Composition Enhancement Candidate

Status: answered

Supports: Matt-derived composition vocabulary and future skill enhancement

Freshness: `react/react` remote `main` verified 2026-07-25 at
`b685b40d870b90a975da28c8d22ecf0ba910b1a1`

## Retain

React's
[`/verify`](https://github.com/react/react/blob/b685b40d870b90a975da28c8d22ecf0ba910b1a1/.claude/skills/verify/SKILL.md)
shows a composition shape missing from Matt Pocock's navigation vocabulary:
an **executable aggregate** owns one combined outcome while invoking
independently useful leaf skills.

Matt's **router** selects a next skill or flow and stops
([Matt vocabulary packet](matt-pocock-skills-vocabulary.md), lines 162-163).
The useful combined vocabulary is:

- **router:** selects and stops;
- **executable aggregate:** invokes leaves and owns the combined completion
  result; and
- **leaf:** performs one bounded operation and returns to its caller.

## Enhancement Use

When evaluating or authoring a composed skill, classify its relationship shape.
An executable aggregate should:

- own one caller-visible outcome;
- keep each leaf independently useful;
- own ordering, failure handling, and the final Return; and
- reference leaf behavior instead of copying its procedure.

Add this distinction only inside the existing relationship and
`pack-composition` analysis
(`docs/synthesis/methods/deploy-prompts.md:702-716`). It sharpens the current
callee, authority, and Return contract; it does not justify another campaign
stage, helper, or generic verification skill.

## Reject

Import no React skill. Its remaining skills are React-specific command wrappers
or compiler-port workflows. Fixed inventories, mandatory fan-out, repeated
orchestration loops, and automatic delivery behavior are not enhancements to
Matt's lightweight composition or this pack.

## Evidence Limit

The complete React agent-facing subset was inspected, but it contains no
controlled behavioral evaluation of the skill wording. The composition shape
is source-supported; its local quality lift is untested.

Revisit only if a local composed skill exposes ambiguous completion ownership
or duplicated leaf procedure.

Caller-use boundary: research evidence only; no runtime change is authorized.

Next: none.
