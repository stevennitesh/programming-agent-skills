---
name: change-review
description: Review a diff, branch, PR, or uncommitted changes for correctness and maintainability problems. Exclude whole-codebase audits and implementation without a review request.
---

# Change review

Judge whether a change delivers the intended behavior and whether its implementation
is sound. Review without editing product code or publishing external comments.
For a review-and-fix request, finish the review phase before returning findings to
the authorized repair work. Review conclusions do not grant merge or release authority.

Use ordinary review by default. Only when the user explicitly requests high
assurance or a review by multiple independent reviewers, read
[High assurance](references/high-assurance.md). A large diff, a PR, or the phrase
"final review" alone does not activate that mode. Ordinary review needs no fanout.

## 1. Identify what is being reviewed

Use the target and comparison the user names. Otherwise use relevant current WIP,
including staged, unstaged, and in-scope untracked content. For a named branch or
PR, resolve its actual base and head; do not assume a branch called main or silently
replace an exact comparison with a merge-base comparison. If the target cannot be
inferred, ask for the missing selection. An empty selection means no changes to
review, not a successful review of an imagined candidate.

Record the resolved comparison and candidate identity. For mutable work, capture
the selected content, including untracked files and relevant surrounding evidence,
or hold exclusive custody while reviewing. A diff alone is insufficient when
callers, configuration, or stored representations determine behavior. Bind the
context and supplied proof to the version actually examined.

Read the request and governing requirements, repository guidance, and relevant
accepted decisions. Use a spec when one governs the work; do not require a tracker
or fabricate intent from tests or implementation. Missing intent may limit
conformance review while independently evidenced correctness checks can continue.
State that limit rather than implying all accepted behavior was verified.

## 2. Trace behavior and engineering quality

Check the outcome and scope first: does the ordinary caller receive the requested
meaning, including relevant rejection, partial-success, and completion behavior?
Then independently assess correctness, ownership, representation, simplicity,
maintainability, and proof. Working happy-path behavior does not excuse a concrete
design cost; attractive structure does not excuse an incomplete outcome.

Trace meaningful changes through real callers, owners, and effects. When a result
crosses stages or tickets, check that its actual produced or persisted form reaches
the consumer and preserves accepted values, issues, identity, and terminal behavior.
Follow serialization, configuration, dependency versions, lifecycle, and cross-language
consumers when they matter even if absent from the visible call graph.

Inspect activated risks: trust and authorization boundaries, shared state,
resource bounds, recovery, migration, and independently deployed consumers. For
removed or replaced behavior, check affected registrations, configuration, callers,
tests, and public guidance. Preserve necessary compatibility rather than demanding
deletion merely because two paths temporarily coexist.

Challenge duplicated decisions, exposed internals, unnecessary state, and layers
that add caller burden without useful ownership or policy. Check whether a simpler
repository-native approach preserves the required meaning. File size, one adapter,
unfamiliar syntax, or repeated text alone does not establish a design defect.
Keep unrelated baseline improvement discovery with audit-codebase.

## 3. Test finding hypotheses

Before reporting, apply [Finding standards](references/finding-standards.md).
Trace a concrete affected scenario and seek disconfirming evidence. Use the
baseline to distinguish an introduced or worsened problem from unrelated old code.
An unchanged line can still be the causal location of a regression activated by
the change; explain the connection rather than restricting investigation to hunks.

Reuse valid candidate-bound proof. Run safe, proportionate checks when they settle
a material question or satisfy repository policy. Scratch harnesses and caches
are acceptable within an isolated review; do not mutate live systems or the reviewed
source. Check whether tests distinguish a plausible wrong result and whether a
substitute bypasses the property under review. Test counts and reviewer agreement
are not evidence of correctness.

## 4. Return an evidence-backed conclusion

Recheck mutable candidate and decisive context identity. If it moved, identify
what was reviewed and what remains unreviewed; do not attach a clean verdict to
the new state. A later review can reuse unaffected evidence after revalidation.

Report actionable findings in impact order with precise locations, scenario,
evidence, consequence, and the required correction or proof. When no findings
remain, say so, and separately state any material coverage or evidence limit.
Do not equate "no findings" with complete coverage when required evidence is absent.
For an explicit gate decision, use the decision rules in Finding standards.

On a repair review, track prior findings as resolved, still present, disproved,
or unresolved. Inspect the repair and its affected consumers for new regressions;
broaden to the full successor when the change grows beyond the bounded repair.
Finish with the reviewed identity, findings, decisive checks, and material limits.
Return control to the caller; publication, repair, or delivery follows existing
authorization rather than being started by the review itself.
