# Facet Research Prompt

Use this prompt when deepening one skill facet before editing a runtime `SKILL.md`.

The goal is not to collect impressive references. The goal is to extract compact language that points Codex toward upper-bound software-engineering behavior: better taste, tighter scope, stronger proof, clearer reviewability, and less drift.

```text
source wisdom
  -> engineering attention handle
  -> agent behavior
  -> evidence gate
  -> plain-language rule
  -> synthesis wording
```

## Main Prompt

```markdown
We are researching one facet of a Codex skill before editing `SKILL.md`.

Skill: `<skill-name>`
Facet: `<facet-name>`
Research question: `<question>`
Skill surface affected: `<where this behavior would live in the skill>`
Current candidate intent: `<one paragraph or bullet list>`

Target:

Find language that makes Codex perform upper-bound engineering behavior, not average behavior. We are looking for strong attention handles from software-engineering canon, professional practice, empirical research, and agentic/LLM guidance. Do not dump research into the skill. Distill it into compact wording that changes agent behavior.

Research lanes:

1. Core engineering canon: books, manuals, and practices that strong professional programmers actually use.
2. Empirical/professional support: studies, large-org practices, and field reports that validate or correct the canon.
3. Agentic translation: LLM/agent/tooling sources that explain how bounded scope, explicit success criteria, verification, and stop rules improve coding-agent behavior.
4. Compression and pruning: which words are leading words, which are weak/no-op, and what should survive into runtime skill prose.

For each lane, return:

- best sources and why they are credible;
- strongest terms/phrases that should steer Codex;
- exact agent behaviors those terms should create;
- evidence gates or completion criteria;
- generic/noisy terms to prune;
- overclaim risks and counterweights;
- candidate synthesis wording, as short as possible.

Then synthesize:

- source-role tiers: `core engineering canon`, `empirical support`, `delivery/operation economics` when relevant, `agentic translation`, `counterweights`;
- high-signal vocabulary;
- weak/no-op vocabulary and stronger replacements;
- start gate, done gate, split/ask gate;
- one tiny good/bad contrast example;
- candidate synthesis wording that could later be compressed into `SKILL.md`;
- what should remain research-only.

Do not edit `SKILL.md` yet. The output should make the synthesis promotion
obvious, small, and high-signal.
```

## Extraction Template

For each source or source cluster, extract only what can affect skill behavior.

```markdown
### <Facet>: <source or cluster>

Source:
- <title / author / link or local note>

Useful terms:
- `<term>` - <what behavior it should wake up in the agent>

Principles:
- <principle that should change how the skill runs>

Agent behavior:
- <observable action the skill should cause>

Evidence gate:
- <what proves the step is done>

Plain-language rule:
- <short blunt version, e.g. "One issue only." / "No proof, no done.">

Candidate synthesis wording:
- <sentence or bullet that could survive promotion into synthesis>
```

## Translation Rules

Keep elite engineering terms when they improve taste:

- `bounded slice`
- `tracer bullet`
- `fixed point`
- `semantic correctness`
- `acceptance criteria`
- `load-bearing internal`
- `seam`
- `red-green-refactor`
- `Standards and Spec`
- `residual risk`

Plain-language the gates:

- One issue only.
- No proof, no done.
- If the better approach changes the promise, stop and ask.
- Do not widen the slice because nearby work is visible.
- Review the diff from the starting point.
- Commit only the work for this issue.

Do not turn the skill into caveman prose. Keep taste precise; make gates blunt.

## Deepen Pass

After researching a facet, update the working notes with:

1. What the current skill already says well.
2. What behavior is missing or weak.
3. Which terms should stay technical.
4. Which gates should become plainer.
5. Which lines should be removed because another skill or the engineering contract owns them.

## Promotion To Synthesis

After a facet packet meets the quality bar, move chosen wording into a
synthesis note before editing runtime `SKILL.md`.

Use:

- [`../../synthesis/promotion-flow.md`](../../synthesis/promotion-flow.md)
- [`../../synthesis/methods/process.md`](../../synthesis/methods/process.md)
- [`../../synthesis/methods/controlled-language-pass.md`](../../synthesis/methods/controlled-language-pass.md)

Research owns evidence and candidate wording. Synthesis owns the selected
behavior, compression, prune decisions, and validation plan.

## Four-Subagent Review Prompt

After the first or second research pass, use four reviewers to rate whether the packet is actually ready to shape runtime skill behavior.

```markdown
Rate this research packet for the goal:

> higher quality programming by encoding strong signal language for upper-bound behavior, not average behavior.

Read:

- `<research-framework-path>`
- `<facet-research-path>`

Use this lens: `<lens>`

Give:

- numeric rating /10;
- strongest signal terms;
- weak, awkward, or no-op terms;
- source-tier corrections or missing sources, if relevant;
- concrete behavioral failures still possible;
- what should change before synthesis promotion or runtime editing;
- the smallest synthesis or runtime wording you would keep.

Do not edit files.
```

Use these four lenses:

```text
1. Behavioral steering and leading words for Codex/LLMs.
2. Source quality and professional canon.
3. Skill compression, pruning, duplication, and runtime information hierarchy.
4. Upper-bound software-engineering execution: proof, maintainability, reviewability, and scope control.
```

## Packet Shape

Save each facet as:

```text
docs/research/skill-facets/<skill-name>/FACET-<n>-<SHORT-NAME>.md
```

Recommended sections:

```markdown
# Facet <n> Research: <Name>

## Decision Summary
## Review / Rating
## Source Tiers
## High-Signal Language
## Agent Behavior And Gates
## Good/Bad Contrast
## Synthesis Promotion
## Prune Notes
## Remaining Research Gaps
```

Keep the research broad enough to justify the words, then compress hard into a
synthesis note. The runtime skill should usually receive a few dense lines, not
the whole packet.

## Quality Bar

A facet is ready for a first skill edit when:

- it has 3-7 high-quality source takeaways;
- the core behavior can be stated in one compact behavior chain;
- the strongest terms are leading words or crisp gates, not generic virtues;
- concrete agent behaviors, evidence gates, plain-language rules, synthesis
  promotion notes, and prune notes are present;
- source roles are separated instead of blended;
- at least one counterweight prevents overclaiming;
- the promoted synthesis wording is smaller than the research by an order of
  magnitude;
- the runtime edit has a stop rule, proof rule, and pruning rule;
- the packet says what not to import into `SKILL.md`.

If the packet is below this bar, do another research or rating pass. If it
meets this bar, promote the chosen wording into synthesis first, then ask or
explicitly decide before approving a runtime `SKILL.md` edit.
