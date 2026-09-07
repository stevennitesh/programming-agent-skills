# Model policy

Most runs begin on Sol Medium or Astra Medium. Sol Medium is the everyday default;
an Astra Medium root can brainstorm, plan, and coordinate directly. Retain a suitable
root rather than switching to match an entry convention. Separate discovery and
planning passes are optional. The main skill requires delegated review for
coordinated feature runs. Preserve explicit user model, effort, provider, and budget
constraints.

| Model | Effort | Choose it for |
| --- | --- | --- |
| GPT-5.6 Luna | Max | Easy retrieval, sorting, repetitive or extensive file work, mechanically checked bulk processing, and easy independent swarm assignments when parallel work is justified |
| GPT-5.6 Sol | Medium | Everyday use, small fixes, and normal bounded implementation and verification of an agreed approach |
| GPT-6 Astra | Medium | Brainstorming, planning, normal independent change review, difficult implementation/debugging, and unresolved design or methodology questions |
| GPT-6 Astra | XHigh, explicitly selected | Intensive review or particularly difficult design problems; not automatic escalation beyond Medium |

## Decide using the actual uncertainty

- Consider consequence, reversibility, and verification strength, not file count.
  A broad rename can be mechanical; one timestamp join can introduce look-ahead bias.
- Separate implementing a known method from deciding whether it is valid. Use Sol
  Medium for a bounded implementation of an agreed method; Astra Medium for difficulty or uncertainty in
  assumptions, leakage, numerical stability, or system interactions. Require an
  independent numerical check such as an analytic case or trusted implementation;
  a stronger model cannot substitute for evidence.
- Luna's low price can come with longer execution and more repairs. Give it bounded
  work with decisive checks. Let Python, SQL, or another engine do heavy computation.
  Use direct search for simple lookups. Large scope alone does not make work easy
  enough for Luna. Its swarm role does not authorize fanout; concurrent implementation
  follows the main skill's parallel-implement route when requested.
- Retain a sufficient permitted model when switching would erase the savings.
  Astra can implement directly through completion.
- Change route for a named capability gap, demonstrated failure, or material change
  in uncertainty. Missing requirements or broken environments need resolution,
  not a more expensive model. Before retrying or escalating, follow
  [Repair allowances](repairs.md).
  For implementation recovery, use Sol Medium -> Astra Medium; from Luna Max,
  choose Sol Medium or Astra Medium for the demonstrated weakness. If Astra Medium
  is insufficient, ask for a revised route rather than automatically selecting XHigh.

Choose for the current uncertainty; a phase change alone does not require switching.
Keep unresolved design questions with the agent resolving them rather than handing
an untested assumption to an implementer as settled.

## Limits and conditional detail

Select from this table unless the user explicitly chooses otherwise. Astra XHigh
requires explicit selection; task difficulty alone does not authorize it. Ultra is
an orchestration choice outside this policy. If no permitted route is sufficient, preserve the
work and report the limitation. This policy does not itself require review or
authorize delegation.

When dispatching, changing models, or deciding whether a current root outside the
default table can continue directly, read [Runtime selection](runtime.md) for
controls, context inheritance, and active-parent exceptions. The main skill owns
budgets and custody; [Repair allowances](repairs.md) owns failure handling and
repair limits.

These task assignments are benchmark-informed judgments, not proven specializations.
Read [Evidence and limits](model-policy-evidence.md) when comparing or revising
choices, interpreting cost/time frontiers, or conducting requested calibration.
