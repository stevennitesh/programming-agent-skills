# Independent review

Use when a fresh review context would materially improve judgment or the caller
requires independent review. One reviewer can provide this isolation; multiple
reviewers are a separate coverage choice.

The reviewer is separate from the candidate's implementation and integration
authors. Give it the fixed candidate and comparison, accepted requirements,
relevant sources, available evidence, assigned scope, and the finding and output
contracts from the main skill. It needs access to surrounding context and
dependencies sufficient to judge the change, not only the diff.

Start with a fresh context rather than the implementation conversation. For a
general review, keep lead suspicions and peer findings out of the initial brief.
For targeted verification, provide the hypothesis as an unproven claim and ask the
reviewer to assess it independently. Preserve factual requirements, constraints,
and known verification results without supplying a desired verdict. Isolation must
not deprive the reviewer of governing context.

Reviewers are read-only: they assess and return findings, coverage, and evidence
gaps. They do not repair, publish, or delegate further. Establish a fixed review
target under the active workflow's custody rules before dispatch. Separate
conversations or worktrees do not isolate mutable services, databases, or proof;
report the independence actually achieved.

The lead evaluates returned findings against the candidate and relevant contrary
evidence, resolves disagreements, and owns the final conclusion. Keep independent
contributions attributable by reviewer and scope. If the lead authored or
integrated the change, distinguish its synthesis from the independent review.

For a repaired successor, reviewers may retain their review context while it
remains useful and independent of implementation. Use fresh reviewers when needed
to restore isolation. Prior findings and evidence apply only while still valid
for the new candidate. If required independence cannot be established, report that
limit without presenting a direct review as independent.
