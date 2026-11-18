# Final review

Use before this workflow opens an authorized PR, or when the user requests this
review method. [Change review](../../change-review/SKILL.md) owns candidate
evidence, findings, independence, correction review, and any requested gate
decision.

## Start with one independent review

Run the relevant tests, linters, and other deterministic checks first. Give a
fresh, read-only reviewer independent of implementation and integration a short
brief with the fixed candidate and base, accepted behavior, relevant repository
contracts, check results, and evidence gaps. Give the reviewer the accepted
decisions and leave out the author's reasoning and verdict. Select model and
effort from the Ultra review routes in
[Shared model routing](../../controlled-delegation/references/model-policy.md).
Ask the reviewer to assess the accepted outcome, follow affected callers and
dependencies, and use targeted reproductions where useful without changing the
candidate. Findings need a realistic trigger, consequence, and supporting evidence.

The lead checks findings against the evidence, coordinates authorized repairs,
and verifies affected behavior. Reuse the still-independent reviewer to verify
scoped corrections and retain coverage that remains valid.

## Add an Astra review for material risk

Add a fresh, independent Astra reviewer after addressing the initial findings
when a regression could have consequential effects or a material design question
remains unresolved. Give Astra the delivery candidate and a concrete failure
question to investigate. For example, can a retry submit the same order twice
if the provider accepted the first request before it timed out? Ask for a trace
or reproduction where possible. Focus the pass on the named risk and gaps from
the initial review.

## Finish on the delivery candidate

Refresh review evidence affected by repairs. Add a fresh review when changes to
interfaces, state transitions, or other behavior invalidate earlier coverage.
Use a full pass only when a material design change or a specific coverage gap
requires broader review. Verify other corrections with focused checks and review.

Missing required coverage or an unavailable required reviewer remains incomplete.
The lead retains final acceptance. Report the final candidate, completed coverage,
decisive checks, and material limits.

Complete the required review before PR opening. Use
[pr-delivery](../../pr-delivery/SKILL.md) for the authorized endpoint. Explicit
user changes to the review arrangement take precedence. Review grants no
publication or risk-acceptance authority and adds no PR workflow to
implementation-only or review-only work.

## Compare routes when evidence is needed

Apply explicitly requested model version updates directly. When choosing between
routes or assessing whether a route improves results, compare them on a small set
of identical PR snapshots. Include clean changes and defects with known later fixes.
Keep the fixes out of the reviewer's reach and verify findings against the code.
Compare Sol `high` with `xhigh`, measure what a targeted Astra pass adds after
Sol, or try Terra `medium` for a narrow review specialty. Track unique verified
defects by severity, disproved findings, repair time, and total reported usage.
[Telemetry](../../controlled-delegation/references/telemetry.md)
