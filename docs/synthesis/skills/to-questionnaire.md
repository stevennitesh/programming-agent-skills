# To Questionnaire Synthesis

## Status And Decision

Status: canonical-and-installed synthesis for the fresh `to-questionnaire`
campaign that began at Git
`4359f7afeeec29a9c8692b18c1586afb041f9bf4`.

Decision: Prompt 5 complete after exact final C1 promotion,
`pruning-not-needed`, and managed installation parity.

Campaign shape: `behavioral-candidate`.

Runtime decision:

```text
historical control B0 != current canonical
current canonical = final C1
final C1 = B0 + C1-TRANSACTION + C1-DIRECT-RETURN
C1-LEDGER = rejected-no-control-failure
```

`B0` was the exact pre-promotion canonical package and is frozen for this epoch at
`docs/validation/evals/to-questionnaire-b0`, package SHA-256
`163d76f3468f2301c6cddeead5cca34b08afaf9ae370f457157707c12e010158`.
It is now a historical exact control, not active runtime.
Final `C1` is promoted at `skills/custom/to-questionnaire`, package SHA-256
`a5c63f7c0ecbe2971dbbd20bb1774ece83990e08fa97d3df6d9f49c3b41cf3c4`.
Its `SKILL.md` SHA-256 is
`B8F96C9788A4BCDEE5C6E5256F631233E9A7BF96E0420673798E607F918B84D2`;
its metadata remains byte-identical to B0. Prompt 4 rejected the ledger unit
without a control failure and accepted the transaction and Direct Return
units on exact B0-first evidence.
The supported installer synchronized the same two-file package to
`C:\Users\steve\.agents\skills\to-questionnaire` at the same package and file
identities.

This document records the active design and proof trace. Current behavior is
owned by
`skills/custom/to-questionnaire/SKILL.md` and
`skills/custom/to-questionnaire/agents/openai.yaml`.

## Outcome And Viability Floor

To Questionnaire is an explicit-only leaf that creates one local,
recipient-ready Markdown questionnaire for one identifiable external
stakeholder who holds material facts or decisions unavailable to the current
user and authorized inspectable sources. The artifact gathers what one
downstream decision needs and may be completed asynchronously or used in a
later meeting.

The leaf owns sender-known intake, question design, one artifact, verification,
and Return. The user owns recipient selection, output authority, delivery, and
the downstream decision. The recipient owns their answers.

The leaf is viable only while all of these boundaries hold:

- explicit user invocation selects it;
- `$skill-router` and `$grilling` may recommend it and stop, but do not invoke
  or continue it;
- `$research` owns source-answerable gaps, and `$grilling` owns decisions the
  current user can make;
- one artifact serves one recipient and one downstream decision;
- the skill does not conduct a survey, deliver or send the artifact, handle
  answers, interpret answers, synthesize the downstream decision, or continue
  another workflow;
- a missing recipient, output authority, or other required fact produces an
  exact no-write gap Return rather than an invented answer or authority;
- recipient and outcome lock precedes a coverage-ready draft; safe write
  precedes reread; reread precedes Return; and
- the leaf does not contact anyone, escape the authorized path, overwrite
  without authority, leak sensitive context, or create extra attributable
  content.

Implicit invocation, delegated callers, Wayfinder schemas, Wayfinder
durability and lifetime rules, and caller continuation are outside this
campaign. They are not deferred C1 behavior.

## Source-First Checkpoint

The Prompt 1 checkpoint is intact.

```text
Checkpoint: to-questionnaire source-first B0
SHA-256: DF7D8DBA368064E4EAF4034E5BF787CDBE21D62D1B37C59EBBA5AFD1ED43B02C
Campaign HEAD: 4359f7afeeec29a9c8692b18c1586afb041f9bf4
B0 units: B0-INV, B0-SEND, B0-DRAFT, B0-COVER, B0-OUTPUT, B0-GAP
Decision: minimum viable; behavioral C1 admitted; no interlude
```

### Source Identities And Claim Limits

