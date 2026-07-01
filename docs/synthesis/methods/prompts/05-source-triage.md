# Prompt 05: Source Triage

Use this as Step 5 of
[`../source-to-skill-flow.md`](../source-to-skill-flow.md).

The goal is to decide which extracted source material survives, where it
belongs, and why, without creating the final behavior flow or runtime wording.

````markdown
We are triaging extracted source material for one Codex skill facet.

Skill: `<skill-name>`
Skill path: `<path-to-skill>`
Facet: `<facet-number-and-name>`
Facet research question: `<question from facet map>`
Facet boundaries: `<paste owns / does-not-own / should-answer / should-not-answer>`
Source search packet: `<path or paste Prompt 03 output>`
Source extraction packet: `<path or paste Prompt 04 output>`

Do not search for new sources.
Do not extract new material except tiny gap notes.
Do not synthesize the skill behavior flow yet.
Do not write runtime `SKILL.md` wording yet.
Do not keep material because it is interesting. Keep it only if it can change
agent behavior.

Your job is to decide what extracted material survives, where it belongs, and
why.

Use these triage categories:

- `keep-runtime`: likely belongs in final runtime skill wording
- `keep-support`: useful, but belongs in support/reference docs
- `keep-research`: useful background, not operational enough for runtime
- `bridge-needed`: promising, but needs translation into agent behavior
- `owned-elsewhere`: belongs to another skill, the engineering contract, or
  repo docs
- `reject`: no-op, generic, decorative, too vague, too source-specific, or not
  useful

Return:

## 1. Triage Scope

State:

- facet being triaged;
- extraction packet used;
- source lanes represented;
- what is out of scope;
- what would count as over-keeping.

## 2. Keep / Reject Standard

Define the judgment standard in 3-6 bullets.

Include:

- what counts as behavior-changing;
- what counts as too vague;
- what counts as too heavy for runtime;
- what belongs in support docs instead of `SKILL.md`;
- what another skill or contract already owns.

## 3. Leading Word Triage

Use:

| Term | Source | Category | Why | Behavior It Can Steer | Risk If Kept | Action |
| --- | --- | --- | --- | --- | --- | --- |

The `Action` should be one of:

- keep for behavior flow
- translate before keeping
- move to support
- keep as research only
- reject

## 4. Behavior Rule Triage

Use:

| Rule | Source | Category | Why | Operational Gate | Failure Prevented | Action |
| --- | --- | --- | --- | --- | --- | --- |

Reject rules that are slogans, taste-only claims, or already default agent
behavior.

## 5. Failure Mode Triage

Use:

| Failure Mode | Source | Category | Why | Skill Countermeasure | Evidence / Warning Sign | Action |
| --- | --- | --- | --- | --- | --- | --- |

Keep only failures this skill can plausibly prevent.

## 6. Evidence Gate Triage

Use:

| Gate | Source | Category | Why | Too Weak If | Too Heavy If | Action |
| --- | --- | --- | --- | --- | --- | --- |

Prefer gates that are checkable, not aspirational.

## 7. Stop / Ask Rule Triage

Use:

| Condition | Source | Category | Why | Agent Should | Resume When | Action |
| --- | --- | --- | --- | --- | --- | --- |

Reject over-cautious stop rules that would make the agent ask instead of doing
ordinary engineering work.

## 8. Agentic Bridge Triage

Use:

| Source Concept | Agentic Translation | Category | Why | Behavior Flow Candidate | Action |
| --- | --- | --- | --- | --- | --- |

Mark `bridge-needed` when the source concept is good but not yet phrased in
agent-executable terms.

## 9. Owned-Elsewhere Check

Identify extracted material that belongs somewhere else.

Use:

| Item | Better Owner | Why | Keep Reference? |
| --- | --- | --- | --- |

Possible owners:

- engineering contract
- another skill
- repo `AGENTS.md`
- repo domain docs
- ADRs
- support/reference docs
- research only

## 10. Rejection Log

List rejected material so we do not rediscover it later.

Use:

| Item | Source | Rejection Reason | Do Not Revive Unless |
| --- | --- | --- | --- |

## 11. Surviving Material

Create the clean pile for Prompt 06.

Use:

### Runtime Candidates

- `<item>`: `<why it may belong in runtime>`

### Support Candidates

- `<item>`: `<why it belongs in support/reference>`

### Research-Only Material

- `<item>`: `<why it stays research-only>`

### Bridge-Needed Material

- `<item>`: `<what translation is needed>`

## 12. Handoff To Behavior Flow

End with:

- strongest runtime candidates;
- strongest support/reference candidates;
- material that needs bridge translation;
- biggest rejected temptation;
- ownership conflicts to watch;
- what Prompt 06 should turn into an execution chain first.

Write the triage packet to:

`docs/research/skill-facets/<skill-name>/FACET-<n>-<name>-triage.md`
````

## Quality Bar

This prompt is complete when the next step has a clean pile of surviving
behavior-changing material, explicit owner decisions, and a rejection log that
prevents weak source material from being rediscovered.
