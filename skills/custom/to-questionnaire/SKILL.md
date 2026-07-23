---
name: to-questionnaire
description: Create one Markdown discovery questionnaire for one external stakeholder who holds facts or decisions the user cannot supply.
---

# To Questionnaire

**Outcome:** one recipient-ready questionnaire that closes a named knowledge gap for one downstream decision.

**Boundary.** This skill owns send intake, the needed-back ledger, question design, one Markdown artifact, verification, and its returned path. The user owns the recipient, delivery, answers, and downstream decision. Leave tracker, domain, specification, Git, and external state unchanged. Never contact or answer for the recipient.

**Grill the send, not the subject.**

**Admit.** Proceed only when one identifiable external stakeholder owns material knowledge unavailable from inspectable sources. When sources can answer, recommend `$research` and stop. When the current user owns the decision, recommend `$grilling` and stop.

**Lock.** Trace supplied context. Lock one recipient; their role, expertise, and relationship to the sender; the downstream decision; what must be learned; how answers will be used; the deadline; the effort budget; and the authorized output path. Infer available fields. Ask one compact intake only for missing send information the user can reasonably know.

For a direct request, default the current user as the return owner, delivery authority to the user, delivery to not performed, overwrite authority to no, and the response format to Markdown. Keep every inference visible as an unresolved assumption.

**Gap.** Build a needed-back ledger. Each missing fact, judgment, constraint, example, or risk names the downstream decision it unlocks. When materially different gaps belong to different recipients, return the proposed split instead of blending them.

**Draft.** Give the recipient enough context to answer without reconstructing the conversation. Order questions by decision value, then dependency. Keep each question neutral, recipient-answerable, and about one idea. Add answer space and a short “why this matters” only when it prevents misreading.

Use a title; purpose and decision; sender, recipient, and answer use; context; answering instructions; themed questions; and a final catch-all.

**Cover.** Map every needed-back item to a question. Remove duplicate, compound, leading, speculative, source-answerable, and out-of-scope questions. The catch-all does not cover a known ledger item.

**Save.** Write exactly one file. Default to `<work-root>/.tmp/to-questionnaire/<slug>.md` after verifying the path is ignored. Otherwise recommend `$repo-bootstrap` and stop. An explicitly supplied path overrides the default.

Before the first write, classify the artifact's sensitivity; resolve the absolute `.md` target and prove it remains contained in the authorized root after traversal and link handling; reject a collision unless overwrite of that exact target is authorized; and capture the target and unrelated worktree state. Refresh that state immediately before Save. Render and reread the complete candidate against Draft and Cover before writing. If the target or worktree changed concurrently, return `Incomplete` with the drift and write nothing.

**Verify.** Reread the artifact as the recipient. Verify identity, context, coverage, priority, answerability, effort fit, sensitive-context minimization, path existence, exact content, and that this invocation changed only the authorized file. Record unrelated baseline drift separately. A failed or partial write returns `Incomplete` with the exact artifact state; never report it as ready.

**Return.** Return one typed status and stop:

```text
Status: Questionnaire ready | Not admitted | Incomplete
Reason or exact blocking predicate:
Recipient:
Sender:
Downstream decision:
Artifact path: <absolute path> | none
Covered and excluded needed-back summary:
Question count and estimated effort:
Sensitive-context omissions or redactions:
Unresolved assumptions:
Verification and attributable mutation summary:
Delivery: not performed
Suggested owner: <$research or $grilling for Not admitted only> | none
```

`Questionnaire ready` requires one verified artifact and complete ledger. `Not admitted` requires a proven failed Admit predicate and no artifact mutation. `Incomplete` names missing intake, authority, path, coverage, write, reread, or proof and reports any file state honestly. Stop before delivery or downstream synthesis.

Complete only when Admit passes; one recipient and downstream decision are locked; every needed-back item has an atomic, recipient-answerable question; the questionnaire fits the effort budget; the complete render passes its pre-Save gates; the artifact passes reread; only the authorized file changed; and typed Return reports its exact path, state, delivery status, and unresolved assumptions.
