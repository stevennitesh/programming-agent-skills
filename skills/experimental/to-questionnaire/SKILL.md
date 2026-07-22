---
name: to-questionnaire
description: Create one unsent Markdown questionnaire for a single external stakeholder's source-unavailable knowledge gap, from a direct request or complete Wayfinder Questionnaire ticket.
---

# To Questionnaire

Create one recipient-ready Markdown questionnaire, verify its exact artifact state, return the needed-back ledger, and stop.

Own direct intake, Wayfinder packet validation, ledger partition, question design, one authorized Markdown artifact, verification, and the matched Return. The Direct user or Wayfinder retains recipient and sender identity, output and disclosure authority, delivery, answers, reconciliation, the downstream decision or prerequisite, and continuation. Leave caller, tracker, domain, specification, implementation, Git, and external state unchanged.

```text
Direct | Wayfinder -> Admit -> Lock -> Gap -> Draft -> Cover -> Save -> Verify -> Direct | Wayfinder Return
```

## Direct Or Wayfinder

**Direct.** Infer supplied context. Default the current user as return and reconciliation owner, deadline to `none`, overwrite to `no`, delivery authority to the user, and response format to Markdown; select storage through Save. Ask at most one compact intake for remaining user-answerable fields that materially affect recipient, scope, effort, sensitivity, or path. Return each inference as an assumption; never ask the user to answer the stakeholder-owned gap.

**Wayfinder.** Accept only one selected Questionnaire ticket with every applicable field:

```text
Caller and return owner: Wayfinder
Questionnaire ticket identifier:
Sender identity or role:
Recipient name or identifying role:
Recipient expertise and relationship to sender:
Recipient knowledge and disclosure authority:
Downstream decision or prerequisite:
Initial needed-back items:
Authorized context, source pointers, and source-check results:
Answer use and reconciliation owner:
Deadline or none:
Effort budget and Markdown response format:
Authorized output root or exact path:
Artifact lifetime and retention owner:
Sensitive-context constraints:
Overwrite authority: yes | no
Delivery authority and assumptions:
Continuation owner: Wayfinder
```

Do not infer Wayfinder-owned authority or ask the user for packet state. A missing, stale, contradictory, or weaker field returns `Incomplete` with that exact gap and creates no artifact.

## Admit

Admit only when one identifiable external stakeholder owns material knowledge unavailable to the current user or Wayfinder and authorized inspectable sources; one decision or prerequisite depends on it; the gaps fit one recipient and effort budget; a legal artifact boundary exists; and delivery plus downstream authority stay outside this skill.

Partition every supplied gap before drafting:

- recipient-owned: admit;
- source-answerable or current-user-owned: exclude and name its owner;
- another external recipient: return the complete proposed split without writing;
- missing or unverified recipient identity or authority: return `Incomplete`;
- proven route, owner, or coherence mismatch: return `Not admitted`.

For a Direct terminal mismatch, recommend `$research` for source evidence, `$grilling` for a conversation-only user decision, `$grill-with-docs` when durable repo-backed domain capture must remain active, or `$repo-bootstrap` when required `.scratch` or `.tmp` state is missing or incompatible. For Wayfinder, return only the classification and exact gap; do not select or recommend its next route.

## Lock

Before drafting, lock entry and return owner; sender; recipient identity, role, expertise, relationship, knowledge and disclosure authority; one decision or prerequisite and answer use; admitted and excluded items; authorized sources; deadline; effort and response format; sensitivity; exact target or authorized root; storage and overwrite state; applicable lifetime and retention owner; continuation owner; and `Delivery: not performed`.

A changed recipient, decision or prerequisite, ledger, sensitivity authority, output root, storage class, overwrite authority, or applicable lifetime reopens its owning gate.

## Gap

Give every admitted item a stable ID and record:

```text
Needed-back ID:
Missing fact | judgment | constraint | example | risk:
Downstream impact:
Recipient authority:
Authorized-source check:
Priority and dependency:
Expected response shape:
Mapped question IDs:
```

Every admitted item maps to at least one atomic question, and every substantive question maps back to an admitted item. Return exclusions with their owners; remove curiosity, duplicates, answered facts, and workflow instructions.

## Draft And Cover

Draft recipient-facing Markdown with a title; purpose and decision or prerequisite; sender and recipient; answer use; deadline, effort, and response instructions; bounded context; and themed stable questions with suitable answer space.

