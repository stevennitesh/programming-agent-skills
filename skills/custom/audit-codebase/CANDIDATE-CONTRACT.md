# Improvement Candidate Contract

An improvement candidate is one user-selectable improvement boundary inside
one audited subsystem. It contains at least one verified defect or admitted
opportunity. Group items only when every member shares one change direction and
Proof Seam plus either one causal owner or one unresolved decision. Gap-only
hypotheses and retained complexity are not candidates.

## Present

Keep every member visible:

```text
Candidate ID:
Subsystem:
Title:
Primary class: reliability | domain | design | simplification | coding practice | performance | declared:<lens-id> | mixed
Member defect, opportunity, and gap IDs:
Files and Modules:
Supported behavior:
Problem:
Current evidence:
Improvement direction:
Expected benefit:
Behavior and safety floors:
Required proof:
Decision questions:
Recommendation strength: Strong | Worth exploring | Speculative
Strength reason:
State: presented
```

The helper derives the linked Analyze pickup from the candidate ID, report, and
resolved skill paths. Apply [CANDIDATE-FOLLOWUP.md](CANDIDATE-FOLLOWUP.md) for
its conditional To Tickets authority and Return.

- **Strong:** direct evidence, concrete cost or impact, a plausible bounded
  alternative, and a meaningful Proof Seam.
- **Worth exploring:** real friction is evidenced, but a material choice,
  experiment, compatibility fact, or Interface question remains.
- **Speculative:** at least one member is admitted, but one exact gap weakens
  the direction, expected benefit, or proof plan.

Rank only candidates inside their audited subsystem. Never rank or select
subsystems.

## Revalidate

The card is a lead, not current proof. Analyze rereads current implicated
source, callers, contracts, decisions, tests, members, and Proof Seams and
records:

```text
Current-source validity: confirmed | changed | disproved | blocked
Last verified identity:
Current Source Trace:
Changed evidence or members:
Validity reason:
```

- **Confirmed:** the recorded problem and direction still hold.
- **Changed:** revise the evidence, members, or direction and continue only
  while at least one currently admitted defect or opportunity remains and all
  members still share one coherent improvement and Proof Seam. Otherwise
  disprove the old candidate and present any genuinely new boundary separately.
- **Disproved:** show the current evidence that removes the problem or cost,
  mark `disproved`, and stop.
- **Blocked:** name the unobtainable evidence or material user decision and
  exact re-entry.

Unrelated repository drift is irrelevant. A changed causal owner expands the
Source Trace; it does not force a whole-repository remap.

Validity describes whether the recorded problem and direction were supported;
later implementation does not rewrite that judgment.

## Analyze

Every confirmed or coherently changed candidate records:

```text
Current shape and demonstrated cost:
Keep:
Smallest sufficient change:
Structural change:
Replacement:
Recommended direction:
Rejected alternatives and why:
Affected contracts and decisions:
Material Responsibilities, Interfaces, Seams, and Proof Seams:
Compatibility, migration, cutover, and rollback:
Proof plan:
Residual risk:
Decision status: none | pending | settled | evidence gap | blocked
State: analyzed | decision pending | blocked
```

Do not force an alternative to exist, but `not applicable` needs evidence.

- **Keep** describes the present shape and continuing cost.
- **Smallest sufficient change** is the first valid reduction or correction
  that preserves supported behavior and safety.
- **Structural change** deepens, merges, inlines, moves a Seam, or introduces
  an earned Adapter only when Depth, information hiding, or testability
  improves and relevant complexity symptoms fall.
- **Replacement** is valid only when incremental evolution is worse and parity,
  migration, cutover, rollback, and proof are explicit.

Name observable success and proof. Bound change-created fallout and leave
unrelated cleanup separate.

For a design or mixed candidate, settle current-user decisions first. Then load
`$codebase-design` for the one bounded architecture question and fold its
recommendation, ownership, data and interface shape, applicable migration,
proof, or exact gap into these fields. Audit retains the HTML; no second design
artifact or later Codebase Design step exists.

## Conditional Follow-up

When `SKILL.md` admits its conditional follow-up branch, apply
[CANDIDATE-FOLLOWUP.md](CANDIDATE-FOLLOWUP.md). Otherwise record
`Next user selection: none`.

## Close Implemented

Close is a separately user-selected `$audit-codebase` objective for exactly one
analyzed candidate. Select the route returned by `inspect --objective close`
and use `schema --objective close --completion-route <route>`. Add
`--tracker-provider local-markdown` for a Local Markdown `tracker-frontier`.
Add `--reviewed` only when condition-triggered Change Review ran. Record its
raw decision and provenance. Audit Close owns this admission table:

- `pass` is admissible;
- `pass with residual risk` is admissible only with separate, explicit caller
  acceptance in `formal_review_residual_risk_acceptance`;
- `blocked` is inadmissible; and
- `incomplete` is inadmissible.

Existing state-version-2 reports that persisted the former synthetic
`accepted` value remain readable as legacy state. New Close manifests cannot
supply or persist it.

- **`tracker-frontier`:** only for `ready-graph|reused`; require the candidate
  digest, tracker mutation/read-back identity, and provider-native Ready tracker
  item identity. Hosted providers require exact HTTPS URLs; Local Markdown
  requires contained parent/item refs and committed completion read-back.
- **`local-markdown-recovery`:** only for an existing version-10/state-schema-2
  `recovery` record whose recorded failure is exactly the former HTTPS-only
  Ready identity mismatch. Require one uniquely matching candidate-bound local
  graph, its original recorded frontier facts, and exact committed closeout.
  Successful Close normalizes the tracker to `ready-graph`. Fresh Analyze must
  record Local Markdown directly and never select this route.
- **`authorized-direct-recovery`:** only for an already-landed,
  `authority-required|not-applicable` candidate whose direct implementation
  was explicitly authorized. Require the exact authority evidence and forbid
  tracker identities. This route repairs the atlas only; never create,
  reconstruct, or imply a retrospective ticket.

Before constructing any packet, the root verifies that the accepted proof and,
when review ran, the admissible raw review decision, provenance, and any
caller residual-risk acceptance bind to the supplied commit/tree; the
commit is current or reachable; Change Closure is complete; no implementation blocker remains;
the report/run/subsystem/candidate, candidate digest, and last Analyze identity
match, and every active candidate finding has one state-and-reason transition.
For direct recovery, the root also verifies the supplied implementation
authority granted that exact direct change before it landed.

The helper enforces the exact packet schema and Git commit/tree relationship;
it does not independently prove the supplied authority, proof, or conditional
review claims. A mismatched, partial, blocked, or failing Return changes no candidate
state.
Successful implementation is distinct from `disproved`.
Each transition changes only current state and reason; original evidence
remains in history, and `active` records residual work without misstating
resolution. The helper verifies Git reachability and derives candidate state,
implementation evidence, history, progress, colors, and finding transitions.
An implemented candidate has no pickup.

## Bound

Candidate analysis confirms, revises, disproves, or frames an improvement and
follows its generated implementation-work prompt when ready. It does not
implement, approve a public contract, mutate domain records, or invoke another
suggested owner.
