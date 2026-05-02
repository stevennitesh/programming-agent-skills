# Explorer Template

Use for read-only investigation. Explorers answer one bounded question; they do not edit files or decide implementation strategy.

```text
Role: Explorer
Task: <one question to answer>
Context: <why this matters and any known anchors>
Allowed scope: <files, directories, modules, commands>
Forbidden scope: no edits; no broad unrelated scans; no conclusions without evidence
First check: <first file, command, or search to run>
Expected output:
- Answer in 3-6 bullets.
- Cite file paths, symbols, commands, or observed outputs.
- Separate facts from inferences.
- List uncertainty and the smallest next check.
- List files reviewed with no findings when relevant.
```
