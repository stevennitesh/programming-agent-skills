# Triage Labels

The skills speak in terms of category roles and state roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

## Category Roles

| Role in mattpocock/skills | Label in our tracker | Meaning                    |
| ------------------------- | -------------------- | -------------------------- |
| `bug`                     | `bug`                | Something is broken        |
| `enhancement`             | `enhancement`        | New feature or improvement |

## State Roles

| Role in mattpocock/skills | Label in our tracker | Meaning                                  |
| ------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`            | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`              | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`         | `ready-for-agent`    | Fully specified, ready for an unattended Codex implementation session or delegated implementation subagent |
| `ready-for-human`         | `ready-for-human`    | Requires human implementation            |
| `implemented`             | `implemented`        | Implemented, reviewed, committed, and recorded by an implementation skill |
| `wontfix`                 | `wontfix`            | Will not be actioned                     |

When a skill mentions a role, use the corresponding label string from these tables.

Every triaged issue or PR should carry exactly one category role and one state role.

Edit the right-hand column to match whatever vocabulary you actually use.
