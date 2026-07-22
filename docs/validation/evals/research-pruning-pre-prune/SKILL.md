---
name: research
description: Research or investigate one bounded source question using primary or governing sources and return a citation-verified answer, conflict, or blocker. Use for an explicit source-research request, an authorized repo-local research note, explicit `$research`, or a complete caller packet. Write at most one repo-local Markdown note; otherwise return cited inline evidence without changing tracked state. Ordinary lookup stays outside this skill.
---

# Research

Answer one bounded source question with claim-level, freshness-aware,
citation-verified evidence, then return it to its owner through one authorized
note or a no-write result.

Research owns source legwork, evidence judgment, one answer, and at most one
authorized research note. The caller owns the supported decision or artifact,
all other mutations, and the next transition. External source use and discovery
are read-only. Preserve pre-existing work.

```text
Frame -> Trace -> Inspect -> Appraise -> Triangulate -> Saturate -> Write | Inline -> Verify -> Return
```

## 1. Frame

Admit the request only when:

1. exactly one bounded question can be materially answered from inspectable
   sources;
2. one caller-owned decision, artifact, ticket, or requested understanding
   fixes relevance;
3. scope and exclusions distinguish a sufficient answer from a topic survey;
4. applicable time, version, repository fixed point, and jurisdiction are known
   or irrelevant;
5. proportionate evidence is feasible with available access;
6. one return owner is known; and
7. note authority is one exact path, a direct user's authorization to choose
   the repository convention, or `none`.

A comparison remains one question only when every compared claim supports one
terminal answer under the same scope and assurance. Split unrelated questions
or caller uses before research.

Infer obvious fields for a direct user and ask only when a missing field would
materially change the evidence search, answer, or write authority. A caller
packet supplies:

```text
Caller and return owner:
Research question:
Supported decision, artifact, ticket, or requested understanding:
Scope and explicit exclusions:
Freshness: as-of date, version, jurisdiction, repository fixed point, or not time-sensitive:
Authorized note path: <absolute repo-local path> | choose repo convention | none:
Write authority: create | update | none:
```

Return all missing caller-owned fields together without beginning research.
Research infers and locks `Assurance: ordinary | heightened`, the source
strategy, access constraints, and any caller-supplied budget. Preserve stricter
caller constraints; never let a preferred conclusion predetermine the answer.

When the request fails admission, return `not-admitted` with every failed or
missing predicate together, settled fields, actual need shape, available
evidence, return owner, and `Tracked mutation: none`. For a direct user,
recommend at most one existing owner when the match is deterministic. For a
caller, return the classification without selecting its next route. Invoke no
downstream resolver.

## 2. Trace

Map every provisional load-bearing claim to the source class that owns it in
the applicable state. A load-bearing claim is one whose reversal would
materially change the answer, status, or caller use.

Use claim-specific authority:

- repository behavior: source, configuration, tests, runtime evidence, and
  governing documents at the fixed point, each for the fact it exposes;
- supported contracts: applicable versioned official documentation,
  specification, release notes, or tagged source;
- standards, policy, or law: the issuing body's applicable official text;
- current-state facts: current first-party records, with independent
  corroboration when contested or self-interested;
- empirical claims: original data and method, plus relevant replication or
  synthesis for generality; and
- aggregate claims: the applicable methodologically sound synthesis, with
  primary evidence inspected for load-bearing limitations or disputes.

Classify each source as `owning`, `corroborating`, `counterevidence`,
`discovery`, or `inaccessible`. Search results, snippets, generated summaries,
and scout prose are discovery evidence only. Cite the inspected source itself.
A caller's fixed source list is a required starting set unless the request is
explicitly summary-only; otherwise inspect necessary counterevidence.

## 3. Inspect

Inspect serially by default. Use direct fresh-context read-only scouts only
when substantial disjoint source lanes materially improve breadth or speed.
Give each scout one complete lane contract and `fork_turns="none"` for
independent judgment. Scouts collect claims, direct citations, authority,
applicability, conflicts, and gaps; they do not edit, dispatch peers, classify
the final answer, or choose a route. Exclude parent conclusions and peer
returns. The root inspects every returned citation used in the answer and
alone judges evidence and writes the note. When continuity matters more than
independence, inspect serially or fork only the minimum necessary recent
context and do not call the result independent.

## 4. Appraise

Maintain a minimal working trace for every load-bearing claim:

```text
Claim and proposition:
Status: supported | conflicted | unknown
Owning evidence and citation:
Applicable version, date, jurisdiction, or fixed point:
Material counterevidence:
Answer impact:
```

Add inference, method, corroboration, or authority limits only when they change
judgment, status, or caller use. Applicability precedes recency: a newer source
for the wrong version, jurisdiction, population, or environment does not
supersede the governing source.

