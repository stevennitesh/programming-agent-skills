# Domain modeling inside Astra shape-work

This extends shape-work with a direct domain clarification and settled-record
reconciliation path. It does not add a separate skill or change the engineering
contract. The runtime method lives in one conditional reference; durable-decisions
continues to own publication and safe dependent writes.

## Decisions

Direct domain requests bypass feature interviewing, specification, ticketing,
and implementation. During shaping, the same path can resolve meaningful terms,
invariants, and relationships before dependent decisions proceed. A valid return
is a clarified distinction, verified record, proposed wording, no change, or an
exact unresolved question.

The repository's domain route now names Astra shape-work as the owner and retains
an explicit legacy domain-modeling route for existing consumers and validation.
Existing custom skill packages are preserved for legacy callers. No global skill was
installed and no current domain meaning or ADR was rewritten by this change.

## Source selection

Custom domain-modeling, CONTEXT-FORMAT, and ADR-FORMAT supply the key details:
canonical meaning within each context, independent meanings across contexts,
translation and responsibility at relationships, code versus intended behavior,
lazy records, no-change outcomes, coherent reconciliation, and partial ADR
supersession. Existing approval and write authority apply without inventing a
new approval gate for an already-authorized request.

Matt Pocock's domain-modeling at local snapshot
`3cca18b368ae95cdbdebbff572ccafa662551015` contributes concrete scenario challenges,
terminology collisions, code comparisons, and the three-part ADR worthiness test.
Do not copy automatic inline writes, glossary-only context, or mandatory root
paths that could displace a repository's existing conventions.

Pstack's principle-model-the-domain at
`93b00b89ef425a9c1bac0d0b317dfc49c930ac99` contributes precise valid states and
knowledge-based ownership. Preserve the semantic constraint in this path; choosing
specific reducers, queues, adapters, or data structures belongs to codebase-design
or implementation. Do not turn a domain-document request into a code refactor.

This was targeted comparison of domain-specific sources, not a new exhaustive
upstream scan. No upstream fetch was performed.

## Challenger review

Two fresh-context reviewers checked the fixed candidate read-only. Workflow review
passed. Quality review restored two useful details: reconcile affected existing
acceptance/references after a domain change, and keep predecessor ADR applicability
explicit across multiple partial supersessions. Both corrections were incorporated.

Repository and skill validation passed after preserving the legacy route alongside
the Astra pointer. This compatibility adjustment does not activate legacy workflows
for ordinary Astra requests.

## Verification limits

Validation and independent textual challenges check routing, source preservation,
and coherent instructions. They do not demonstrate improved modeling or agent
behavior. Domain correctness still depends on the project's actual authority and
evidence; a well-formed document is not proof of a correct model.
