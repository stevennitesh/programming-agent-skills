# Astra audit-codebase rewrite

This records the source choices, implementation, and challenges for the Astra
audit package. It is evidence about this candidate, not runtime instructions or
proof that the skill improves agent judgment over baseline.

## Quality method

Preserve the custom audit's strongest controls: reachable scenarios, concrete
costs, accepted expectations for defects, sibling callers before systemic claims,
counterevidence, justified complexity, and explicit evidence gaps. Keep dynamic
reachability checks before deletion and meaningful regression responsibilities
before test consolidation.

Add focused discovery through actual change scenarios and explicit consideration
of both fragmented ownership and excessive concentration. Rank consequences and
relevance against disruption and verification cost. A new boundary can be a valid
direction; an existing destination is not an admission requirement. Audit finds
justified improvements, codebase-design resolves consequential alternatives, and
prototype gathers empirical evidence. Neither downstream skill is a prerequisite.

Six-class ledgers, exhaustive file ownership, exact terminology, mandatory HTML,
and user selection after every stage are removed from the common path. Broad
quality coverage remains available in a conditional reference. Mapping and HTML
are explicitly retained for the user's visual exploration and targeted selection.

## Upstream selection

Used the locally inspected snapshots from this conversation, without fetching:

| Source | Commit | Treatment |
| --- | --- | --- |
| Matt Pocock | `3cca18b368ae95cdbdebbff572ccafa662551015` | Keep change-hotspot discovery, caller friction, and deletion as a design question. Reject mandatory terminology, HTML, delegation, and grilling. |
| Pstack | `93b00b89ef425a9c1bac0d0b317dfc49c930ac99` | Use information leakage, repeated workarounds, and decomposition by execution stage as hypotheses. Reject universal shape prohibitions, size thresholds, and automatic restructuring. |
| Superpowers | `b36e0829c6d0140e93cfef2ca599b1b07d4a7797` | Its general review checklist adds little beyond local evidence controls. Do not import approval gates or diff-review scope. |
| Ponytail | `974d940a1c5344210874150b98ff0d2c861fab6a` | Preserve subtraction and reuse, already stronger locally. Reject ranking by cuts, single-implementation heuristics, and unsupported savings. |

## Atlas mechanism

The new standalone stdlib helper retains the legacy mechanism's useful design:
one offline HTML file containing canonical data, escaped presentation, validated
updates, writer exclusion, atomic replacement, and read-back. The old helper's
strict schemas encode the mandatory lifecycle being removed, so the Astra package
has its own smaller record model rather than importing a legacy runtime dependency.
Legacy source, reports, and tests remain supported and unchanged.

The helper owns inventory, directory expansion, overlap rejection, generated IDs,
prepared source fingerprints, report revision checks, history, priority sorting,
navigation, rendering, and freshness. Per-refresh caching reads shared source once;
the publication check uses a fresh snapshot. Agent input supplies the judgment.

Commands create a partial map, inspect a compact index or one selected record,
prepare one update, apply it, or refresh observations. Updates preserve omitted
records. Explicit removals preserve historical versions and cannot orphan children
or dependencies. IDs remain reserved after deletion. Reassignment is supported.

Mapping counts and audit coverage are distinct. Coverage is an explicit scoped
assessment, not something inferred from file counts. Changed source flags old
evidence; refresh never revalidates conclusions. Findings can include additional
decisive source outside their origin subsystem. The visual page exposes a dated
snapshot, collapsible subsystem details, dependency anchors, ranked findings, and
coverage rather than requiring agent-written HTML.

Limits: Git inventory is required; selectors are files or directory prefixes,
not globs. Nonignored untracked paths are visible and explicit untracked files
can be evidence. Semantic ownership, completeness, priority, and whether drift
invalidates a conclusion remain agent judgments. The helper is not an atomic
snapshot of a concurrently changing repository; rechecks narrow the race and
published freshness remains timestamped. Legacy schema migration and durable
archival installation are outside this change.

## Challenges and verification

Two fresh-context reviewers challenged a fixed candidate read-only. The quality
reviewer identified admission wording that overfit ownership refactors; it now
admits any demonstrated cost with a plausible removal mechanism. The mechanism
reviewer independently reproduced a canonical-rendering defect also found by root
tests, and found source drift during publication, removed-source cleanup,
reassignment, and ID reuse defects. All were fixed and covered by regression tests.
Both reviewers rechecked the corrected candidate and passed their assigned scopes.

The targeted suite exercises actual CLI-to-HTML round-trips, stale report/source
rejection, new selected files, unrelated source changes, history preservation,
ownership overlap, writer exclusion, escaping/tampering, explicit removal,
reassignment, removed source, coverage, and defect admission. Legacy helper checks
run alongside the new tests. A partial atlas of this repository's existing audit
package was generated under `.tmp/audit-codebase/astra-preview/report.html` as a
reviewable example; it does not claim whole-repository coverage.