| Source | Exact identity | Claim admitted | Limit |
| --- | --- | --- | --- |
| Local `CONTEXT.md` | SHA-256 `EA6CB7894E806EAFD030F8A7FE5E4DF5ABAAC0D35A0F861CCED47369DCE77D90` | Local pack language and ownership | Local intent, not steering efficacy |
| Local Grilling runtime | SHA-256 `AD261344B28F6E47F7281C20AFA742994A7351FB11DF43036AE8B1EC49C323DD` | Current-user decision boundary and recommend-and-stop relationship | Does not own the artifact |
| Local Skill Router runtime | SHA-256 `2BBF8E9C2B9C0C86D8AA3ABFF2A66BDFB946A9A120DBFF3D5D640966398D7C05` | Explicit route selection and stop | Does not invoke or execute the leaf |
| Matt Pocock upstream | Git `ed37663cc5fbef691ddfecd080dff42f7e7e350d`, clean; `SKILL.md` SHA-256 `65D8F34C1E8089119EC07D1B22E5EDE592EBACADBF4D2E76DE7007AF2450414D`; metadata SHA-256 `0B5ED84D805809777A15371C946A70F98321E3C6400FCE5FCD74DF71D40E860B`; README SHA-256 `F55C5E8A5650F2927409F7E5C6B3B2DB804182778D7885D926B2F8A043B3F0AB`; question-limits SHA-256 `4079B906B148C0C4EED7DFF807348AD62B2C0C83CED017DC674973007E04A55D` | User-invoked questionnaire, grill the send rather than the subject, compact document, later-meeting use, named-item coverage | Upstream meaning, not local authority or professional efficacy |
| Superpowers upstream | Git `d884ae04edebef577e82ff7c4e143debd0bbec99`, clean; brainstorming exclusion analogue `SKILL.md` SHA-256 `E14914605F640E0841758E45D0AB2A53243B59B921F929E47921C99668F2E61D`; visual reference SHA-256 `3321A044C777D03D7177DF41C77BB83155FF2A6D0C16B8A3D752426D29F14EA8` | No equivalent questionnaire skill; analogue supports keeping a leaf out of an owner that must stop | Absence and boundary analogue only |
| Ponytail upstream | Git `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`, clean | Verified absence of an equivalent skill | Absence only |
| Upper-bound engineering language | SHA-256 `DAB0407C917FFA7F17F1F4E41C7B2B1B69978C76887CD69F9C75E16574657572` | Counterpressure toward explicit bounds and proof | General research, not questionnaire efficacy |
| Matt vocabulary note | SHA-256 `AD812A4BEE0F478C3DBACB0F17B8B27DC45FC8176F24A7C768FACF98B49A5B65` | Source vocabulary and provenance | Research summary, not runtime authority |

Freshness was checked only against the local upstream clones at the identities
above. The sources support meaning, mechanics, and vocabulary. They do not
establish professional questionnaire efficacy. Source steering requires the
specified D0/B0 comparisons.

## Semantic-Unit Ledger

Every B0 unit has one intended-contract obligation, one basis, one owner, one
destination, and one proof obligation. `Required compatibility` denotes local
behavior needed for a viable pack leaf rather than a source-derived steering
claim.

| Unit | Intended-contract obligation | Source mechanic or compatibility | Owner | Current and research disposition | Protected and C1 disposition | Destination and proof |
| --- | --- | --- | --- | --- | --- | --- |
| `B0-INV` | Reach the leaf only by explicit user choice; preserve the difference between the questionnaire's recipient/subject and the person supplying send metadata | Matt's user-invoked identity plus local explicit-only compatibility | User selects; leaf admits | Current `allow_implicit_invocation: false` is `keep`; Matt is `adapt`; no Prototype | Explicit-only is protected; no C1 delta | Metadata plus Admit clauses; deterministic policy check and explicit route cases |
| `B0-SEND` | Ask only for missing sender-known information needed to address and constrain the artifact; do not grill the user for recipient-owned answers | Matt's "grill the send, not the subject" | Leaf owns intake; user supplies sender-known facts | Current is `keep`; source mechanic is `adopt`; no Prototype | Compact intake and no invented answer are protected; no C1 delta | Lock/intake clauses; D0/B0 send-versus-subject arm |
| `B0-DRAFT` | Produce a compact recipient-ready document with purpose, sender/recipient, answer use, bounded context, instructions, themed value-ordered atomic neutral questions, answer stubs, selective "why," and an optional catch-all | Matt document structure and later-meeting use, adapted by local safety and question-limit counterpressure | Leaf | Current is `keep`; source structure is `adapt`; no Prototype | Recipient readiness, later-meeting use, and one-recipient scope are protected; C1 adds no content section | Draft clauses; D0/B0 priority-and-atomicity arm plus B0 viability rubric |
| `B0-COVER` | Map every user-named needed-back item to a substantive question; remove duplicates, compounds, leading, speculative, source-answerable, and out-of-scope questions; never count catch-all as coverage | Matt's named-item completion criterion plus required local ownership compatibility | Leaf | Current is `keep`; coverage mechanic is `adapt`; no Prototype | Complete named-item coverage is protected; `C1-LEDGER` was rejected because B0 already prevented every registered failure | Cover clauses; B0 mapping and quality controls |
| `B0-OUTPUT` | Write exactly one Markdown file and Return its absolute path while preserving compatible `.tmp` fallback and Repo Bootstrap setup ownership | Matt's one-file/path Return plus required local safe-write compatibility | User authorizes output; leaf writes and verifies; Repo Bootstrap owns missing local setup | Current is `keep`; upstream current-directory default is `reject`; no Prototype | One artifact, no delivery, `.tmp` fallback, and Repo Bootstrap boundary are protected; `C1-TRANSACTION` sharpens the transaction | Save/Verify/Return clauses; B0 one-file check and C1 transaction matrix |
| `B0-GAP` | On missing required intake, authority, or viable route, name the exact gap and write nothing; never invent an answer or authority | Required safety and authority compatibility | Leaf reports; user retains the missing choice | Current stop branches are `keep`; no independent source or Prototype claim | No-write safe failure is protected; `C1-DIRECT-RETURN` makes its truth visible and typed | Admit/Return clauses; negative B0 viability cases and C1 Return truth arm |

