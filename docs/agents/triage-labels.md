# Triage labels

These mappings preserve this repository's tracker roles and their meaning.
Items reconciled by tracker workflows must end with exactly one category role
and one state role below; unrelated labels may coexist. The consuming workflow
owns readiness evidence and permitted transitions. Direct coding does not require
a tracker item. A mapped label alone does not establish that it exists remotely
or that an item is ready or complete.

## Category roles

| Repository role | Tracker value | Meaning |
| --- | --- | --- |
| `bug` | `bug` | Defect in intended existing behavior. |
| `enhancement` | `enhancement` | New or changed behavior. |

## State roles

| Repository role | Tracker value | Meaning |
| --- | --- | --- |
| `needs-triage` | `needs-triage` | Unprocessed intake, not a completed disposition. |
| `needs-info` | `needs-info` | Missing reporter facts can change the disposition. |
| `ready-for-agent` | `ready-for-agent` | One bounded implementation-ready outcome with resolved prerequisites. |
| `ready-for-human` | `ready-for-human` | One named actionable human-owned step. |
| `implemented` | `implemented` | Current evidence establishes the requested outcome exists. |
| `wontfix` | `wontfix` | Authorized rejection, duplicate, supersession, or out-of-scope disposition. |

If these roles cannot truthfully represent a blocked item, report the mapping gap
and leave the affected transition unresolved. Do not misuse `needs-info` for an
internal dependency or advertise false readiness; independent cleanup can proceed.
