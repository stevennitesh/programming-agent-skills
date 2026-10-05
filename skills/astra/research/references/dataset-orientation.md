# Dataset orientation

Read when understanding a dataset or checking whether its documented meaning
matches the available files. Reconcile three evidence sources: authoritative
documentation, the actual local artifacts, and observations computed from them.
Choose inspection methods and depth for the user's question; orientation does
not by itself require modeling, training, or an experiment.

## Establish what the available data represents

Identify the documented dataset version and the local release, subset, or
transformation being inspected. Determine which expected files or components are
present and which are missing or inaccessible when that affects the question.
Keep documentation claims distinct from facts established in the local data.

Establish the relevant row or event grain, identifiers, relationships between
files, label definitions, units, population, and time coverage. Use the question
to select checks such as key uniqueness, join cardinality, duplicates, missingness,
or class counts. A row count is not necessarily a count of independent entities
or events; distinguish these when interpreting coverage or suitability.

Do not infer a label's meaning solely from its name, numeric encoding, or apparent
correlation. Trace consequential definitions to their source and report missing
or ambiguous meaning. For quantitative claims, apply
[Quantitative evidence](quantitative.md) where units, denominators, timestamps,
or other measurement semantics affect interpretation.

## Bound the conclusions to the inspection

Make decisive observations traceable to the relevant files or version and the
query, calculation, or inspection that supports them. Distinguish complete checks
from samples, including the selection limits that matter. A clean sample cannot
establish absence of a problem throughout the dataset.

Explain discrepancies among documentation, artifacts, and observations without
silently choosing the most convenient account. Distinguish a demonstrated mismatch
from an unverified mapping or missing evidence. Keep inferred uses or hypotheses
separate from established properties; descriptive profiling alone does not
establish predictive value or evaluation validity.

Return an orientation that answers the requested question, with consequential
gaps and limits. Choose its format and level of detail. Preserve source data;
cleanup, relabeling, model development, and experiments require their own scope.
