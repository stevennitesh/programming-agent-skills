# Issue tracker: GitLab

Issues and specifications live in GitLab Issues for this repository's configured
project. Use this guide for tracker-backed work.

## Configuration

**MRs as a request surface:** no.

**Close implemented items:** no.

**Parent / child mode:** body-links.

**Dependency mode:** body-links.

## Operations

Resolve the exact project and whether the target is an issue or merge request.
Use an available connector, installed CLI, or documented API. Check current
operation support and a read-back method before mutation.

Read the description, notes, labels, state, assignee, and relevant relationships.
Publish, comment, label, or claim only within the authorized task. Leave
implemented issues open under this configuration unless the user directs closure.

## Representation

- Content lives in issue descriptions and notes.
- Category and state use [the label mapping](triage-labels.md).
- Parent and child links live in the body and point to each other.
- A `Blocked by:` section records dependency links.
- An active claim uses the assignee when the workflow requires claiming.

Preserve the relationship representation during an operation. A closed blocker
does not establish readiness if other dependencies remain unresolved.

## Mutation read-back

Refetch the target and affected relationships after a mutation and verify the
fields that changed. After an uncertain result, inspect actual state before
retrying to avoid duplicate issues, notes, or other effects. Report any partial
result and remaining gap.
