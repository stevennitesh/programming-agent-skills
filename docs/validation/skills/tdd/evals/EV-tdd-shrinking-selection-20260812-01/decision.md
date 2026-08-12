# TDD Shrinking Selection Evaluation

Decision: `accept`

## Registration

- Class: `defect-correction`.
- Expected control failure: reject otherwise-suitable property-based testing
  solely because the framework does not provide shrinking.
- Entry predicate: TDD is already activated; intended behavior and an
  independent oracle are settled; a stable property ranges over a broad or
  combinatorial valid domain covered by a credible generator.
- Applicability: situational. It applies only when property-based testing is a
  credible test shape; it does not change TDD invocation.
- Control: repository commit
  `9200a972adc2bebae06ec8a4dcb75a8cc7be9b85`; TDD `tests.md` Git blob
  `5ab57c8ff5385f23a64dac35f32779f99099a7bf`.
- Candidate: TDD `tests.md` Git blob
  `95846bcfb8cbae9f3c487e78f4128bc1ac7e439b`.
- Host and model: fresh-context subagents on the current Codex host using the
  session-default model and reasoning configuration; exact model telemetry,
  seed, token use, and latency were unavailable.
- Tools and authority: read-only repository inspection; no mutation authority.

## Fixed Cases And Rubric

Every entry-positive sample judged the same five cases:

1. a broad, valid, credible generated domain without shrinking must still
   select property-based testing;
2. a smaller generator-producible case that reproduces the target failure is
   an acceptable reduction;
3. a reduced case outside the declared valid domain is rejected;
4. a reduced case that triggers a different exception or location is rejected;
5. exactly eight enumerable cases use an exhaustive table.

A critical failure was rejecting case 1 solely for missing shrinking, accepting
case 3 or 4, or selecting generation for case 5. The wrong-condition cohort
repeated invalid-generator, wrong-failure reduction, and small-domain cases.

## Results

All five controls failed case 1 by choosing focused examples or a table because
shrinking was unavailable. All five passed cases 2 through 5. The registered
deficit therefore appeared with no observed variance.

All five candidates passed all five cases: 25/25 judgments, five of five
overall passes, no critical failures, no variance, and worst result `PASS`.
Both wrong-condition controls and both wrong-condition candidates rejected the
invalid generator, rejected the different-failure reduction, and chose an
exhaustive table for the small domain: 6/6 judgments per arm.

One candidate wrong-condition sample initially used a raw file SHA-1 rather
than `git hash-object`, stopped before inspection, then retried after the exact
Git verifier confirmed the frozen candidate. No candidate bytes or judgments
changed.

## Decision And Limit

`accept`. The candidate removes shrinking from property-testing admission while
requiring any performed reduction to remain generator-producible and reproduce
the target failure. It preserves the credible-generator and small-domain
non-trigger gates without adding a TDD phase, Return field, artifact, or
universal property-testing requirement.

This evaluation proves instruction-following judgment on the fixed cases. It
does not compare property-testing frameworks, reducer quality, performance, or
empirical defect-finding effectiveness.
