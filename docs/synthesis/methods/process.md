# Skill Synthesis Process

This is the working process for turning source research into compact,
powerful skills.

The goal is not to write verbose skills. The goal is to use a generous draft as
temporary scaffolding, then compress it into predictable behavior.

```text
source pressure
  -> generous synthesis
  -> controlled language pass
  -> behavior audit
  -> blunt gates
  -> validation on real tasks
  -> prune
```

The final artifact should be compact. The path there can be exploratory.

```text
Think generously.
Encode tightly.
Gate bluntly.
Validate against reality.
Prune without mercy.
```

## 1. Source Pressure

For each skill, name the few sources or priors it should recruit. Do not start
with a bibliography. Start with behavioral pressure.

For each source, extract only:

- leading words;
- rules;
- failure modes;
- evidence gates;
- stop/ask conditions.

Example for `tdd`:

```text
Test-Driven Development: By Example
Growing Object-Oriented Software
Specification by Example
Working Effectively with Legacy Code
```

Potential extraction:

```text
red-green-refactor
smallest meaningful seam
red must fail for the missing behavior
refactor only while green
no red, no TDD claim
```

## 2. Generous Synthesis

Write the first version slightly verbose on purpose. It is scaffolding.

Include:

- why the skill exists;
- when to use it;
- what to do first;
- what not to do;
- what evidence proves done;
- what failure modes it prevents.

This draft is allowed to explain. It should expose the behavior before the
compression pass removes excess prose. Use
[`../GENEROUS-TEMPLATE.md`](../GENEROUS-TEMPLATE.md) when the reasoning needs a
durable note.

## 3. Compact Synthesis

Now turn prose into skill text.

Use:

- active verbs;
- one instruction per sentence;
- explicit conditions;
- strong leading words;
- `must`, `no`, `stop`, and `done` where a gate matters;
- context pointers for branch-specific detail.

Avoid:

- soft phrasing;
- decorative vocabulary;
- repeated meaning;
- long explanations in the main path;
- branch-specific reference in the top-level path.

Use [`../TEMPLATE.md`](../TEMPLATE.md) for the compact synthesis handoff.

## 4. Behavior Audit

After compacting, test every candidate runtime line:

```text
What behavior does this change?
What failure mode does this prevent?
What evidence gate does this enforce?
What leading word recruits the right prior?
Is this duplicated, bloated, or better moved behind a context pointer?
```

If a line only sounds intelligent and does not steer behavior, move it to
reference or cut it.

## 5. Blunt Gates

Only the gates get blunt.

Keep the professional term:

```text
Use red-green-refactor through the smallest meaningful seam.
```

Make the gate hard:

```text
Red must fail for the missing behavior.
Green must pass with the smallest implementation.
Refactor must preserve behavior.
No red, no TDD claim.
No proof, no done.
```

Do not flatten professional taste into low-resolution commands.

```text
Do not caveman the taste.
Caveman the gates.
```

## 6. Real Task Validation

Run the skill against real repo tasks, old transcripts, or representative
fixtures.

Check:

- Did the agent read the right context?
- Did it choose the right slice?
- Did it stop when it should?
- Did it prove the behavior?
- Did it overclaim?
- Did it ask too early?
- Did it produce reviewable work?

This is where fake clarity shows up.

## 7. Prune

Final pass:

- remove no-ops;
- remove repeated meaning;
- remove decorative terms;
- move reference out;
- tighten completion criteria;
- keep each meaning in one source of truth.

## Done Shape

A finished skill should mostly contain:

```text
when to use this
what to do first
what words to think with
what proof is required
what shortcuts are forbidden
when to stop or ask
```

The target line shape is:

```text
Use <software-engineering taste term>
through <agent execution surface>
until <evidence gate>.
```
