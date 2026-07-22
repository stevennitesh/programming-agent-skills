# Source Distillation Prompts

These optional prompts turn primary and outside sources into a compact set of
important concepts and usable techniques. The owning method is
[`../source-distillation-flow.md`](../source-distillation-flow.md).

| Prompt | Use | Output |
| --- | --- | --- |
| [`01-scope-source-question.md`](01-scope-source-question.md) | Bound the question and evidence need | Scope, exclusions, source lanes, freshness, decision |
| [`02-map-research-facets.md`](02-map-research-facets.md) | Split a broad question when necessary | Independent facets and search order |
| [`03-search-and-verify-sources.md`](03-search-and-verify-sources.md) | Discover, inspect, and rank sources | Verified source registry and extraction queue |
| [`04-extract-concepts-and-techniques.md`](04-extract-concepts-and-techniques.md) | Preserve source meaning and provenance | Traceable concepts, techniques, limits, disagreements |
| [`05-distill-source-packet.md`](05-distill-source-packet.md) | Prune and consolidate the evidence | Decision-ready source packet |

Use only the prompts the question needs. Prompt 02 is optional. This set stops
at evidence and never drafts, edits, validates, promotes, installs, or delivers
a runtime skill.

## Specialized Profiles

| Profile | Use | Output |
| --- | --- | --- |
| [`extract-skill-pack-vocabulary.md`](extract-skill-pack-vocabulary.md) | Apply Prompts 03-05 to language extraction across any skill pack | One refreshable, revision-pinned vocabulary packet |
