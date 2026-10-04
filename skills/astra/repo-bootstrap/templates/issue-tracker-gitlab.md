# Issue tracker: GitLab

Issues and specifications live in GitLab Issues for this repository's configured
project. Use this guide for tracker-backed work.

## Configuration defaults for setup

Adapt these starting values to the repository's chosen policy and supported tools.
Record the exact project and selected settings in the adopted guide; existing
repository choices take precedence. Keep the representation below consistent
with those settings.

**MRs as a request surface:** no.

**Close implemented items:** no.

**Parent / child mode:** body-links.

**Dependency mode:** body-links.

## Operations

Resolve the exact project and whether the target is an issue or merge request.
Choose an available connector, CLI, or documented API that supports the configured
operation and read-back, subject to the environment's tool rules.

Read the issue content, state, and relationships needed for the intended decision.
Publish, comment, label, claim, or close only within the authorized task. Apply
the selected closure policy once the consuming workflow establishes completion;
the default here leaves implemented issues open. Configuration does not itself
authorize closure.

## Representation

- Content lives in issue descriptions and notes.
- Category and state use [the label mapping](triage-labels.md).
- With these defaults, parent and child links live in the body and point to each
  other, and a `Blocked by:` section records dependency links. Adapt this to the
  selected representation during setup.
- An active claim uses the assignee when the workflow requires claiming.

An assignee identifies an account; the executing workflow establishes any
required run or actor ownership before dispatch.

Preserve the relationship representation during an operation. A closed blocker
does not establish readiness if other dependencies remain unresolved.

## Mutation read-back

Refetch the target and affected relationships after a mutation and verify the
fields that changed. After an uncertain result, inspect actual state before
retrying to avoid duplicate issues, notes, or other effects. Report any partial
result and remaining gap.
