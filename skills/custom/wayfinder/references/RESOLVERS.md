# Resolver routes

Load only the selected ticket's route. Wayfinder owns the question, decision
owner, acceptance evidence, and map reconciliation. Each resolver owns its own
method, evidence judgment, mutation, and completion.

For every invoked resolver, pass the selected question, why it matters,
decision owner, acceptance evidence, relevant identifiers and Source Trace,
applicable mutation boundary, return owner, and Wayfinder re-entry. Each row
adds only route-specific inputs.

| Type | Route |
| --- | --- |
| Research | Invoke `$research` for one source-answerable question. Pass the map use, scope, applicable state, approved note path or no-write mode, and Wayfinder return owner. |
| Prototype | Invoke `$prototype` for one runnable design question. Pass the named human judge or objective rule, representative evidence, bounded run, mutation authority, and cleanup or custody. |
| Grilling | Invoke `$grilling` for one conversation-only user decision. Use `$grill-with-docs` only when that same decision needs live domain reconciliation. |
| Questionnaire | Return the recipient, downstream decision, needed-back items, authorized path, answer-return destination, and exact `$to-questionnaire` plus Wayfinder re-entry instruction. Do not invoke the explicit-only skill. |
| Task | Establish one bounded repository or operational prerequisite. It may inspect state but cannot perform durable mutation. A required live human action becomes a wait. |

A supported answer, confirmed decision, or objective verdict resolves the
ticket. A source conflict, missing authority, unavailable prerequisite, or
evidence gap blocks it with one observable intervention. A human or external
return that cannot arrive in this invocation becomes waiting with its owner and
required evidence. Governing evidence may put the question out of scope.

A questionnaire file is waiting evidence, not an answer. Only matching
attributable stakeholder answers can resolve the ticket. A malformed,
mismatched, unauthorized, or non-admitted return records no outcome.

If a resolver cannot return in this invocation, release every claim before
stopping. Record a durable wait only when its owner, trigger, and required
return are exact.
