# Controlled Language Pass

Use this after drafting or rewriting skills. The goal is to make completion
gates and stop conditions blunt enough that the agent cannot wriggle around
them.

The useful pattern is not full caveman-speak. Full caveman-speak loses the
upper-bound attention handles. The better frame is controlled procedure
compression: keep the elite professional term, then write the gate in short,
observable, imperative language.

```text
elite leading words
  + controlled plain language
  + blunt gates
```

Example:

```text
Use red-green-refactor through the smallest meaningful seam.
Red must fail for the missing behavior.
Green must pass with the smallest implementation.
Refactor must preserve behavior.
No red, no TDD claim.
No proof, no done.
```

This keeps the professional steering phrase while making the evidence gate hard
and low-ambiguity.

## Compression Sources

These sources can sharpen the post-draft compression pass.

| Source | Use It For | Skill-Pack Takeaway |
| --- | --- | --- |
| [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/) | Controlled vocabulary and clear technical instructions | Treat skill wording as controlled technical language: fewer meanings per sentence, fewer ambiguous verbs, less decorative prose. |
| [Digital.gov Plain Language Guide](https://digital.gov/guides/plain-language/) | Plain-language discipline for public instructions | Prefer direct verbs, obvious structure, and reader-first wording over abstract process language. |
| [The Checklist Manifesto](https://atulgawande.com/book/the-checklist-manifesto/) | Expert checklists that prevent missed critical steps | Skills should preserve the steps experts skip under pressure, not summarize all possible expertise. |
| [Human Factors 101: Procedures](https://humanfactors101.com/topics/procedures/) | Procedure writing and task aids | Treat a skill as an operational aid: sequence, decision points, gates, and stop conditions matter more than exposition. |
| [FAA Human Factors Technical Writer's Guide](https://hf.tc.faa.gov/publications/1998-human-factors-technical-writers-guide/full_text.pdf) | Safety-critical procedural writing | Use active voice, concise steps, clear conditions, and observable outcomes when failure matters. |

These are not sources for engineering taste. They are sources for making taste
hard to evade once the right leading words have been chosen.

## Procedure

Apply this pass to each skill after the main vocabulary and workflow are
settled:

1. Keep the elite term.
2. Replace explanation with command where the behavior is already clear.
3. Split compound instructions.
4. Use `must`, `no`, `stop`, and `done` for gates.
5. Make every gate observable.
6. Delete polite mush.

Use this as a post-draft pass only:

- Keep leading words like `tracer bullet`, `deep module`, `seam`,
  `red-green-refactor`, `fixed-point review`, and `residual risk`.
- Shorten completion criteria until they are checkable.
- Add blunt failure gates where agents tend to overclaim.
- Prefer "No proof, no done" style gates over polite, slippery prose.
- Do not flatten the whole skill into low-resolution commands.

The rule:

```text
Do not caveman the taste.
Caveman the gates.
```
