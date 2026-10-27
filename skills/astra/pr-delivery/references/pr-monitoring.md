# PR monitoring

Read when requested follow-through requires waiting on CI, hosted review, or
merge state. Monitor the identified PR and requested conditions through available
host, connector, API, or CLI capabilities. Do not create a watcher implementation
as part of routine delivery.

Assign one monitoring owner for a PR. Reuse a supported existing watch rather
than starting duplicate monitors. A delegated reviewer does not acquire the
parent's delivery or monitoring ownership. Preserve enough target and resource
identity to resume safely after interruption.

Handle already-present actionable state before waiting. Prefer an event-driven
host watch when available; otherwise use an existing bounded wait or status
facility appropriate to the available tools. If only status reads exist, space
them according to expected progress and rate limits. Do not start tight polling
or overlapping waits. Keep unchanged, non-actionable states quiet.

A wake or successful watcher exit is a signal to refresh the PR and reassess its
candidate and gates under the main skill. Resume against a moved head; include
relevant base changes even without line conflicts. Repository policy and requested
reviews determine gates, not fixed bot names. An old comment can still identify
an unfixed issue after a push; an inaccessible review remains unavailable.

For rate-limit, access, or transport failures, distinguish unavailable evidence
from failed code. Honor exposed retry/reset timing and use a supported alternate
API only when it supplies the needed coverage and identity. A different API has
no guaranteed independent quota. Retry within scope without manufacturing a
green result from missing checks or partial thread retrieval.

When handing off, stopping for a blocker, or reaching the endpoint, release any
watch resources owned by this run through their lifecycle owner and verify the
result where supported. A recurring automation is a separately requested effect;
do not create one merely to continue routine PR delivery. Report material resource
or access limits once, with a usable continuation state.
