# Recordkeeping standard

All durable engineering work must live in the repository, not only in agent chat. Use dated/versioned Markdown/JSON/CSV/diagrams as appropriate. Include owner/agent, status, scope, source links, assumptions, commands, evidence and decisions. Store large binary outputs only when useful; avoid customer/private URLs and secret-bearing artifacts.

Required record types: product briefs, SRS, architecture diagrams, ADRs, threat models, implementation specifications, milestone plans, agent task prompts, research reports, competitor matrices, experiment cards, test plans/results, security findings, performance/accessibility reports, release notes, runbooks, incident reports, postmortems, privacy reviews and approvals.

Update project-state files after every substantial milestone. Index all records. Keep obsolete documents with superseded status rather than silently deleting their decision history. Never commit API keys, credentials, production exports, customer data or raw malicious payloads.