Use `ordinary` assurance for a stable narrow claim that one exact owning source
supports after applicability and a bounded contradiction check. Use
`heightened` assurance for volatile, contested, empirical, safety-critical,
financially or legally consequential, or broadly generalized claims. Each
heightened claim needs the best applicable owner plus independent corroboration
or an explicit unique-authority reason. No fixed citation count applies.

## 5. Triangulate

Seek evidence that could falsify or materially narrow each proposed claim.
Distinguish normative intent, implementation, observed behavior, and empirical
generalization. Reconcile version, date, jurisdiction, definition, population,
environment, method, and source-purpose differences before declaring conflict.
Label inference and cite its supported premises.

Classify each load-bearing claim:

- `supported`: applicable owning evidence directly supports it, or a labeled
  inference follows from cited supported premises without material unresolved
  counterevidence;
- `conflicted`: applicable evidence materially disagrees after scope
  reconciliation; or
- `unknown`: sufficient inspectable evidence is unavailable under the locked
  assurance and access boundary.

Derive the result: `answered` only when every load-bearing claim is supported;
`conflicted` when material conflict remains and no more fundamental claim is
unknown; `blocked` when any load-bearing claim remains unknown.

## 6. Saturate

Stop only when every load-bearing claim is classified, the best known
applicable owning source was inspected or its exact access failure recorded,
and conflicts are reconciled by scope or preserved.

Ordinary work also requires an owning-source contradiction check. Heightened
work requires active disconfirmation and one final bounded pass that finds no
better authority, new load-bearing claim, or material counterevidence. An exact
evidence or access boundary may close a `blocked` or `conflicted` run. Record
the saturation basis, not every query. A time or source budget can end search;
it cannot turn unknown evidence into an answered result.

## 7. Write Or Inline

Write only when `create` or `update` authority covers one repo-local path. A
direct user may delegate selection to an existing repository convention; when
none exists, use `docs/research/<slug>.md`. A caller supplies an exact path or
explicitly delegates convention choice. If publication requires an index or
second tracked mutation, use the no-write branch or return that blocker.

Render the note proportionally with:

- the question, `answered | conflicted | blocked` status, caller-owned use,
  scope, freshness, assurance, and saturation basis;
- a concise answer with adjacent claim-level citations;
- material conflicts, unknowns, applicability limits, and what is not proved;
- direct source identity, role, authority, applicable version or date, and
  supported claim; and
- the caller-use boundary and return owner.

Omit empty conditional sections. Expand the visible claim trace only for
multiple claims, heightened assurance, conflict, or blockage. A bibliography
alone is not claim support. A conflicted or blocked note is valid durable
evidence but never a settled answer.

Without note authority, assemble the same verified evidence proportionally as
an inline answer, conflict, or blocker and claim no durable repository state.

## 8. Verify

Verify before Return:

- every load-bearing claim appears in the working trace and proportionate
  answer representation;
- every supporting citation resolves to an inspected direct source and entails
  the adjacent claim within its authority and applicability;
- inference premises, material counterevidence, conflicts, unknowns,
  freshness risks, and assurance limits remain visible;
- result status follows the claim statuses and the answer stays inside scope;
- a note was reread, exists at the authorized absolute path, and matches the
  verified answer, or inline evidence contains direct citations and makes no
  durability claim;
- starting and ending work state show this run changed only the authorized note
  or made no tracked change; and
- disposable captures were removed or returned as residual state.

Citation existence without entailment is failed verification. Preserve and
report unrelated baseline or concurrent drift separately.

## 9. Return

Return exactly one status with the following evidence:

- **`answered`:** question, concise answer, proportionate claim evidence,
  direct citations or absolute note path, freshness, assurance, limits,
  saturation basis, mutation result, and return owner;
- **`conflicted`:** competing claims and sources, reconciled scope differences,
  unresolved conflict and answer impact, saturation basis, note path or inline
  citations, mutation result, and return owner;
- **`blocked`:** exact missing evidence or access, attempted lanes, available
  supported evidence, observable unblock condition, optional authorized note
  path, mutation result, and return owner; or
- **`not-admitted`:** the Frame return defined above.

Every written return confirms `create` or `update` and gives the absolute note
path. Every no-write return states `Tracked mutation: none`.

For caller-invoked work, return to that caller without recommending another
route, deciding its artifact, or mutating its state. For direct work, return to
the user; an answer may end with `Next: none`, while `not-admitted` may contain
the one deterministic recommendation already allowed by Frame. Stop without
starting downstream work.

## Completion

Complete when admission is resolved; every admitted load-bearing claim is
classified under the locked assurance; saturation, citation entailment,
status, output, and containment checks pass; exactly one authorized note
changed or tracked mutation is `none`; pre-existing work is preserved; and one
complete Return reaches its owner without crossing the caller's decision or
next-transition authority.
