---
name: change-review
description: Review one selected branch, WIP, staged or since-X diff, PR, or fixed implementation candidate read-only for concrete correctness and code-quality problems. Use for direct review or caller-triggered independent review; exclude repository-baseline audits, repair requests, and explicit High Assurance Review.
---

# Change Review

Review one code change against its accepted behavior and repository standards.
Return only evidence-backed findings or a truthful pass. Never edit, repair,
delegate, or authorize a successor.

## 1. Pin

Use the candidate and comparison point the caller names. Otherwise select the
current WIP, including staged, unstaged, and in-scope untracked files. Capture
the exact diff or content and enough identity to repeat the check. Stop as
`incomplete` when the candidate is empty, ambiguous, partial, or cannot be
identified completely.

Review the captured candidate, not a later version. The repository baseline is
context, not part of the candidate. A whole-repository or subsystem baseline
audit is outside this skill.

When the caller declares `Formal review: yes`, load
[Formal Review](references/FORMAL-REVIEW.md) and apply its additional admission,
remediation, decision, and Return rules. Otherwise do not load it.

## 2. Understand

Read the accepted request and commitments, repository instructions and durable
decisions, the shared engineering contract when routed, meaningful nearby code
and tests, and any caller-supplied proof. Use a supplied specification when it
exists. Without one, do not infer product intent from tests or implementation;
review the observable request and repository contracts that are available.

Trace each meaningful change through its real owner and callers to its result or
effect. Include an applicable failure or recovery path and any behavior the
change replaces or makes redundant.

## 3. Inspect

First judge whether the candidate delivers the accepted behavior with the right
meaning, scope, contracts, and complete replacement or removal. Then judge the
implementation independently for correctness, ownership, data shape, interface
clarity, simplicity, maintainability, and proof proportional to the claim.
Neither judgment may hide failures in the other.

Ask whether the change introduces indirection, mutable state, branching, or a
second path that no current caller or requirement justifies. Prefer direct,
repository-native code, but do not report a preference as a defect.

Follow only conditions the candidate activates. For a touched trust or effect
boundary, migration, concurrent state, or partial-effect path, inspect the
applicable contract and failure behavior. For removed or replaced behavior,
inspect displaced callers, registrations, configuration, proof, and public
documentation. An inactive concern creates no checklist or specialist review.

When evidence identifies a serialized, stored, configured, pinned-dependency,
lifecycle, or cross-language boundary outside the visible call graph, trace
that boundary and its affected consumers before judging the change safe.

## 4. Verify

Reuse proof bound to the candidate. Run only safe checks needed to resolve a
material finding candidate, repository requirement, or concrete uncertainty.
Prefer the real caller or artifact when an isolated check cannot establish the
claim; unavailable optional proof is a stated limit, not an automatic defect.

Load [Finding Contract](FINDING-CONTRACT.md) before admitting a finding. Treat
every observation as a hypothesis until it satisfies that contract. Verify the
location and decisive evidence yourself; another agent's report, test count, or
tool output summary is not sufficient by itself.

## 5. Return

Repeat the candidate identity check. If mutable content changed, return
`incomplete` and name the drift; do not silently recapture it.

For ordinary review, list admitted findings in impact order with their location,
evidence, impact, and required correction or proof. If required evidence remains
unresolved, return `Review incomplete` and the gap. Otherwise, when no finding
remains, say `No findings`. Include only material checks, skipped proof,
uncertainty, and the candidate identity needed to understand the conclusion.

Formal review returns the decision and fields defined by its conditional
reference. In every mode, return control to the caller with mutation and
successor authority unchanged, then stop.

Completion requires the selected candidate to be fully inspected, every
reported finding to satisfy the Finding Contract, material uncertainty to be
named, and the final identity check to agree with what was reviewed.
