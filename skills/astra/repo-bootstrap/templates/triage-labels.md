# Triage labels

Record the repository's chosen categories, states, meanings, and required
cardinality. The consuming workflow defines readiness evidence and permitted
transitions. Direct coding does not require a tracker item.

The rows below are optional starting examples, not a required taxonomy. Reuse
established labels or fields, adapt the roles to the actual workflow, and state
any one-category/one-state or other constraints the repository adopts. Preserve
distinct meanings for actionable work, unresolved blockers, completion, and
rejection. Record the selected mapping during setup; agents should not rename
states or change their meaning during an operation.

## Category roles

| Role | Tracker value |
| --- | --- |
| `bug` | `bug` |
| `enhancement` | `enhancement` |

## State roles

| Role | Tracker value |
| --- | --- |
| `needs-triage` | `needs-triage` |
| `needs-info` | `needs-info` |
| `ready-for-agent` | `ready-for-agent` |
| `ready-for-human` | `ready-for-human` |
| `implemented` | `implemented` |
| `wontfix` | `wontfix` |

A mapping does not establish that remote labels exist. Verify the relevant
values before an operation needs them. A state label alone does not prove
completion or remove an unresolved dependency.
