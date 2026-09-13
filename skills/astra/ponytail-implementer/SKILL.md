---
name: ponytail-implementer
description: Simplify implementation within an assigned plan and engineering contract. Use only when explicitly assigned to an implementer; leads and reviewers do not load this guidance.
---

# Ponytail implementer

As the implementer, follow your assignment and repository engineering contract
for scope, quality, checks, custody, and handoff. Use this guidance to choose
simpler means; raise consequential conflicts with the lead.

## Choose sufficient means, then build

Read the affected flow and distinguish the accepted outcome from proposed means.
Before adding a wrapper, configuration option, fallback, or custom subsystem,
check whether the outcome needs it. Omit unnecessary means within your authority;
binding mechanisms require their owner's decision to change.

Look for a suitable implementation already in the repository, then for standard
library, native platform, or installed dependency support before writing your
own. Check actual caller requirements: data meaning, failure behavior, runtime
support, and operating limits. Similar API names do not establish a fit.

Choose the first sufficient option whose caller, dependency, and operational
burden fits the supported workflow. Once fit is established, stop searching and
implement it. Add machinery only for remaining needs. Real policy ownership can
justify structure even with one caller; line or file counts do not decide.

For a bug, search references to the prospective owner to discover sibling paths
the report may omit. Fix the owner of the violated rule, sharing the correction
only where those callers share its meaning.

Resolve consequential uncertainty about a simplification's limits. Record a
material limit and revisit condition at the existing owner when useful.

As you complete the change, remove machinery it displaced within the assigned
scope after checking consumers. Preserve required behavior and semantic checks.
Return through the assignment without copying this guidance into the lead's context.

Original Astra adaptation informed by Dietrich Gebert's Ponytail at
`356918eba965ee1eac64bd3a7f0dd02108350de5`; upstream notice: [LICENSE](LICENSE).
No upstream installation, hooks, modes, or additional skills are required.
