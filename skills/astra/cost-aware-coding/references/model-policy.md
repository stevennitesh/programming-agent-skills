# Model policy

Use the user's working assumption that Astra is roughly five times as expensive
as Sol to reserve Astra attention for decisions where it adds value. This is a
routing assumption, not a current pricing table or a measured savings claim.
Account for the cost of the whole accepted result, including reviewer and helper
usage, handoffs, verification, and repair.

## Role assignments

| Role | Model and effort | Responsibility |
| --- | --- | --- |
| Lead | **User-selected starting model and effort**, normally Astra Medium or XHigh | Planning, architecture, codebase ownership, consequential decisions, orchestration, and final acceptance |
| Worker | **Sol 6.1 High** by default; **Sol 6.1 Max** for especially difficult implementation | Investigation, implementation, debugging, verification, and repair |
| Bounded worker | **Luna Max** | Clearly bounded search, retrieval, extraction, bulk writing, and mechanical work with limited judgment, even with large inputs or outputs |
| Isolated reviewer | **Astra Medium or XHigh** | Independent candidate assessment or a complementary scope under change-review; the lead can instead perform review directly |

The user starts the work with the lead. Do not select, replace, or change that
session's model or effort. Normal Astra work uses Medium; XHigh is the strongest
Astra option in this policy for demanding scientific reasoning, state-of-the-art
methods, and similarly intensive architecture or review. These assignments express
the user's operating policy, not a universal ranking of model quality.

## Choose effort and support

Sol is the main implementation worker, including for difficult tasks. In this
workflow, Sol means exactly `gpt-6.1-sol`; use `high` by default and `max` when
the implementation's reasoning demands justify the additional effort. The lead
may choose Max up front for clearly demanding work or raise effort after observing
a reasoning limit. Routine corrections do not require escalation.

Use Astra Medium for normal reviewer or advisory assignments. Use Astra XHigh
when deep scientific, state-of-the-art, or other consequential reasoning can
materially change the result. Resolve architecture or domain questions with Astra
and return a clear decision to Sol when that lets implementation continue.

If implementation capability remains the bottleneck, an Astra implementation
takeover is an exception the lead may choose when its benefit justifies the cost.
Transfer write custody before replacing the worker. There is no mandatory
promotion ladder or fixed number of attempts, and subagent routing never changes
the user's lead session.

Luna work is bounded by scope, judgment, and observable acceptance, not by the
number of files or tokens it reads or writes. Large searches and bulk writing are
good candidates when the selection rules, source facts, or writing pattern are
clear. Examples include populating templates, drafting repetitive documentation
from supplied facts, and producing boilerplate from an established pattern.
Keep instructions and handoff summaries focused while delivering the complete
requested output. Move work to Sol when it needs open-ended implementation judgment
or substantial debugging, rather than routing it upward just because input or
output volume grew.

The allowed subagent efforts are **Sol High or Max, Astra Medium or XHigh, and
Luna Max**. Preserve an explicit user-selected route within the task's constraints.
Do not use stronger effort to compensate for missing requirements, contradictory
acceptance, permissions, or broken environments.

## Availability

Pass model and effort explicitly using the host's supported controls. Preserve
the Sol version pin; do not silently substitute `gpt-6-sol` or a latest-model alias.
If the intended route is unavailable, choose a supported route within the allowed
efforts and role boundaries, and report substitutions that materially affect the
user's cost or quality intent. Surface the limitation if no suitable route exists.
