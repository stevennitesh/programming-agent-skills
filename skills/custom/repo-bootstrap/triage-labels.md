# Triage Labels

This guide maps shared skill-pack roles to this repository's tracker values.
Category roles identify the kind of request. State roles provide transition
orientation only; a role alone is not evidence that its transition is valid.

## Category Roles

| Skill-pack role | Tracker value |
| --- | --- |
| `bug` | `bug` |
| `enhancement` | `enhancement` |

## State Roles

| Skill-pack role | Tracker value |
| --- | --- |
| `needs-triage` | `needs-triage` |
| `needs-info` | `needs-info` |
| `ready-for-agent` | `ready-for-agent` |
| `ready-for-human` | `ready-for-human` |
| `implemented` | `implemented` |
| `wontfix` | `wontfix` |

State orientation is intake (`needs-triage`), reporter wait (`needs-info`),
agent handoff (`ready-for-agent`), human handoff (`ready-for-human`), or terminal
disposition (`implemented`, `wontfix`).

When a skill names a role, use its mapped tracker value. Every triaged work item
carries exactly one category role and one state role. When adapting this guide,
change only the tracker values; keep the shared role names.

## Wayfinding Labels

For hosted trackers, these fixed labels identify Wayfinder maps and ticket
types. They are not triage roles.

- `wayfinder:map`
- `wayfinder:research`
- `wayfinder:prototype`
- `wayfinder:grilling`
- `wayfinder:questionnaire`
- `wayfinder:task`
