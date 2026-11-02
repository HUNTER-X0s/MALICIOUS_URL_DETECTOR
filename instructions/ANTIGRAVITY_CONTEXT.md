# URLSentinel Antigravity Context Index

This file explains how to use the workspace knowledge system. It is not a substitute for `instructions/MASTER_PROJECT_INSTRUCTIONS.md`, `AGENTS.md` or the detailed documents.

## Instruction hierarchy
1. Applicable law, platform policies and tool permissions.
2. `governance/SECURITY_AUTHORITY_MODEL.md` and safety/approval boundaries.
3. `instructions/MASTER_PROJECT_INSTRUCTIONS.md` and root `AGENTS.md`.
4. Relevant `.agents/rules/*.md` workspace constraints.
5. The active milestone plan and accepted ADRs.
6. Relevant `.agents/skills/*/SKILL.md` procedures.
7. `docs/` reference knowledge and external sources.

If documents conflict, do not silently choose. Record the conflict, use the safer temporary interpretation, and propose an ADR/change record for the owner where the conflict changes scope or risk.

## What to load for each task
- Product/roadmap: `instructions/PROJECT_DESCRIPTION.md`, `docs/00-overview/`, `docs/01-product/`, backlog and active plan.
- Research: `docs/02-research/`, `project-state/RESEARCH_INDEX.md`, research skills and source terms.
- Architecture: `docs/03-architecture/`, threat-model docs and accepted ADRs.
- URL detection: `docs/04-security/`, `docs/05-detection/`, source governance and evaluation.
- Extension: `docs/06-extension/`, browser-compatibility matrix, security rules.
- UI/UX: `docs/07-ux/`, accessibility and performance docs, trust-UX skill.
- QA/release: `docs/08-quality/`, `docs/09-operations/`, release templates and quality gates.
- Privacy/startup: `docs/10-governance/`, `docs/11-startup/`, approval records.

## Persistent outputs
- `plans/`: active roadmap, milestone specifications and generated focused agent prompts.
- `research/`: dated research and source cards.
- `records/`: authoritative decisions, tests, security findings, releases, incidents and approvals.
- Project-state files: project state, current milestone, next actions, risks, decisions, backlog and research index.

Every agent must save its important output, not merely describe it in a chat. Each rule file requires valid YAML trigger frontmatter; each skill file requires YAML description metadata. The orchestrator is responsible for updating indexes and resolving contradictory records.
