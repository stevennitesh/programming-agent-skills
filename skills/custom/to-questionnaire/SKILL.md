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

**Gap.** Build a needed-back ledger. Each missing fact, judgment, constraint, example, or risk names the downstream decision it unlocks. When materially different gaps belong to different recipients, return the proposed split instead of blending them.

**Draft.** Give the recipient enough context to answer without reconstructing the conversation. Order questions by decision value, then dependency. Keep each question neutral, recipient-answerable, and about one idea. Add answer space and a short “why this matters” only when it prevents misreading.

Use a title; purpose and decision; sender, recipient, and answer use; context; answering instructions; themed questions; and a final catch-all.

**Cover.** Map every needed-back item to a question. Remove duplicate, compound, leading, speculative, source-answerable, and out-of-scope questions. The catch-all does not cover a known ledger item.

**Save.** Write exactly one file. Default to `<work-root>/.tmp/to-questionnaire/<slug>.md` after verifying the path is ignored. Otherwise recommend `$repo-bootstrap` and stop. An explicitly supplied path overrides the default.

**Verify.** Reread the artifact as the recipient. Verify identity, context, coverage, priority, answerability, effort fit, sensitive-context minimization, path existence, and that only the authorized file changed.

**Return.** Report the absolute path, recipient, downstream decision, covered ledger items, and unresolved send assumptions. Stop before delivery or downstream synthesis.

Complete only when Admit passes; one recipient and downstream decision are locked; every needed-back item has an atomic, recipient-answerable question; the questionnaire fits the effort budget; the artifact passes reread; only the authorized file changed; and its path and unresolved assumptions are returned.
