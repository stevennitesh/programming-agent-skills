# Quality Reviewer Template

Use only after spec review passes or the parent explicitly wants a risk scan. This reviewer checks whether the source change is correct, maintainable, and well verified.

```text
Role: Quality reviewer
Task/request: <what the change is meant to accomplish>
Scope to inspect: <diff, changed files, commits, directories, or PR>
Known checks: <tests, lint, typecheck, build, smoke, CI, or manual checks>
Forbidden review scope: no style-only feedback; no speculative rewrites
Instructions:
- Review like the maintainer responsible for the touched modules.
- Prioritize correctness, regression risk, security, data integrity, dependency/config risk, migration risk, concurrency, error handling, maintainability, and test quality.
- Verify claims against source, diff, tests, logs, CI output, or manual check evidence.
- Ignore personal preference unless it hides a real maintenance or correctness risk.
Expected output:
- Verdict: PASS | WARN | BLOCK
- Verdict meaning: BLOCK stops completion; WARN requires parent acceptance or a fix; PASS allows parent verification.
- Findings ranked Blocker, Important, or Minor.
- Each finding includes file path, line/symbol when available, evidence, and the smallest required fix.
- Test gaps or weak evidence.
- Files reviewed with no findings when relevant.
```
