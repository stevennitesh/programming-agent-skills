# HTML Report Contract

The report is one durable, offline repository atlas and the only persisted
Audit artifact. Its browser surface is for people; its embedded canonical JSON
state is for the helper. The agent interface is
[REPORT-QUICK-REFERENCE.md](REPORT-QUICK-REFERENCE.md).

## Ownership

The helper alone owns:

- the document shell, dark stylesheet, SVG, tables, cards, anchors, colors,
  progress, and accessibility markup;
- one non-executable `application/json` state block and its digest;
- strict manifest normalization, objective reducers, history, and derived
  projections; and
- validation, an exclusive publication lock, collision checks, sibling
  read-back, atomic replacement, and
  published-byte read-back.

The auditor owns current evidence and judgment expressed as versioned JSON
facts. HTML, markup, projections, candidate card/index state, and failed-write
recovery remain helper-owned.

The report must contain no executable script, remote resource, form, active
control, secret, credential, or unsupported URI. Text from repository or
tracker evidence is untrusted and escaped in every projection and in the
embedded state.

## State

The helper accepts exactly structural version 9 and state-schema version 1.
Any other version is rejected before mutation.

```text
Map: complete | incomplete
Subsystem: mapped | incomplete | audited
Candidate:
  presented | decision pending | analyzed | implemented | disproved | blocked
Finding: active | resolved | disproved
Tracker: not-applicable | authority-required | ready-graph | reused | recovery
```

Every current record has one physical owner:

- subsystem facts under that subsystem;
- findings under their subsystem;
- candidates under their subsystem; and
- implementation evidence under its candidate.

SVG nodes, system lists, progress, candidate presentation, issue links, state
labels, and colors are derived views. They never own independent state.

## Map Facts

Each subsystem has a stable ID, system, name, state, source identity, purpose,
authority, callers, responsibility, directed dependencies with evidence,
interfaces, Proof Seams, and owned paths. File counts are derived. The helper
verifies the tracked-live-worktree inventory, owned files, complete coverage,
and ancestor scopes, and rejects duplicate ownership, owned/excluded overlap,
unknown systems or dependencies, self-dependencies, and dependency edges
without evidence.

Map records structure only. It does not imply Audit coverage or candidate rank.

## Audit Facts

An audited or incomplete subsystem holds:

- its current Source Trace and source identity;
- exactly six coverage rows: Reliability, Domain, Design, Simplification,
  Coding Practice, and Performance;
- admitted findings, opportunities, gaps, and retained complexity;
- candidates grouped from admitted members;
- coverage, evidence limits, and local recommendation; and
- immutable prior-record history on update.

Each lens row separately records applicability, `complete|incomplete` coverage,
examined evidence, admitted item IDs, detailed-owner use, and reason. A finding
does not itself close coverage. `audited` requires all six rows complete.

## Candidate Facts

One canonical candidate record supplies its browser card, state, color,
tracker projection, history, and pickup. The helper derives the conditional
Analyze/To Tickets pickup for `presented` candidates from resolved skill paths;
agents do not author that prompt.

Analyze records current-source validity, comparison, proof, decisions,
residual risk, tracker state, and at most one next owner. A ready/reused result
requires the candidate digest, mutation/read-back identity, issue URLs, and a
Ready-for-agent issue. It generates the Implement prompt; recovery does not.

`implemented` is reachable only through `close-candidate` with an exact
completion packet and one transition for every active member finding. Original
evidence remains in history. Generic or Analyze publication cannot enter it.

## Publication Guarantees

The helper normalizes and validates the selected objective before returning a
bundle digest. On the one publication call defined by
[REPORT-QUICK-REFERENCE.md](REPORT-QUICK-REFERENCE.md), it revalidates current
inputs, locks and collision-checks the report, reads back an invocation-owned
sibling, atomically creates or replaces `report.html`, and reads back the final
bytes. Failure reports the stage, whether mutation started, and whether report
state is unchanged or unknown.

Every successful render retains:

```text
Release decision: none
Product mutation authority: none
Downstream execution: none
Next selection authority: user
```