No Prototype was run or admitted. Research settled source meaning only. The
Prompt 1 grill settled the local intended contract; it is not efficacy proof.

## Historical Executable B0

`B0` is the exact pre-promotion control package:

| Surface | Exact identity |
| --- | --- |
| `docs/validation/evals/to-questionnaire-b0/SKILL.md` | SHA-256 `0310B4EDBED253A641C3DCD44320E8703A73234DBECC7B7F87290492ACE479FB` |
| `docs/validation/evals/to-questionnaire-b0/agents/openai.yaml` | SHA-256 `DC1585512A0C63A93D69421C2AFAE62EBC94B0EAB91A792A41D2859219CE0B9A` |
| Historical control package identity | `163d76f3468f2301c6cddeead5cca34b08afaf9ae370f457157707c12e010158` |

Its executable order is:

```text
explicit invocation
-> Admit one external owner
-> Lock recipient, decision, needed-back scope, sender-known send facts,
   effort, and output
-> Draft and Cover a compact recipient-ready questionnaire
-> safely write one Markdown artifact
-> reread and verify
-> Return the absolute path and unresolved assumptions
-> stop
```

This order is irreversible at the write boundary: the recipient and outcome
must be locked and the candidate coverage-ready before the first Save. A
failed gate returns the exact gap without writing or inventing an answer.

## Active C1 Delta

Active canonical `C1` is B0 plus the two accepted hypotheses below. The ledger
hypothesis remains only as concise decision-changing history.

| Hypothesis | Origin and owner | Expected B0 failure | Cheapest expression | Wrong-condition case | Proof | Destination and decision |
| --- | --- | --- | --- | --- | --- | --- |
| `C1-LEDGER` | `current-retention` inspected as a beyond-minimum mechanism; leaf owns traceability | A fluent draft can omit a needed-back item, add an orphan question, rely on catch-all, or exceed the effort budget without making the mismatch visible before Save | Give needed-back items stable IDs; require forward and inverse mapping plus semantic and effort checks before the first Save | Do not expose internal bookkeeping in the recipient artifact or require IDs to replace clear question text | Five exact B0 samples for missing item, orphan, catch-all substitution, and hard-budget conflict | `rejected-no-control-failure`; no C1 arm ran and the delta was removed |
| `C1-TRANSACTION` | `current-retention` and `intent-counterexample`; user owns authority, leaf owns verification | B0 may accept traversal, wrong extension, collision, unauthorized overwrite, sensitive placement, stale/dirty/concurrent target state, or a first Save before the complete render is ready | Before first Save, classify sensitivity; resolve and prove the absolute `.md` target is contained; prove exact overwrite authority and refreshed target/worktree state; render and read the whole candidate; after Save prove attributable mutation only | Do not create Wayfinder durability, lifetime, schemas, a helper, a manifest, or broad worktree ownership | B0 exhibited wrong-extension and first-write failures; exact rederived C1 passed the nine-case matrix in 5/5 registered samples | `SKILL.md` Save/Verify boundary; `accepted` |
| `C1-DIRECT-RETURN` | `current-retention`; leaf owns Return truth | B0's narrative Return can obscure whether no artifact was admitted, construction is incomplete, or a verified questionnaire is ready, and can omit visible Direct defaults | Make Direct defaults visible and Return one typed status: `Questionnaire ready`, `Not admitted`, or `Incomplete`, with exact artifact state and `Delivery: not performed` | Do not add a delegated caller adapter, Wayfinder result schema, or downstream continuation | B0 failed the typed schema in 5/5 samples; exact C1 passed success, wrong-owner, missing-authority, and partial-write cases in 5/5 | `SKILL.md` Direct Return/Completion; `accepted` |

