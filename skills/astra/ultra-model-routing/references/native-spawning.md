# Native spawning

Use before the first routed spawn on a host, after a relevant capability or
configuration change, or when observed routing disagrees with the request.

## Use the available contract

Preserve the current lead selection and native orchestration instructions.
Inspect the exposed spawn controls and any applicable custom-agent settings
needed to choose the route. Reuse established host facts; do not repeat a global
configuration audit for every child.

Pass both the selected model and reasoning effort. In the current Codex V2 tool
contract the fields are `model` and `reasoning_effort`, and routed fresh
contexts use `fork_turns="none"`. Native configuration files instead use
`model_reasoning_effort`. Use the field names exposed by the actual tool.

A task name describes the assignment; it does not by itself select a configured
agent role. Use a role only through supported role selection, and check its
model and effort fields: a custom role can take precedence over spawn values.
Skill `agents/openai.yaml` metadata does not register or enforce native child
model settings.

Follow the displayed tool contract. Do not send hidden arguments, assume numeric
fork values, or copy old configuration keys because a historical workaround
used them. A request for model routing does not authorize modifying global
configuration or installing a separate orchestrator.

## Give a fresh child the needed context

Provide the accepted outcome, constraints and decisions, relevant accessible
sources, candidate or base identity, ownership of writes, decisive checks, and
expected return. Supply information the child cannot infer or retrieve; link
to durable sources for detail. Keep consequential requirements in the brief
even when they increase its size.

For a reviewer, supply a stable candidate and the review obligations. For an
implementation worker, preserve the authorized effects and supported behavior.
For routine work, supply the settled production rule and an observable finish.

When an authorized child can delegate, include the routing policy or an
accessible explicit reference with instructions to load and apply it before
delegating, along with the assignment's remaining scope. Apply the same route
selection to descendants without instructing every child to create helpers.
Respect the host's actual concurrency limits.

## Continue work and handle mismatches

Use a suitable existing worker for coherent follow-ups. Recheck configuration
only when a role change, host update, resume behavior, or observed mismatch
makes the route uncertain. Do not impose a universal one-turn child lifecycle.

If an explicit route cannot be expressed, use an already available supported
role only if it selects the intended pair. Otherwise report the affected
assignment and missing capability; continue independent authorized work.
Do not claim that an inherited or substituted route met the policy. A missing
independent reviewer leaves its required review round incomplete.

When routing needs verification, prefer runtime configuration or execution
metadata over the child's self-description. Distinguish requested selection,
stored selection, and resolved inference effort. Report the limit when only a
request is observable; routine work does not require a new telemetry system.

## Version-sensitive facts

The inspected Codex source resolves selected Ultra through model metadata for
ordinary inference and separately chooses proactive delegation instructions.
An Ultra selection can therefore report `xhigh` while retaining Ultra mode.
Do not change the root to Extra High on the assumption that it is equivalent,
or hardcode Ultra as always meaning Max or Extra High.

The agent-facing guidance directs explicit overrides to fresh children even
though some backend tests exercise broader full-history behavior. Follow the
exposed guidance. Do not assume a historical depth setting enforces a V2
recursion limit, or that a Markdown skill enforces spending or publication gates.

Source checks, 2026-10-26:
[Subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[native override guidance](https://github.com/openai/codex/blob/4aca387e3ea9ac32382d814735e80cb7c2b327b9/codex-rs/prompts/src/multi_agent_instructions.rs),
[effort resolution](https://github.com/openai/codex/blob/4aca387e3ea9ac32382d814735e80cb7c2b327b9/codex-rs/protocol/src/openai_models/reasoning_effort.rs),
and [delegation-mode selection](https://github.com/openai/codex/blob/4aca387e3ea9ac32382d814735e80cb7c2b327b9/codex-rs/core/src/session/multi_agents.rs).
Use current host evidence when it differs; these source observations are not
a guarantee about every client or a reason to reproduce native orchestration.
