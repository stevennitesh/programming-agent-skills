# GPT-6 model policy

Use this policy for cost-aware routing within the GPT-6 family. Model and reasoning
effort are part of the token-efficiency strategy, not interchangeable implementation
details.

## Default roles

| Role | Default route | Use when |
| --- | --- | --- |
| Lead | **Astra Medium** | Consequential reasoning, shaping, ambiguous decisions, orchestration, exception handling, and final review |
| Implementer | **Sol Medium** | Substantial repository investigation, coding, debugging, verification, and repair |
| Bounded worker | **Luna Low** | Fine-grained edits, extraction, classification, targeted inspection, or other compact tasks with clear inputs and cheap verification |
| Bounded coordinated worker | **Luna Medium** | A still-bounded task that needs coordinated edits or more complete execution than Luna Low reliably provides |

These are starting routes, not claims that a model always wins a task. Preserve an
explicit user-selected route when it is available and compatible with the task.

## Spend stronger reasoning where it changes the result

Keep Astra on lead-owned decisions rather than routine implementation throughput.
Use Sol instead of Luna when the task requires substantial repository reasoning,
long debugging context, nontrivial implementation judgment, or verification whose
failure would be expensive to reconstruct.

Use Luna only when the assignment can remain compact and the result is cheap to
judge. Cheap inference is not a cheap workflow when Astra must provide a large
brief, reconstruct missing context, or deeply verify the output.

Do not split one coherent Sol assignment into many Luna tasks merely to reduce
per-token price.

## Effort escalation

Start at the default effort above. Raise effort only when evidence suggests that
more reasoning can change the result:

- For a difficult consequential lead decision or review, raise Astra effort before
  moving implementation responsibility into the lead.
- For a difficult implementation or debugging task, raise Sol effort when the
  failure reflects reasoning capability rather than missing requirements,
  permissions, environment, or acceptance.
- Raise Luna effort only while the task remains genuinely bounded; move the task to
  Sol when it has grown into substantial implementation reasoning.

Prefer the lightest model and effort that reliably meet acceptance. Repeated
failure at a lower tier is not useful savings when it creates expensive briefing,
repair, or review churn.

Availability and supported effort controls are host-dependent. If a requested
route is unavailable, use the closest supported route that preserves these role
boundaries and report the substitution when it materially affects the user's cost
or quality intent.