The original hypotheses were admitted because they had plausible B0
counterexamples, not because current contained them. Prompt 4 supplied the
deciding contribution evidence and removed the unproved ledger expression.

## Rejected And Deferred Alternatives

Rejected from B0 and C1:

- implicit invocation;
- delivery, email, form, survey, response-store, reminder, scheduling, or
  provider integration;
- response ingestion, answer interpretation, truth scoring, synthesis, or
  downstream execution;
- multi-recipient or respondent-pool questionnaires;
- mandatory catch-all coverage;
- supporting references, schemas, scripts, or helpers; and
- any existing experimental candidate as this epoch's C1.

Deferred solely to a future Wayfinder-owned decision:

- Wayfinder invocation, packet and result schemas;
- durable artifact lifetime and retention fields;
- external-wait state;
- caller answer reconciliation and continuation; and
- `.scratch` durability required by such a caller.

These deferred items are not residual gaps for this Direct-only campaign.

## Relationships And Affected Surfaces

| Source | Relationship | Target | Observable trigger and Return owner |
| --- | --- | --- | --- |
| User | Explicitly invoke | `$to-questionnaire` | The user requests one local questionnaire for one identifiable external owner and retains the returned path, delivery, and downstream decision |
| `$skill-router` | Recommend and stop | `$to-questionnaire` | Route selection identifies this explicit leaf; the user decides whether to start it |
| `$grilling` | Recommend and stop | `$to-questionnaire` | Grilling reaches a question owned by one external stakeholder; the user decides whether to start the leaf |
| `$to-questionnaire` | Recommend and stop | `$research` | Authorized inspectable sources own the whole material gap |
| `$to-questionnaire` | Recommend and stop | `$grilling` | The current user owns the material decision |

Research owns source-answerable investigation; Grilling owns the current
user's decision conversation. Neither transfers its procedure to this leaf.
The recipient owns answers. The user owns delivery and subsequent use.

These are the complete active To Questionnaire edges. Wayfinder, delegated
callers, Grill-with-Docs routing, and a Research-to-Questionnaire edge remain
excluded; their owners were not changed.

## Proof Matrix

| Lane | Exact claim | Control and candidate | Required evidence | Current state |
| --- | --- | --- | --- | --- |
| B0 viability | Each `B0-*` unit satisfies the viability floor as the executable minimum | Exact Prompt 3 B0 against fixed positive and negative tasks | Artifact and filesystem read-back, rubric, exact Return, no-write failures | `passed`; complete ten-case suite 5/5 |
| Conditional D0 steering | "Grill the send, not the subject" changes intake; priority/atomic drafting changes question selection and wording | D0 omits only the tested steering while invocation, authority, task, tools, and context match B0 | D0 must exhibit the claimed failure before B0 receives efficacy credit | `passed`; send 0/5 to 5/5, priority/atomic 0/5 to 4/5 |
| C1 contribution | Each surviving C1 hypothesis prevents its named B0 failure without weakening B0 | Exact B0 versus exact rederived C1 | Ledger B0 control; transaction matrix; Direct Return truth cases | Ledger rejected; transaction and Direct Return accepted |
| Invocation | Explicit reach works and implicit discovery remains disabled; recommendation edges stop | Exact metadata and fixed explicit/recommendation tasks | Deterministic policy check plus behavior cases; no implicit-invocation claim | `passed` for explicit and recommendation cases; implicit behavior excluded |
| Protected contracts | One recipient, compact sender-known intake, later-meeting use, one artifact, no delivery/answer handling/synthesis, safe ownership, `.tmp` fallback, and Repo Bootstrap ownership survive | Exact B0 and C1 | Relationship traces, negative cases, artifact and mutation inspection | `passed`; no critical regression in any executed C1 arm |
| Pruning | Every accepted C1 clause changes protected or proved behavior | Behavior-complete Prompt 4 C1 versus pruned candidates | Complete cut audit; equivalence only if a material cut changes bytes | `passed`; all 20 runtime-facing passages kept, no material cut, final C1 byte-identical |
| Deterministic | Canonical bytes, policy, links, structure, and package contracts agree | Exact promoted package | Hashes, read-back, focused checks, validation, both diff checks | `passed`; focused 59/59, affected contract files 68/68, sequential full suite 203 passed/4 skipped, validation and install parity passed |

