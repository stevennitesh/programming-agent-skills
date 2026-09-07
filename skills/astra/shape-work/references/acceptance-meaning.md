# Acceptance meaning

Read the part whose omission could change the requested behavior. These questions
preserve a contract; they do not prescribe a test framework or exhaustive matrix.

## Results cross a boundary

When one stage feeds another, identify the actual produced result, its ordinary
consumer, and the meaning that must survive the handoff. Include materially
different successful and rejected outcomes. Preserve value or null, issues,
availability, provenance, and identity when the source makes them meaningful.
Do not replace a distinguishing field or state with a vague category.

For independent items, settle whether failure rejects one item or the entire
request, and where each issue belongs. Bind companion metadata to the result it
describes. Use a mixed case when interactions between valid and invalid inputs
could otherwise remain ambiguous.

## State and representation carry meaning

Identify authoritative data and writers, what persists, and how ordinary readers
use it. Preserve source-defined identity, units, calendar-date versus instant
meaning, derivation, and schema compatibility across materially different states.
If accepted inputs or rules conflict, state precedence and the observable result.
Name changes that advance a governing version when version semantics matter.

Include compatibility, migration, cutover, rollback, or removal obligations only
when real consumers or persisted state require them. For a visual or placement
rule, state the relevant context and observable relation, not a guessed mechanism.

## Completion and evidence differ

For measured requirements such as speed, accuracy, cost, or capacity, establish
the relevant workload, metric, threshold or comparison baseline, and operating
conditions. For numerical claims, include material tolerance and data assumptions.
Keep unknown targets explicit and resolve decision-bearing gaps with their owner;
do not invent numbers or treat an unmeasured aspiration as proved acceptance.

For retries, escalation, or multiple stopping conditions, distinguish success
from exhaustion, cancellation, and unresolved work. Include the case where two
criteria disagree if their precedence changes the result.

Acceptance should name the cheapest evidence capable of establishing the claim.
A deterministic fixture may prove a rule while leaving a live integration,
representative performance, or production-shaped claim unproved. Preserve the
accepted evidence requirement and any safe-input condition; if it cannot be met,
record that gap rather than silently weakening acceptance. A prior prototype
supports only the question and conditions it actually exercised.
