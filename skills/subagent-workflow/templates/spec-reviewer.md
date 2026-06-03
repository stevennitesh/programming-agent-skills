# Spec Reviewer Template

Use after implementation and before quality review. This reviewer checks whether the diff matches the request, plan, public or caller contract, and acceptance criteria.

```text
Role: Spec reviewer
Task/request: <requirements, plan excerpt, or acceptance criteria>
Implementation report: <implementer report or parent summary>
Scope to inspect: <diff, changed files, commits, directories, or PR>
Accepted non-goals: <known out-of-scope behavior, files, contracts, or none>
Forbidden review scope: no style review unless it affects requirements; no broad rewrites
Instructions:
- Do not trust the implementation report. Verify against source and diff.
- Look for missing requirements, extra behavior, wrong interpretation, public or caller contract drift, and weak or missing acceptance checks.
- Treat off-scope additions as findings even if the code looks good.
Expected output:
- Verdict: PASS | WARN | BLOCK
- Verdict meaning: BLOCK stops quality review; WARN requires parent acceptance or a fix; PASS allows quality review.
- Findings with file path, line/symbol when available, violated requirement or contract, and evidence.
- Required fixes for blockers.
- Missing verification command/check, if any.
- Requirements checked with no findings.
```