Order by decision value and dependency. Keep every question atomic, neutral, recipient-answerable, authority-bounded, response-shaped, and effort-fit; remove compounds, leading language, speculation, source-answerable or duplicate content, leakage, and scope drift. An optional final catch-all fits the budget and covers no known item.

Minimize context. Omit credentials, secrets, unapproved personal data, privileged material, and unrelated internal detail; redact or abstract authorized sensitivity when the question remains answerable. If necessary context lacks disclosure authority, return `Incomplete` before writing and name the required authorization or sanitized substitute.

Do not Save until bidirectional coverage, question quality, sensitive-context, and effort checks pass.

## Save

Choose the target in order:

1. an exact path authorized for this artifact;
2. a new collision-free `.md` name inside an authorized output root;
3. `<work-root>/.scratch/to-questionnaire/<slug>.md` for durable local use after proving `.scratch` is trackable and version-controlled storage fits the sensitivity boundary;
4. `<work-root>/.tmp/to-questionnaire/<slug>.md` only when the Direct user explicitly accepts a disposable artifact and `.tmp` is proved ignored.

Wayfinder requires a retention-suitable durable path, lifetime, and retention owner; `.tmp` is invalid. Missing or incompatible local-state policy is a setup gap, never authority to edit setup.

Before writing, resolve an absolute `.md` target; prove containment inside the authorized root after traversal and link handling; confine parent creation there; verify storage, sensitivity, and lifetime; and reject an existing target unless that exact overwrite is authorized. Root authority never implies overwrite. Capture the pre-write identity of any exact existing target authorized for replacement.

**Render first.** Immediately before Save, refresh target and worktree mutation state, preserve unrelated work as baseline evidence, render the complete candidate, and reread that exact content against every required Draft field, bidirectional mapping, sensitivity rule, and effort limit. Do not use the first write as validation. Only then write exactly one Markdown content artifact; create no coverage file, template, response store, manifest, delivery draft, or caller record.

## Verify

**Recipient lens.** Reread identity, purpose, context, stable questions, answer space, coverage, order, answerability, effort, sensitivity, and no claim of delivery or resolution.

**Transaction lens.** Prove the absolute target contains the verified content; admitted and excluded mappings are complete; lifetime and retention match the Lock; this invocation wrote only the authorized file; unrelated baseline or concurrent drift is recorded separately; and no delivery or caller mutation occurred. For durable Wayfinder use, hash the reread content with SHA-256.

A failed write or verification returns `Incomplete` with the exact target state. Never represent a partial, stale, or unverified artifact as `Questionnaire ready`.

## Return

Return one status: `Questionnaire ready`, `Not admitted`, or `Incomplete`.

**Direct Return**

```text
Status: Questionnaire ready | Not admitted | Incomplete
Reason or exact blocking predicate:
Recipient:
Sender:
Downstream decision or prerequisite:
Artifact path: <absolute path> | none
Covered and excluded needed-back summary:
Question count and estimated effort:
Sensitive-context omissions or redactions:
Unresolved assumptions:
Verification and attributable containment summary:
Delivery: not performed
Suggested owner: <Direct Not admitted only> | none
```

**Wayfinder Return**

```text
Status: Questionnaire ready | Not admitted | Incomplete
Reason or exact blocking predicate:
Caller and return owner: Wayfinder
Questionnaire ticket identifier:
Recipient and sender:
Downstream decision or prerequisite:
Answer use and reconciliation owner:
Artifact identity: <absolute path + SHA-256> | none
Storage class and sensitivity disposition:
Artifact lifetime and retention owner:
Admitted ledger and question mapping:
Excluded items and actual owners:
Question count and estimated effort:
Authorized source pointers used:
Sensitive-context omissions or redactions:
Unresolved assumptions:
Verification and attributable containment evidence:
Delivery: not performed
Wayfinder retains: waiting, delivery, answer reconciliation, downstream decision or prerequisite, and next-transition authority
```

`Questionnaire ready` requires a verified path and complete ledger; Wayfinder also requires hash, lifetime, and retention evidence. `Not admitted` requires a proven failed predicate and no artifact mutation. `Incomplete` names missing intake, evidence, authority, path, write, reread, or proof and reports any file state honestly.

Return to the Direct user or Wayfinder and stop. Never send, await, ingest, reconcile, interpret, certify, or act on answers, and never continue the caller's workflow.
