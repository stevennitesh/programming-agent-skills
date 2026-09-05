# Delegation guidance

Give each worker a concrete task, exclusive ownership or a defined seam, necessary
context, expected evidence, and a completion condition. State which adjacent work
it should not repeat. Ask workers to report contradictions to the root. Keep
fanout at the root rather than asking workers to delegate further.

Use fresh context for independent judgment and review. With `spawn_agent`, set
`fork_turns="none"` for that purpose. Pass conversation history only when the
subtask needs it. Preserve the user's model selection; otherwise use the current
tool's inheritance defaults.

Keep a review candidate fixed through exclusive custody or an immutable snapshot.
If it changes, review the final candidate before relying on the findings. Inspect
returned artifacts and integrate the work before declaring the combined task done.

## Routed provider failures

For a routed worker's HTTP 429, follow a supplied retry delay when available and
resume the same worker once so its evidence survives. Replace it only if it cannot
resume. Report a persistent provider limitation rather than looping retries.
