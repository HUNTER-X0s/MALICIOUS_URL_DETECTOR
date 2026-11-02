# URLSentinel Directory Map

```text
URLSentinel/
├── AGENTS.md                    # Always-on Antigravity workspace instructions
├── instructions/                # Master mission, instructions, project description, setup/context
├── governance/                  # Engineering organization, SDLC, autonomy and authority
├── project-state/               # Persistent status, milestone, backlog, decisions, risks and indexes
├── .agents/
│   ├── rules/                   # 12 modular rules with required YAML triggers
│   └── skills/                  # 19 reusable skills, each with SKILL.md metadata
├── docs/                        # 15 subject areas of product/technical knowledge
├── plans/                       # Roadmap, milestone specs, generated task prompts and templates
├── research/                    # Dated research and source cards
├── records/                     # Decisions, tests, security findings, approvals, incidents and releases
├── apps/                        # Web, extension and admin product surfaces
├── services/                    # API, detection, feed ingestion and isolated scanner candidates
├── packages/                    # Shared contracts, utilities and UI packages
├── infra/                       # Development, staging and production infrastructure candidates
├── tests/                       # Unit, integration, E2E, security, accessibility and performance suites
└── data/                        # Synthetic fixtures and schemas only
```

## Grouping policy
- Keep only workspace entrypoints and package metadata at the root.
- Keep related knowledge together; do not scatter specialist documents across the root.
- `.agents/rules/` must remain flat for reliable automatic discovery; each rule requires valid YAML frontmatter.
- `.agents/skills/<skill>/SKILL.md` is the supported skill bundle shape.
- Preserve every generated plan, focused agent prompt, implementation specification, source assessment, test result, security finding and release decision in this repository and link it from an index.
- `docs/` is curated reference knowledge; `plans/` and `records/` are durable execution history.

`PACKAGE_VALIDATION_REPORT.md` records structural, metadata and archive validation results.
