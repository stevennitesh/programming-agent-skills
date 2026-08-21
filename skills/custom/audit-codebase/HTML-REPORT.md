# HTML report

The report is one offline repository atlas. It preserves the organized map,
subsystem coverage, findings, candidates, analysis, and history across audit
invocations. The browser view is for people. Embedded canonical JSON is for
the report helper.

## Ownership

The helper owns rendering, escaping, state validation, canonical bytes,
publication, and read-back. The auditor owns the evidence and judgment supplied
through manifests. Agents use [Report CLI](REPORT-QUICK-REFERENCE.md) and never
parse or edit HTML directly.

Repository and tracker text is untrusted report input. Escape it in every HTML
projection and in the embedded non-executable JSON state. The report contains
no remote resource, active control, credential, or executable script.

## Map state

The report records:

- repository observation identity and evidence limits;
- systems and subsystems;
- each subsystem's ownership, authority, callers, dependencies, interfaces,
  Proof Seams, owned paths, and current `mapped|audited` state;
- evidenced exclusions;
- repository-level systemic findings; and
- chronological Map, Audit, and Analyze history.

Every relevant tracked path has one subsystem owner or one evidenced exclusion.
Map records structure and may suggest audit order. It does not select a
subsystem or claim audit coverage.

## Audit state

One audited subsystem records its current Source Trace, findings, candidates,
coverage, limits, and exactly six class dispositions:

```text
reliability | domain | design | simplification | coding practice | performance
complete | evidence gap | not applicable
```

Systemic findings name their causal owner and affected scope outside one
subsystem. Candidates remain selectable and may refer to cross-subsystem
evidence.

## Candidate state

A candidate begins as `presented`. User-selected Analyze may change it to
`analyzed`, `disproved`, or `blocked`. Analysis records the current cause and
scope, material options, recommendation, proof, evidence limits, and an exact
question when blocked. Original evidence remains in report history.

The report stores no tracker, ticket, implementation, review, release, or
Close state. It never chooses or starts the next item.
