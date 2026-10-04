# Issue tracker: GitHub

Issues and specifications live in GitHub Issues for this repository's configured
project. Use this guide for tracker-backed work.

## Configuration defaults for setup

Adapt these starting values to the repository's chosen policy and supported tools.
Record the exact project and selected settings in the adopted guide; existing
repository choices take precedence. Keep the representation below consistent
with those settings.

**PRs as a request surface:** no.

**Close implemented items:** yes.

**Parent / child mode:** native-sub-issues.

**Dependency mode:** native-dependencies.

## Operations

Resolve the exact project and target type before acting. Choose an available
connector, CLI, or documented API that supports the configured operation and
read-back, subject to the environment's tool rules.

Read the issue content, state, and relationships needed for the intended decision.
Publish, comment, label, claim, or close only within the authorized task. The
configured closure policy applies when the consuming workflow has established
completion. It does not start work or authorize closure by itself.

## Representation

- Content lives in issue bodies and comments.
- Category and state use [the label mapping](triage-labels.md).
- Parent, child, and blocking links use the selected representation; these
  defaults use native relationships.
- An active claim uses the assignee when the workflow requires claiming.

An assignee identifies an account; the executing workflow establishes any
required run or actor ownership before dispatch.

Preserve the relationship representation during an operation. A closed blocker
does not establish readiness if other dependencies remain unresolved.

## Mutation read-back

Refetch the target and affected relationships after a mutation and verify the
fields that changed. After an uncertain result, inspect actual state before
retrying to avoid duplicate issues, comments, or other effects. Report any
partial result and remaining gap.
