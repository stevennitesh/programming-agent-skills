# Private-Source Evidence

Load this branch when a source, query, or requested output includes non-public,
sensitive, credentialed, or audience-restricted information. Otherwise do not
load it.

Keep external source systems read-only. Put only public information or
caller-approved search terms in public queries. Retrieve private or sensitive
evidence only through authorized private channels and use it only within the
defined audience, destination, and tool authority. Keep private and public
provenance separate. If separation fails, keep the dependent claim `unknown`
and return the access boundary.

Read-only local inspection, tool-managed temporary retrieval, and the one
authorized note mutation remain permitted under the common authority rules.
