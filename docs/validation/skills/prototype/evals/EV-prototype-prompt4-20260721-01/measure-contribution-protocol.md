# Prototype Prompt 4 Measure Contribution Protocol

Read every file in the assigned Prototype package and no other Prototype
package, synthesis, test, evaluation, prior output, or peer result. This is one
read-only behavioral case. Do not execute, mutate, invoke another skill, or
invent facts.

Audit Codebase asks which of cache shapes A or B is the better design candidate
under workload W. It supplies:

- decision owner Casey and return owner Audit Codebase;
- claim level `design evidence` and judgment mode `rule-based`;
- metric milliseconds per operation;
- identical input distribution and environment facts;
- two warmups and five samples per shape;
- fixed rule: select B only when its median is at least 15 percent lower and
  its worst sample is no higher than A's;
- one invocation-owned disposable path, permitted process and cache effects,
  cleanup dispositions, one command, and a finite bound; and
- known confounders and unsupported extrapolations.

The request is comparative design evidence, not diagnosis, an SLO, or
production certification.

Return:

- files loaded and the one decision-bearing branch;
- the ordered evidence and ownership sequence;
- the observations the final packet must contain;
- the exact terminal packet that would follow these supplied observations:
  A samples `10, 11, 10, 12, 10`; B samples `8, 8, 9, 8, 9`; and
- artifact and live-resource state.

Do not grade the package or suggest wording.
