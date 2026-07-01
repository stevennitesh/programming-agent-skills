# Further Research Opportunities

This note captures optional targeted research lanes for later gap passes.

The core approach is already clear:

```text
software-engineering taste term
  -> agent execution surface
  -> evidence gate
```

Do not delay synthesis or skill work for another broad source hunt. Use these
lanes only when a facet has a concrete gap. Compare any finding against the
accepted target spine and skill-writing formula in
[`../../synthesis/target-spine.md`](../../synthesis/target-spine.md).

## Research Lanes

| Priority | Lane | Why It Matters | Vocabulary To Sharpen |
| ---: | --- | --- | --- |
| 1 | Agent evaluation and benchmarks | Keeps agent quality tied to observable task success, regressions, and repo-state proof instead of impressions. | `evaluation harness`, `trajectory evaluation`, `task success`, `regression`, `LLM-as-judge`, `criteria-bound review` |
| 2 | Context engineering and memory | The strongest missing pillar for long-running coding agents: what to load, compress, retrieve, preserve, and distrust. | `context engineering`, `context budget`, `memory`, `retrieval`, `compression`, `context pointer`, `lost-in-context` |
| 3 | Agent safety, prompt injection, and tool-use guardrails | Coding agents touch real files, shell commands, dependencies, secrets, browsers, and untrusted text. | `guardrail`, `trusted source`, `untrusted context`, `tool permission`, `sandbox boundary`, `policy boundary` |
| 4 | Empirical studies of AI coding quality | Identifies where coding agents actually fail in practice: review burden, technical debt, insecure code, comprehension loss, and governance gaps. | `review bottleneck`, `AI-authored debt`, `comprehension loss`, `security regression`, `governance gap` |
| 5 | Official agent-building manuals | Provides current operational vocabulary from the major model/tool ecosystems without letting vendor language replace repo-specific proof. | `agent`, `tool`, `handoff`, `guardrail`, `trace`, `structured output`, `eval`, `instruction hierarchy` |
| 6 | Cognition and expertise | Strengthens the human and model-facing vocabulary around expert behavior, cognitive load, attention, and deliberate practice. | `cognitive load`, `context load`, `legwork`, `expert behavior`, `deliberate practice`, `chunking`, `mental model` |

## Candidate Source Targets

Use these as starting points, not as already-final authority. Verify each source
before importing terms or claims into the core vocabulary.

### Agent Evaluation And Benchmarks

- CodeLLM and coding-agent benchmark surveys.
- SWE-bench follow-ups and benchmark critiques.
- Agent evaluation surveys focused on task success, trajectories, and
  repeatable evaluation.
- Practical coding-agent leaderboards such as Aider's public benchmarks.

### Context Engineering And Memory

- Anthropic's context engineering writing.
- Context engineering surveys.
- Agent memory surveys.
- Lost-in-the-middle and long-context reliability research.
- Retrieval and contextual retrieval papers or manuals.

### Agent Safety And Tool-Use Guardrails

- Prompt-injection benchmarks.
- Prompt-injection defense catalogs.
- Tool-use safety papers.
- Secure coding-assistant studies.
- Vendor docs on tool permissions, sandboxing, untrusted input, and policy
  boundaries.

### Empirical AI Coding Quality

- Developer productivity studies for AI coding assistants.
- Studies on AI-generated code quality, security, and maintainability.
- Studies on code review burden and comprehension effects.
- Field reports from professional teams adopting coding agents.

### Official Agent-Building Manuals

- OpenAI Codex and Agents docs.
- Anthropic agent, skills, and Claude Code docs.
- Google agent and evaluation docs.
- Microsoft agent design-pattern and prompt-engineering docs.
- Hugging Face agent course material.

### Cognition And Expertise

- `The Programmer's Brain`.
- Cognitive load theory applied to programming.
- Cognitive dimensions of notation.
- Deliberate practice and expertise research.
- Empirical software engineering work on comprehension, review, and debugging.

## Output Of The Gap Pass

The research pass should produce:

- a short source list for each lane;
- the strongest terms worth importing;
- terms to avoid because they are vague, overloaded, or decorative;
- one or two bridge patterns per lane;
- completion criteria or evidence gates that make the terms operational.

## Stop Rule

Stop the research pass when each lane has enough evidence to answer:

```text
What professional behavior should this vocabulary recruit?
What agent execution surface makes that behavior happen?
What evidence gate prevents premature completion?
```

More sources are only useful if they change one of those answers.
