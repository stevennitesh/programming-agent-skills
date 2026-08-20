---
name: prototype
description: Prototype one bounded design question with a disposable runnable probe; exclude production proof, uncertain defects, and multi-decision design.
---

# Prototype

Answer one bounded design question with a disposable runnable probe. The answer
may inform later work; the probe is not production code or production proof.
The caller owns adoption, durable truth, implementation, and any next route.

## 1. Frame

Confirm that one unsettled design choice can be answered by one runnable
question. State the decision it informs, the representative cases, what
observation would decide it, and the allowed paths and effects.

If the answer needs human judgment, name the judge. Otherwise choose the
objective rule before observing results. Do not invent or tune a material
threshold after decisive evidence.

Use one invocation-owned `.tmp/prototype/<question-slug>/` root by default. An
explicitly authorized durable result may use `.scratch/<feature>/prototype/`.
Touch application paths only when real context is necessary, the mutation
authority for the allowed paths and effects is present and verified, and the
repository proves the whole probe is development only or excluded from the
build. A caller packet transports authority; it does not create it.

Ask only when a missing fact changes the question, judge, evidence, effects, or
authority. When an existing system instead has a hard failure needing causal
investigation, recommend `$diagnosing-bugs` and stop before mutation with the
intact symptom evidence.

## 2. Choose

Read only the branch that owns the needed evidence:

| Question | Load |
| --- | --- |
| State, rules, data, API shape, or interface behavior | [LOGIC.md](LOGIC.md) |
| Visual hierarchy, density, navigation, flow, or interaction | [UI.md](UI.md) |
| Comparative latency, throughput, resources, variability, or scale | [MEASURE.md](MEASURE.md) |

Keep independent questions separate.

## 3. Build

Build the smallest artifact that could change the answer. Prefer
repository-native tools, in-memory state, direct control flow, and one obvious
way to run it. Keep relevant state visible. Add only enough structure and error
handling to make the evidence trustworthy.

Prefer a cheap authorized observation over asking the user an empirical
question. Ask for product direction, human judgment, or authority that an
experiment cannot supply.

## 4. Observe and decide

Run the actual behaving, rendered, or measured artifact against the
representative cases. Source inspection and a successful start are not a
verdict. Apply the named human judgment or the objective rule chosen before the
run.

Return the supported answer or an exact residual with the observation and its
material limits. State which production claims remain unsupported. Prototype
evidence answers only the framed design question.

## 5. Clear and return

Stop live processes and release Prototype-owned resources. Delete or restore
disposable changes. Retain an artifact only at an authorized path after the
recipient accepts custody and cleanup; read back durable evidence. When cleanup
would overwrite unrelated or ambiguously owned work, preserve the conflict and
report it.

Return the answer or residual, evidence, limits, and any retained artifact to
the current caller, or to the user for direct work. Start no downstream work.

## Completion

Complete when the question is answered or truthfully unresolved, the caller
has judgeable evidence, and no unauthorized or live Prototype state remains.
