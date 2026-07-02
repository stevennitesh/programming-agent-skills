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
Extraction decision: `<Prompt 04 extraction decision>`
Claim-strength notes: `<Prompt 04 direct / cross-source / bridge / thin notes>`
Boundary-drift notes: `<Prompt 04 boundary drift notes>`
Revision feedback: `<optional feedback if rerunning this prompt; otherwise "none">`

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

Use these owner-conflict severities:

- `hard-boundary`: do not carry into this facet except as a stop/owner note;
- `later-facet-watchpoint`: likely useful, but another facet should decide it;
- `soft-reference`: this facet may point to it without owning the behavior;
- `support-only`: keep only behind support/reference material;
- `research-only`: useful rationale, not an execution input.

Return:

## 1. Triage Scope

State:

- facet being triaged;
- extraction packet used;
- source lanes represented;
- what is out of scope;
- what would count as over-keeping.

## 2. Prompt 04 Handoff Check

Confirm how extraction shaped this triage.

Use this table:

| Prompt 04 Input | Used / Revised / Deferred / Rejected | Triage Consequence | Notes |
| --- | --- | --- | --- |

Cover at least:

- extraction decision;
- claim-strength labels;
- extraction target coverage;
- boundary-drift notes;
- extraction gaps;
- uncertain source material;
- Prompt 05 triage-first suggestions.

Do not re-extract source material here. If the handoff lacks enough behavior,
gates, misuse risk, or claim strength to triage honestly, choose
`return-to-extraction`.

## 3. Keep / Reject Standard

Define the judgment standard in 3-6 bullets.

Include:

- what counts as behavior-changing;
- what counts as too vague;
- what counts as too heavy for runtime;
- what belongs in support docs instead of `SKILL.md`;
- what another skill or contract already owns.

## 4. Leading Word Triage

Use:

| Term | Source | Category | Why | Behavior It Can Steer | Risk If Kept | Action |
| --- | --- | --- | --- | --- | --- | --- |

The `Action` should be one of:

- keep for behavior flow
- translate before keeping
- move to support
- keep as research only
- reject

## 5. Behavior Rule Triage

Use:

| Rule | Source | Category | Why | Operational Gate | Failure Prevented | Action |
| --- | --- | --- | --- | --- | --- | --- |

Reject rules that are slogans, taste-only claims, or already default agent
behavior.

## 6. Failure Mode Triage

Use:

| Failure Mode | Source | Category | Why | Skill Countermeasure | Evidence / Warning Sign | Action |
| --- | --- | --- | --- | --- | --- | --- |

Keep only failures this skill can plausibly prevent.

## 7. Evidence Gate Triage

Use:

| Gate | Source | Category | Why | Too Weak If | Too Heavy If | Action |
| --- | --- | --- | --- | --- | --- | --- |

Prefer gates that are checkable, not aspirational.

## 8. Stop / Ask Rule Triage

Use:

| Condition | Source | Category | Why | Agent Should | Resume When | Action |
| --- | --- | --- | --- | --- | --- | --- |

Reject over-cautious stop rules that would make the agent ask instead of doing
ordinary engineering work.

## 9. Agentic Bridge Triage

Use:

| Source Concept | Agentic Translation | Category | Why | Agent Bridge Candidate | Action |
| --- | --- | --- | --- | --- | --- |

Mark `bridge-needed` when the source concept is good but not yet phrased in
agent-executable terms.

## 10. Bridge Resolution Plan

For each `bridge-needed` item, state the behavior translation Prompt 06 should
try.

Use:

| Item | Raw Source / Bridge Term | Plain Behavior Translation | Keep / Support / Drop If | Prompt 06 Input |
| --- | --- | --- | --- | --- |

Do not write final runtime wording. This is only the translation target that
lets Prompt 06 build an execution chain.

## 11. Owned-Elsewhere Check

Identify extracted material that belongs somewhere else.

Use:

| Item | Better Owner | Conflict Severity | Why | Keep Reference? |
| --- | --- | --- | --- | --- |

Possible owners:

- engineering contract
- another skill
- repo `AGENTS.md`
- repo domain docs
- ADRs
- support/reference docs
- research only

## 12. Duplicate / Synonym Collapse Check

Identify competing terms or rules that may be doing the same job.

Use:

| Cluster | Candidates | Preferred Carry-Forward | Demote / Merge | Why |
| --- | --- | --- | --- | --- |

This is the place to collapse duplicate leading words and overlapping gates
before Prompt 06 turns the pile into behavior. Do not decide exact runtime
wording yet.

## 13. Rejection Log

List rejected material so we do not rediscover it later.

Use:

| Item | Source | Rejection Reason | Do Not Revive Unless |
| --- | --- | --- | --- |

## 14. Surviving Material

Create the clean pile for Prompt 06.

Use:

### Runtime Candidates: Must Carry Forward

- `<item>`: `<why Prompt 06 should preserve this behavior>`

### Runtime Candidates: Optional / Supporting Pressure

- `<item>`: `<why it may belong in runtime>`

### Support Candidates

- `<item>`: `<why it belongs in support/reference>`

### Research-Only Material

- `<item>`: `<why it stays research-only>`

### Bridge-Needed Material

- `<item>`: `<what translation is needed>`

## 15. Runtime Priority / Budget

Rank the runtime candidates so Prompt 06 knows what must survive compression.

Use:

| Priority | Candidate | Must / Should / Could | Why | Drop If |
| --- | --- | --- | --- | --- |

Prefer a small `Must` set. If everything is marked `Must`, triage has not done
enough pruning.

## 16. Handoff To Agent Bridge

End with:

- triage decision:
  - `ready-for-behavior-flow`: continue to Prompt 06;
  - `return-to-extraction`: return to Prompt 04 because extraction missed
    behavior-changing material or misuse risks;
  - `return-to-source-search`: return to Prompt 03 because source coverage is
    too weak;
  - `revise-facet-map`: return to Prompt 02 because the facet is all
    owned-elsewhere, too broad, too narrow, or overlapping;
  - `drop-or-merge-facet`: stop this facet and record where its remaining
    material belongs;
- strongest runtime candidates;
- strongest support/reference candidates;
- material that needs bridge translation;
- biggest rejected temptation;
- ownership conflicts to watch;
- what Prompt 06 should turn into an execution chain first.

The triage decision label must be explicit. Do not omit it.

Write the triage packet to:

`docs/research/skill-facets/<skill-name>/FACET-<n>-<name>-triage.md`
````

## Quality Bar

This prompt is complete when the next step has a clean pile of surviving
behavior-changing material, runtime priorities, explicit owner-conflict
severity, bridge translations, duplicate-collapse decisions, and a rejection log
that prevents weak source material from being rediscovered, or when it decides
to loop back, drop, or merge the facet.
