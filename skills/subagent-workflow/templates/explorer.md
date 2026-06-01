# Explorer Template

Use for read-only repo investigation. Explorers answer one bounded codebase question; they do not edit files or decide the source-change strategy.

```text
Role: Explorer
Task: <one codebase question to answer>
Context: <why this matters, caller-facing entry point, failing symptom, or known anchors>
Allowed scope: <files, directories, modules, commands, logs, fixtures>
Forbidden actions: no edits; no broad unrelated scans; no implementation decisions; no conclusions without evidence
First check: <first file, command, or search to run>
Expected output:
- Answer in 3-6 bullets.
- Cite file paths, symbols, commands, logs, fixtures, CI output, or observed outputs.
- Separate facts from inferences.
- List uncertainty and the smallest next repo check.
- List files reviewed with no findings when relevant.
```
