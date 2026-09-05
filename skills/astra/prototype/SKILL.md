---
name: prototype
description: Build and observe a small runnable experiment to resolve an empirical design question, such as feasibility, state behavior, interaction, or comparative performance. Exclude ordinary implementation, diagnosis of an existing defect, and architecture decisions that need no experiment.
---

# Prototype

Produce evidence that can change a design decision. Codebase-design owns the
broader architecture choice; this skill owns the experiment. A direct prototype
request ends with findings and any requested demo. When embedded in authorized
implementation, return the evidence so that work can continue without another
approval gate. A successful probe does not establish production readiness.

## 1. Frame an answerable question

Identify the uncertainty, the decision it affects, and an observation that would
support or reject the proposed direction. Reuse a question supplied by the caller;
do not reopen settled requirements. If source or an existing result already
settles it, return that evidence without building a ceremonial prototype.

Choose representative conditions and the comparison rule before the decisive
run. Include a case that could expose the approach's limitation, not just its
best demonstration. For subjective choices, distinguish your recommendation
from the intended user's judgment. An experiment cannot choose an unresolved
product priority on their behalf.

Keep the question bounded by the decision. Several cases or variants may belong
to one experiment; unrelated questions do not. If exploration reveals a better
question or metric, state the revision and gather evidence for it rather than
silently changing the success rule to fit a result.

## 2. Choose the necessary fidelity

Build the smallest artifact that can distinguish the relevant outcomes. Keep
the mechanism under investigation real: an in-memory simulation cannot establish
database isolation, and a static screen cannot establish an interaction. Simplify
incidental infrastructure, state, and polish. Name substitutions that limit the
answer. If the required environment is unavailable, return the remaining gap
instead of presenting a substitute as equivalent evidence.

For state, logic, or integration behavior, visual layout or interaction, or
variable measurements, read the relevant section of
[Evidence methods](references/evidence-methods.md).
Choose the form for the question and its recipient: a script, focused harness,
interactive demo, or repository-native test may each be the cheapest valid probe.
Do not build a demo UI for a machine-checkable question unless it helps judgment.

## 3. Build and observe

Use an invocation-owned scratch location, following repository conventions or
`.tmp/prototype/<question>/` by default. Identify existing work before editing.
When real application context is necessary, use an isolated checkout or a
verified development-only path within existing authorization. A hidden link or
a name containing "prototype" does not keep a route out of production.

Keep experiment effects within authorized targets. Use scratch data and stub
unrelated mutations; a disposable file location does not isolate a shared service
or database. Track the processes and resources the probe creates so they can be
released after success, failure, or interruption.

Run the actual behavior, render, or measurement under the framed conditions.
Check that the harness exercises the intended mechanism and exposes the result;
a successful start is insufficient. Add assertions or harness checks when they
prevent misleading evidence, without turning disposable code into a production
test project.

Stop when the evidence distinguishes the options, exposes a blocking limitation,
or further runs would not resolve the remaining uncertainty. Improve a failed
harness when practical; distinguish a broken instrument from a failed design.
Do not expand the experiment into implementation to obtain a positive verdict.

## 4. Return evidence and settle the artifacts

Return the answer or precise unresolved question, the decisive observations,
and the conditions and substitutions that limit the conclusion. Preserve enough
input, command, environment, and output detail to judge the claim or repeat the
important observation. Use the caller's existing artifact when suitable; no
separate report, issue, or branch is mandatory.

Stop probe-owned processes and release temporary resources. Restore only changes
you own; preserve and report conflicts with unrelated work. Keep a requested demo
or evidence artifact at a clear path with rerun instructions. Do not delete an
artifact still awaiting the requested human evaluation. Otherwise remove
disposable material after preserving the findings. A live preview may remain
only when requested or needed for an ongoing authorized review; report its
location and how to stop it.

Complete when the caller has judgeable evidence or a truthful gap, and retained
artifacts and resources have an explicit purpose. Adoption belongs to the calling
work: reassess any reused code against production requirements and prove its real
integration. Neither automatic promotion nor a mandatory rewrite follows from
the experiment's success.
