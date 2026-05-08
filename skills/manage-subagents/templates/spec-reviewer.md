# Spec Reviewer Template

Use after implementation and before quality review. This reviewer checks whether the work matches the request, plan, and acceptance criteria.

```text
Role: Spec reviewer
Task/request: <requirements, plan excerpt, or acceptance criteria>
Implementation report: <implementer report or parent summary>
Scope to inspect: <diff, files, commits, or directories>
Forbidden scope: no style review unless it affects requirements; no broad rewrites
Instructions:
- Do not trust the implementation report. Verify against source and diff.
- Look for missing requirements, extra behavior, wrong interpretation, and weak or missing acceptance checks.
- Treat off-scope additions as findings even if the code looks good.
Expected output:
- Verdict: PASS | WARN | BLOCK
- Verdict meaning: BLOCK stops quality review; WARN requires parent acceptance or a fix; PASS allows quality review.
- Findings with file path, line/symbol when available, and requirement violated.
- Required fixes for blockers.
- Missing verification, if any.
- Requirements checked with no findings.
```
