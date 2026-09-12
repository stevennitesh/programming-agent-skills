# Issue tracker: GitHub

Issues and specifications live in GitHub Issues.

Project: [stevennitesh/programming-agent-skills](https://github.com/stevennitesh/programming-agent-skills).
Use this guide for tracker-backed work. Direct coding does not require creating
an issue; the consuming workflow owns readiness and completion evidence.

## Configuration

**PRs as a request surface:** no.

**Close implemented items:** yes.

**Parent / child mode:** native-sub-issues.

**Dependency mode:** native-dependencies.

## Operations

Resolve the exact project and target type before acting. Prefer an available
GitHub connector; otherwise use the installed CLI or documented API. Check
current operation support and an independent read-back method before mutation.

Read the issue body, comments, labels, state, assignee, and relevant relationships.
Publish, comment, label, claim, or close only within the authorized task. The
configured closure policy applies when the consuming workflow has established
completion. It does not start work or authorize closure by itself.

## Representation

- Content lives in the issue body and comments.
- Category and state use [the label mapping](triage-labels.md).
- Parent and child links use the configured parent / child mode.
- Blocking links use the configured dependency mode.
- An active claim uses the assignee when the workflow requires claiming.

Do not switch relationship representations during one publication. Closing or
superseding a blocker must not expose a dependent as ready while it remains
blocked.

## Mutation read-back

Refetch the target and affected relationships after a mutation and verify the
fields that changed. After a failed or uncertain result, inspect actual state
before retrying to avoid duplicate issues, comments, or other effects. Report
any partial result and remaining gap.
