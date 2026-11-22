# Final review

Use before this workflow opens an authorized PR, or when the user requests this
review method. [Change review](../../change-review/SKILL.md) owns candidate
evidence, findings, independence, correction review, and any requested gate
decision.

## Start with one independent review

Run relevant deterministic checks first. Give a fresh, read-only reviewer
independent of implementation and integration the fixed candidate and base,
accepted behavior, relevant contracts, check results, and known evidence gaps.
Keep the initial assessment independent of the author's verdict. Use the Sol
route in [Shared model routing](../../controlled-delegation/references/model-policy.md)
by default, subject to the user's requested review arrangement.

## Scope a second review to the risk

After handling initial findings, add a fresh, independent Astra review when a
credible consequential failure or unresolved design question merits separate
scrutiny. Name the question and the evidence a second reviewer can add. For
example, ask whether a checkout replacement after the final status check can
still reach removal. Give Astra the delivery candidate and focus the pass on
that risk.

## Finish on the delivery candidate

The lead assesses findings and verifies repairs. Reuse the same reviewer for
scoped corrections while they remain independent. Refresh the coverage the
changes affected. Use a fresh reviewer when independence is lost or a material
change makes the earlier review scope insufficient. Widen the review to cover
material gaps in the final candidate.

Report the final candidate, review coverage, decisive checks, and limits.
Missing required coverage stays incomplete. Complete the required review
before opening an authorized PR through [pr-delivery](../../pr-delivery/SKILL.md).
The lead retains final acceptance within the authority granted.