D0 is not required for independently owned authority, safety, output, or
Return contracts. A D0 failure cannot establish those contracts.

## Prior Evidence Dispositions

| Evidence | Exact identity | Disposition for this campaign |
| --- | --- | --- |
| Pre-promotion canonical B0 | Skill and metadata hashes plus package identity recorded above | `exact-reusable` for byte identity; current-epoch behavioral viability passed before promotion |
| 2026-07-21 Control Lock | SHA-256 `114706FE8042C6A307844EC40793F2B26D6C646F961C2CDC034C1F831DB28337` | `lane-limited` for exact canonical preservation; its K2/K3/K5-K12 observations are `historical-admission-only` |
| 2026-07-21 post-candidate evaluation | SHA-256 `3352BB19A2CF1FD9432E799AA33C38EB5B11CE6ACD09A42E5EEC39A1FD0F04F3` | `historical-admission-only`; it tested a different, implicit, delegated candidate |
| 2026-07-21 pruning evaluation | SHA-256 `9EBBC442810552E9FC021FCF7FB81B4DDDB6F90296547F10FF4B4DAC28F95A28` | `historical-admission-only`; its control and final bytes are not this epoch's C1 |
| Historical retained candidate | Package tree `7d36b43411bfc6146d9390465b845ff251893d309cdae09690db921b56cc8376`; current experimental skill SHA-256 `781F10C05147CB501D532B4182A9B367A131CD053E56CE3C3BC0DE07BEDDDE34`; metadata SHA-256 `51E6B9B09D7E82F9A512B077779D3F9662F47348F8C7D7FD81E2F02FE9ECED5D` | `lane-limited` inventory and `historical-admission-only` mechanism evidence; explicitly not B0 or C1 |
| Prompt 1 experimental manifest and structural tests | Files inspected during Prompt 1 | `lane-limited` inventory; they prove neither this epoch's semantics nor contribution |
| D0/B0 steering evaluations | Current Prompt 4 raw corpus and behavior record | exact current-epoch evidence for the two registered steering lanes |
| Exact C1 construction and contribution evidence | Initial and behavior-complete package identities plus current Prompt 4 record | ledger rejected; transaction and Direct Return accepted for exact behavior-complete bytes |

Historical evidence preserved the reasons to inspect stable traceability,
transactional safety, and typed Return. It does not authorize carrying the old
implicit invocation, Wayfinder adapters, durability model, chronology, or
package bytes into C1.

## Promotion Lifecycle And Residual Gaps

Lifecycle:

```text
Prompt 1 source-first checkpoint: complete
Prompt 2 decision-complete synthesis: complete
Exact B0 candidate fixture for this epoch: constructed
Exact C1 candidate fixture for this epoch: constructed
Prompt 4 behavior-complete package: accepted
Pruned package: pruning-not-needed; byte-identical to behavior-complete C1
Canonical promotion: complete at exact final C1
Managed installation parity: complete at exact final C1
```

No promotion or installation lifecycle gap remains. Behavioral evidence limits
remain screening scope only: no professional efficacy claim, no live
link/junction or operating-system torn-write exercise, one of five B0
priority/atomic steering samples retained compound questions, and
`C1-LEDGER` remains rejected only for its tested cases.

Pruning result: the complete cut audit classified all 20 runtime-facing
passages `keep`. No material cut reduced always-loaded description,
common-path instructions, duplicated semantic ownership, branch load, or an
unused package surface. No pre-prune fixture or behavior wave was created.
Final C1 remains byte-identical at
`a5c63f7c0ecbe2971dbbd20bb1774ece83990e08fa97d3df6d9f49c3b41cf3c4`.
The canonical runtime and Direct-only relationship surface now publish that
exact decision. Promotion and installation evidence is recorded in
[`2026-07-23-to-questionnaire-promotion-install.md`](../../validation/transcripts/2026-07-23-to-questionnaire-promotion-install.md).
