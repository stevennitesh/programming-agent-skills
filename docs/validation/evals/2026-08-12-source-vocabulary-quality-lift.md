# Source Vocabulary Quality-Lift Evaluation

- claim: source-native, predicate-bound wording improves design and test choice
  without weakening correctness or activating extra ceremony;
- class: `quality-lift`;
- applicability: common for the ordinary-design branch because the active core
  workflow and shared Codebase Design caller both exercise ordinary interfaces;
  situational for characterization, property-based testing, wrong abstractions,
  and substitutes because each requires its named runtime predicate;
- control: commit `96b7d0fa325b3a8cbffdede6c73d66c97da24ce2`;
- candidate: that commit plus tracked-diff hash
  `a2b10a86252eef176b18a745962a9441393cb87c`, produced by
  `git diff --binary --no-ext-diff | git hash-object --stdin` in Windows
  PowerShell;
- task and fixed inputs: the six cases and rubric below, supplied identically to
  each arm without prior outputs or candidate conclusions;
- model, host, and reasoning: fresh subagents on the current Codex host using
  the session-default model and reasoning configuration; exact model telemetry
  was unavailable;
- tools and authority: read-only repository inspection; no mutation authority;
- evidence and runtime: canonical skill text at the frozen bytes; five fresh
  entry-positive controls and five fresh entry-positive candidates, followed by
  two fresh wrong-condition controls and two fresh wrong-condition candidates;
  each sample ran to one terminal judgment;
- mutation boundary: control, candidate, and repository remained unchanged
  during each cohort.

## Rubric

The same six cases tested: a small stateless local interface; observable legacy
behavior with intended behavior unavailable; a broad combinatorial property; a
small enumerable property; a shared abstraction with distinct meanings,
owners, and change rates; and interchangeable adapters. Passing behavior omits
dormant design fields, treats characterization as actuality only, selects
property-based testing only when generators and shrinking discriminate better
than examples or exhaustive enumeration, unshares only a wrong abstraction,
and preserves applicable preconditions, postconditions, and class invariants
for interchangeable implementations.

## Result

Entry predicate: the task presents at least one of the six cases whose correct
choice depends on conditional design, characterization, property-testing,
wrong-abstraction, or substitute-contract guidance. Control showed a repeatable
deficit: four of five samples found low-risk design ceremony; all five found no
explicit property-testing selection rule; three of five found no reliable
small-domain exhaustive-testing choice. Control remained safe on unresolved
intended behavior and usually chose a reasonable collapse for the wrong
abstraction. Per-control results were `A/B/C/D/E/F`: samples 1, 4, and 5 =
`FAIL/PASS/FAIL/FAIL/PASS/PASS`; sample 2 =
`PASS/PASS/FAIL/FAIL/PASS/PASS`; sample 3 =
`FAIL/PASS/FAIL/PASS/PASS/PASS`. Worst result: three rubric failures.

All five final-candidate samples returned
`PASS/PASS/PASS/PASS/PASS/PASS`: they omitted dormant design fields, chose
property-based testing for the broad domain and an exhaustive table for the
small domain, kept characterization below correctness and corrective RED,
restored bounded duplication for the wrong abstraction, and used behavioral
subtyping for interchangeable adapters. Aggregate: 30/30 case passes, five of
five overall passes, no critical failures, no observed outcome variance, and
worst result `PASS`.

Final wrong-condition pairs tested shared-policy reuse, ambiguous preservation
evidence, small enumerable domains, delegation without a user request,
noninterchangeable adapters, and an ordinary stateless design. Control samples
returned `PASS/PASS/PASS/PASS/PASS/FAIL` and
`PASS/PASS/PASS/FAIL/PASS/FAIL`: 9/12 case passes, zero of two overall passes,
with design ceremony in both and unauthorized scouting in one. Candidate
samples both returned `PASS/PASS/PASS/PASS/PASS/PASS`: 12/12 case passes, two
of two overall passes, no critical failures, no variance, and worst result
`PASS`. Earlier exploratory wrong-condition sampling found the same delegation
and migration leaks; those bytes were repaired before the five final
entry-positive candidates and the final wrong-condition cohort.

Protocol deviations: four final-candidate samples initially interpreted the
registered PowerShell/Git blob identity as raw SHA-256. Each stopped before
candidate inspection, obtained the exact verifier, matched the frozen hash, and
then proceeded. Platform-required evaluator or memory instructions were read by
some samples; candidate judgment remained confined to the named canonical
skills. These deviations did not change candidate bytes, inputs, or outcomes.
Unavailable telemetry: exact model identifier, token usage, latency, and seed.

Decision: `accept`. The final candidate improves the registered choices without a
new phase, Return field, checklist, or mandatory artifact. The pre-existing TDD
invocation conflict between the engineering contract and composition owners was
not changed or claimed by this evaluation; it requires a separate behavioral
decision. Residual transfer gap: resolve that invocation conflict in the
relationship and Pack Composition owners before claiming that ordinary testing
cannot activate the TDD protocol; this Task 2 candidate transfers that decision
unchanged and makes no routing claim.
