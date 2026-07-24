# To Tickets Prompt 4 Isolation V2

This directory is the clean continuation of Deploy Prompt 4. It replaces no
historical capture. The original fixtures and raw outputs remain preserved one
level above, but they receive zero decision credit because worker-visible
output boundaries leaked evaluator conclusions.

`generate_fixtures.py` separated each complete worker packet from root-only
evaluator material. Worker packets contain the task, source, authority,
simulated runtime, exact arm package, permitted tools and mutations, neutral
output shape, and assigned capture path. Root evaluator fixtures contain the
hypothesis, expected weakness, rubric, scoring rule, candidate terms, and
conclusions. For every comparison pair, replacing only the exact delimited
runtime-package slot makes the M0 and H1 packets byte-identical. The generator
now refuses to overwrite these payloads after the package root was rederived
to V1; `registry.json` and `payloads/**` are the immutable entering-arm
evidence.

`registry.json` freezes fixture, payload, and normalized-pair identities.
The three comparison fixture pairs are:

| Cluster | Worker fixture | Root evaluator fixture | Normalized pairs |
| --- | --- | --- | ---: |
| `H1-01` | `6a9cbd49505e3e9dfb71bd7f27d3b2194582a09563277a61aab33621e5544017` | `0fea938266670d0a079c14af97a6090781848f232a6135021093139b4aeee554` | 5/5 equal |
| `H1-02` | `29c48688ed279bb59fb6c08f03956ee5730e17e86aad376bbd0805c5d35e1f73` | `3db1823bd081ee04ed6cb14c45fc9e44b79a5f2f38eca2fdb9fc48fc875bbac2` | 5/5 equal |
| `H1-03` | `d0035ebcfd4ca0aa8306be9f92b8ac63a9a5d26eb324c1d250159a9565bb9437` | `d9f809a4dc28337966b226b6e4a849cb28f697e8e711b1e24cf943d20c60d05d` | 5/5 equal |

All credited samples used fresh contexts at exact `gpt-5.6-sol`, high
reasoning, Codex desktop, fixture-scoped simulated tools, and no live provider.
The root inspected every complete credited response and operation log.

Capture layout:

- `capture-slots/viability/`: credited clean M0 viability outputs;
- `raw/current/cluster-01/`: credited H1-01 M0 controls;
- `raw/current/cluster-02/m0/` and `h1/`: credited paired H1-02 arms;
- `raw/current/cluster-03/m0/`: credited H1-03 M0 controls;
- `raw/deviations/pre-viability/`: zero-credit samples dispatched before the
  viability gate; and
- `raw/deviations/viability-fixture-defect/`: zero-credit first V-02 attempt
  against an under-specified source contract.

The terminal judgments and V1 refreeze are in [`results.md`](results.md).
