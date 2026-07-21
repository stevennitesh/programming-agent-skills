---
name: to-questionnaire
description: Create one recipient-ready Markdown questionnaire when the user requests it or an active caller delegates one external-stakeholder knowledge gap with one recipient, downstream decision, needed-back ledger, and authorized output location. Return the verified path without sending, answering, or continuing the caller's workflow.
---

# To Questionnaire

Own one outcome: one recipient-ready Markdown questionnaire for one external stakeholder, plus its verified path and needed-back ledger.

This skill owns send intake, question design, one artifact, and verification. The caller owns its decision, tracker or workflow state, answer verification, and next transition. The user owns the recipient, delivery, answers, and unapproved sensitive material. Leave tracker, domain, specification, implementation, Git, and external state unchanged.

## Direct Or Delegated

A direct user invocation may infer available context and ask one compact intake for missing send information the user can reasonably know.

A delegated invocation must supply:

```text
Caller and return owner:
Caller item or decision identifier:
Recipient name or role:
Recipient expertise and relationship to sender:
Downstream decision or prerequisite:
Needed-back ledger:
Authorized context and source pointers:
Deadline and effort budget:
Authorized output root or exact path:
Sensitive-context constraints:
Known delivery assumptions:
```

When a delegated field is missing, return that exact field to the caller without creating a partial artifact or choosing the caller's next action.

## Admit

Proceed only when one identifiable stakeholder owns material knowledge unavailable to the caller and authorized inspectable sources; one downstream decision depends on it; the ledger fits one recipient and coherent questionnaire; an authorized path exists; and delivery plus downstream authority remain outside this skill.

Source-answerable facts return `$research` as the missing owner. A current-user preference or tradeoff returns `$grilling`. Several recipients return a proposed split without writing. Missing output setup recommends `$repo-bootstrap` only when no explicitly authorized or verified ignored path exists.

## Compose

1. **Lock.** Lock recipient, role, relationship, downstream decision, ledger, answer use, deadline, effort budget, and path.
2. **Gap.** Map each missing fact, judgment, constraint, example, or risk to what it unlocks.
3. **Draft.** Supply bounded context. Order questions by decision value and dependency. Keep each neutral, atomic, recipient-answerable, and within recipient authority.
4. **Cover.** Map every ledger item to questions. Remove duplicates, compounds, leading or speculative wording, source-answerable items, unnecessary sensitive context, and scope drift. A catch-all covers no known item.
5. **Save.** Write exactly one Markdown file at the authorized path; otherwise use `<work-root>/.tmp/to-questionnaire/<slug>.md` only after proving it ignored.
6. **Verify.** Reread as the recipient. Verify identity, purpose, context, coverage, priority, answerability, effort fit, sensitive-context minimization, path existence, and one-file containment.

Use a title; purpose and downstream decision; sender, recipient, and answer use; bounded context; instructions; themed questions with answer space; and one final catch-all.

## Return

```text
Artifact path:
Recipient:
Downstream decision or prerequisite:
Covered needed-back ledger:
Question count and effort estimate:
Authorized source pointers used:
Unresolved send assumptions:
Delivery: not performed
Caller retains: tracker, waiting, answer verification, downstream decision, and next-transition authority
```

Return to the delegating caller and stop. Do not recommend another route after a delegated run.

## Completion

Complete when Admit passes; recipient and decision are locked; every ledger item has an atomic recipient-answerable question; the effort budget fits; sensitive context is minimized; reread and one-file containment pass; and Return is complete. Stop before delivery, answer collection, answer interpretation, or caller continuation.
