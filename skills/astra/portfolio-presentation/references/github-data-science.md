# GitHub data science artifacts

Use when GitHub is a requested presentation surface for data science work,
including READMEs, notebooks, and linked results. Choose the inspection path for
the intended reader and the project's existing artifacts.

Make the main finding and its consequential qualification understandable before
local environment setup. An existing README explanation, saved notebook output,
static figure, or report may provide that first inspection. Link to the relevant
analysis and execution instructions for readers who want to investigate further;
the appropriate combination depends on the work being presented.

[GitHub renders Jupyter notebooks as static HTML](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files).
Custom JavaScript interactions do not work in that viewer. Check whether saved
outputs retain the evidence the summary relies on. When an essential result
depends on an interaction, use an existing static output, provide a suitable
export within scope, or link to an accessible renderer. State any essential
evidence that remains unavailable; a notebook that works locally does not
establish that GitHub displays it correctly.

Give evidence links a useful destination and explain their role: a result report,
analysis notebook, data provenance, or implementation can support different
claims. Prefer the relevant artifact or section when linking only to the
repository root would leave the reader to search for the evidence.

Check essential links with the access available to the intended reader. For a
public portfolio, author-session credentials should not be necessary to inspect
the main result. If a linked output requires an account or proprietary viewer,
offer an available alternative suitable for public sharing or make the access
limit visible.
Preserve distinctions between inspecting saved outputs and reproducing the
analysis; use the requested publishing scope for any external changes.
