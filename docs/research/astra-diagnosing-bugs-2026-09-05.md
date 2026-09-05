# Astra diagnosing-bugs rewrite

This records source selection and review for the optional hard-debugging skill.
It is not evidence of improved diagnosis performance over the model baseline.

## Direction

Keep a specialized method for causally ambiguous failures: faithful observation,
backward and forward tracing, falsifiable explanations, discriminating probes,
and verification against the original symptom. Ordinary fixes do not require it;
an investigation that reveals a simple cause can still finish normally.

The main skill owns evidence, causal reasoning, repair scope, and truthful return.
One conditional reference covers intermittent failures, observer effects, test
pollution, cross-system correlation, environment/restart differences, historical
comparison, reduction, and performance regressions. No scripts or universal test
framework are added; the repository and actual failure determine the instrument.

## Source selection

The custom skill supplies most of the core: expected versus actual behavior,
faithful feedback, strongest viable alternative, useful reduction, affected
callers, authorized fix, original-loop verification, and cleanup. The rewrite
removes route-mismatch stops and preserves useful evidence instead of requiring
all disposable artifacts to vanish. Mitigation remains distinguishable from a
supported root-cause repair.

Compared local upstream snapshots without fetching newer revisions:

| Source | Commit | Selection |
| --- | --- | --- |
| Matt Pocock | `3cca18b368ae95cdbdebbff572ccafa662551015` | Keep the faithful feedback loop, replay/differential/bisection options, reduction, real-pattern regression, original-scenario verification, and redaction. Reject a mandatory seconds-fast red loop before reasoning, exhaustive minimality, 3–5 hypotheses, fixed stress counts, and required human-loop scripts. |
| Superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Keep backward tracing, comparing working/failing cases, targeted boundary evidence, and condition-based waits. Reject mandatory instrumentation at every boundary, TDD for all cases, fixed failure-count escalation, and validation at every layer. A correct guard belongs where its invariant can be enforced. |
| Pstack | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Keep causal repair and persisted-state investigation for restart failures. Reject treating state deletion as proof of the proper fix, banning guards categorically, or requiring a local reproduction before any useful causal work. |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | Keep shared-owner and sibling-path investigation. Reject shortest-diff reasoning or assuming the shared function is always the correct enforcement owner. |

## Quality controls

An instrument must reach the original mechanism; setup errors, overload artifacts,
and nearby failures cannot substitute for the reported symptom. Observation and
intervention can change timing. A green run after a patch supports neither a
universal elimination claim nor a unique causal explanation by itself.

Use incident evidence when safe local reproduction is unavailable. Distinguish
attributable observations, plausible hypotheses, mitigation, supported cause,
and verified repair. Multiple contributing conditions can be causal. A failed
sequence of patches warrants revisiting evidence and assumptions, not automatically
redesigning the architecture. Keep live effects within existing authority.

## Challenger review

Two fresh-context reviewers challenged a fixed candidate read-only. The causal
review compared custom and upstream detail and passed the stated hard-debugging
scenarios. The workflow review found that completion wording could permit a
partially verified repair to be called complete. The final wording requires the
scoped repair and passing required checks, distinguishes statistical uncertainty,
and leaves unavailable required verification incomplete. The root also added
conditional reverification after removing outcome-changing instrumentation.
The workflow reviewer rechecked both corrections and passed.

Skill and repository validation, local links, and whitespace checks passed.

## Verification limits

Instruction structure and source comparison can reveal omitted safeguards and
contradictions, but do not demonstrate debugging effectiveness. A later behavioral
evaluation should include intermittent, environmental, and misleading-reproducer
cases rather than only deterministic bugs. The legacy skill remains unchanged;
creating the Astra source does not install it globally.
