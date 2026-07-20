# Triage Labels

The skills speak in terms of category roles and state roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

## Category Roles

| Skill-pack role | Label in our tracker | Meaning                    |
| --------------- | -------------------- | -------------------------- |
| `bug`                     | `bug`                | Something is broken        |
| `enhancement`             | `enhancement`        | New feature or improvement |

## State Roles

| Skill-pack role | Label in our tracker | Meaning                                  |
| --------------- | -------------------- | ---------------------------------------- |
| `needs-triage`            | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`              | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`         | `ready-for-agent`    | Fully specified, ready for an unattended Codex implementation session or delegated implementation subagent |
| `ready-for-human`         | `ready-for-human`    | Requires human judgment, access, design, testing, or merge action |
| `implemented`             | `implemented`        | Implemented, reviewed, committed, and recorded by an implementation skill |
| `wontfix`                 | `wontfix`            | Will not be actioned                     |

When a skill mentions a role, use the corresponding label string from these tables.

Every triaged work item should carry exactly one category role and one state role.

Edit the right-hand column to match whatever vocabulary you actually use.

## Wayfinding Labels

`$wayfinder` uses these fixed labels for map and ticket mechanics. They are not triage roles.

- `wayfinder:map`
- `wayfinder:research`
- `wayfinder:prototype`
- `wayfinder:grilling`
- `wayfinder:diagnosis`
- `wayfinder:questionnaire`
- `wayfinder:design`
- `wayfinder:task`

## Provisioning

For GitHub or GitLab, `$repo-bootstrap` verifies every mapped and fixed label exists and creates only missing labels after approval. Local Markdown uses equivalent unprefixed `Type:` values and creates no external labels.
