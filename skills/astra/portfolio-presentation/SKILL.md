---
name: portfolio-presentation
description: Present demonstrated project work for first-time visitors, hiring managers, and external reviewers. Exclude isolated wording edits, new research, and generic site building.
---

# Portfolio presentation

Present the problem, the author's contribution, consequential decisions, and
demonstrated results through a coherent reading path for an outside audience.
Choose narrative, visuals, tools, and detail for the requested surfaces; no fixed
template or new website is required. Use only when requested.

An audit alone returns findings. Authorized edits use existing artifact owners
and publishing conventions. Presentation alone grants no authority to publish,
run new experiments, or change scientific meaning.

## Establish the story the evidence supports

Inspect actual implementation, maintained results, and accepted requirements,
distinguishing demonstrated work from plans. Use the requested audience, purpose,
and deliverables; settle only consequential gaps the context cannot answer and
choose ordinary editorial details directly.

Explain the problem or learning objective, what the author built/investigated,
why key choices matter, and what the evidence shows. Attribute contribution
separately from dependencies, datasets, and inherited work. Include consequential
tradeoffs and negative findings; invent no business impact, deployment experience,
or independent validation.

Separate measurements, interpretation, and proposed applications. Preserve
evaluation boundaries, label proxies/synthetic demonstrations, and attach material
limits to their claims. Expose methodological defects to the analysis/engineering
owner rather than concealing them or silently changing the analysis.

For data-analysis work, explain what the data represent and consequential source,
sampling, and preparation choices. Distinguish descriptive/exploratory findings
from unseen-case or causal claims. Retain existing uncertainty; negative or
inconclusive results can be credible. Use the existing analysis without requiring
new statistical tests or reopening evaluation.

For decision-relevant findings, explain the user, supported choice, and material
uncertainty or constraints. Recommendations stay conditional on evidence; model
performance alone does not establish outcomes from acting on predictions.

## Write for the intended reader

Assume the reader is new to the project. In the opening, explain the problem,
what the author built or investigated, and what works or what the evidence
shows. Link directly to the clearest demo, figure, or result. Make the main
claim understandable before asking readers to install tools or read code.

Use plain explanations and precise domain terms that help the reader understand
the work. Define local names and unfamiliar abbreviations at first use. Explain
important metrics through the question they answer, the population they describe,
and the inference they support. Use clear sentences, active verbs, and consistent
terms informed by [ASD-STE100](https://www.asd-ste100.org/about_STE.html).

Give readers a path from the opening to the detail they need. A hiring manager
should be able to find the author's scope, a consequential decision or tradeoff,
and evidence of the result. A curious visitor can start with the clearest
example or finding. Put material limits next to the claims they qualify and link
to supporting methods or implementation where useful.

Apply pstack's [Unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md)
intent directly: concrete actions, constraints, tradeoffs, and observed results
instead of generic flourish. Cut inflated claims, vague attributions, stock
transitions, rhetorical contrasts, forced groupings, decorative emphasis, and
compressed fragments. Let structure follow the content; invent no personal
experience or emotion. No separate editing workflow is required.

## Make the requested artifacts agree

Keep a focused README pass on the entry page and the evidence it relies on.
When the story spans multiple artifacts or a material claim needs reconciliation,
compare the relevant surfaces. Keep claims, numbers, terminology, and status
consistent across in-scope READMEs, reports, charts, resume material, or websites
while preserving each artifact's purpose.

Trace decisive numbers/visuals to current sources, reconciling units, labels,
denominators, cohorts, time windows, baselines, and evaluation stage. Investigate
disagreement at its producing data/calculation within existing authority; return
needed analysis changes to that owner or expose the unresolved discrepancy.
Do not copy a preferred number everywhere or relabel a different underlying
quantity to make artifacts agree.

Use visuals that support assessment, with interpretable labels, comparisons,
and explanations. Axes, scales, and emphasis must preserve meaning. Supply useful
text alternatives and cues beyond colour for consequential distinctions. Prefer
existing evidence-generation paths; renderer changes do not authorize model
retuning or reopening held-out evaluation for a better story.

Offer available examples, outputs, or execution instructions for inspecting the
work. Distinguish inspected, executed, and independently reproduced evidence;
expose missing reproducibility rather than substituting unrelated demos or
infrastructure. Exclude private inputs and credentials from public artifacts.

For GitHub-hosted data science presentations, read
[GitHub data science artifacts](references/github-data-science.md) for notebook
viewer constraints and access to the supporting evidence.

## Verify the reader's experience

Start at the rendered entry page with the access an intended reader has. Check
whether a first-time visitor can find the problem, author contribution, main
result, and its material limits. Follow the main evidence link and verify that
the destination supports the claim. For a focused README pass, this check and
the affected layout may be enough. When the presentation spans artifacts, check
the relevant rendered surfaces, chart/text agreement, links, and legibility at
the presentation sizes that matter. Use reader feedback when useful. Fix
presentation defects in scope and identify surfaces whose rendering or access
could not be checked.

Deliver the artifacts, material changes, checked surfaces, and evidence/rendering
limits. Broader research, product work, and publication retain their own authority.
