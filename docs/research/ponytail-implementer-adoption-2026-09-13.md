# Ponytail implementer adoption evidence

Research snapshot, 2026-09-13. This note records source evidence and adoption
decisions; it is not runtime guidance for the lead or implementer.

## Source and coverage

Local source: `.tmp/repos/ponytail`, clean at
`356918eba965ee1eac64bd3a7f0dd02108350de5`, package version `4.9.0`.
Upstream: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/356918eba965ee1eac64bd3a7f0dd02108350de5).

The complete tracked inventory contains 162 files. The assessment covered all
repository areas through that inventory and representative source inspection;
it was not an exhaustive line-by-line audit of every file. Generated rule copies,
translated introductions, binary art, and every host adapter were not separately
read in full. No upstream benchmark or host installation was run.

| Area | Inspected evidence | What it establishes |
| --- | --- | --- |
| Core instructions | `AGENTS.md`, all six canonical `skills/*/SKILL.md` files | Implementation persona, review/audit/debt/scoreboard/help responsibilities, and competing scope pressures |
| Runtime delivery | `hooks/ponytail-instructions.js`, `ponytail-activate.js`, `ponytail-subagent.js`, `ponytail-runtime.js`; representative Pi extension, Hermes adapter, MCP instruction selector | Repeated activation, persisted modes, broad subagent injection, and reuse of the canonical instruction builder |
| Packaging and commands | `package.json`, `.codex-plugin/plugin.json`, `commands/ponytail.toml`, `scripts/build-openclaw-skills.js`, `scripts/check-rule-copies.js`, `.github/workflows/test.yml`, tracked adapter inventory | Platform distribution and copy synchronization are substantial parts of the repository, separate from implementation judgment |
| Documentation and examples | README introduction/results, `docs/agent-portability.md`, `docs/platform-native.md`, CSV and debounce examples | Native-feature preference is useful, but examples and lookup substitutions cannot establish semantic equivalence for a different task |
| Verification and research | Benchmark and agentic READMEs, behavior grader and tests, correctness-grader search, command/hook-test search, agentic completeness and complexity judges, comprehension/reuse result note | Different evidence types have different limits; small code and complete behavior require separate assessment |
| Rights and provenance | `LICENSE`, package author and source metadata | MIT source with DietrichGebert copyright notice |

## Retained and excluded

The standalone adaptation retains comprehension before simplification, local
reuse before new implementation, considering built-in capabilities, fixing the
owner of a violated rule, and avoiding speculative machinery. It evaluates
choices by preserved behavior and maintenance burden rather than shortest text.

It does not import upstream persistent modes, hooks, broad discovery, automatic
subagent injection, installation, statusline setup, audit/debt commands, or
scoreboards. Those are distribution or independent-workflow concerns, not part
of a bounded implementer's job. Upstream review intentionally excludes
correctness and performance; Astra change-review continues to own the complete
quality judgment.

Several upstream prescriptions are deliberately narrowed: line/file minimization
does not score success; required outcomes cannot be replaced by an unsolicited
smaller product; abstractions can own real policy without multiple callers;
shared functions are changed only when affected callers share the rule; and
verification follows the repository contract without a fixed one-check ceiling.
Material limits belong at their existing owner, without mandatory marker syntax
or a new ledger. Platform lookup examples are suggestions to investigate, not
compatible replacements by definition.

## Evidence limits

The upstream benchmark documentation distinguishes single-shot output-size
comparisons from agentic edits, reports that an earlier baseline was contaminated
by automatic activation, and separates executable safety checks from structural
or model-judged evidence. The inspected behavior grader uses heuristic text
signals; its unit tests establish grader behavior, not production correctness.

The comprehension/reuse note reports improvement on a seeded shared-owner bug
for some models, while its reuse probes did not demonstrate an advantage over
baseline. That supports making root-cause tracing actionable without claiming
universal gains. Historical examples can omit behavior such as resource cleanup;
they are not accepted implementation templates.

No claim is made that this adaptation reduces runtime, tokens, cost, or defect
rates. Structural validation and editorial scenarios can establish packaging and
instruction coherence; a representative delivery comparison is still needed to
measure the worker-only pairing.

An author challenge found that the initial adaptation repeated much of the
engineering contract, weakening its likely incremental value. The refinement
concentrates on implementation choices: distinguish necessary outcomes from
optional machinery, check existing and native capabilities for actual fit, stop
searching when sufficient, and remove displaced machinery within scope. General
verification and handoff rules remain with their existing owners. This is a
hypothesis about more useful wording, not demonstrated improvement for Sol or
the coordinated delivery workflow.

## Packaging and context boundary

The new package is `skills/astra/ponytail-implementer/`. It is original, concise
Astra wording informed by the pinned upstream, with the upstream MIT notice
included as `LICENSE` so attribution travels with managed installation. No
upstream executable code, examples, hooks, or assets are vendored.

The skill is explicit-only and addressed to an assigned implementer. The lead
uses its name, path, and content identity to dispatch it, and reviews the result
against the accepted plan and engineering contract without loading its body.
That is an instruction and invocation boundary, not a filesystem access control.
The skill does not load this research note or depend on the upstream clone.
