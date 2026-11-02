# Google Antigravity Setup and Operating Notes

1. Extract to a stable dedicated path such as `Z:\URLSentinel` or `C:\Projects\URLSentinel`.
2. Open this folder itself as the Antigravity workspace root.
3. Confirm root `AGENTS.md`, `.agents/rules/` and `.agents/skills/` are discovered in the installed product's Customizations/Rules/Skills view.
4. Official Antigravity docs currently describe workspace/directory rules via `AGENTS.md` and `.agents/rules/*.md`, and reusable skills via `.agents/skills/<skill>/SKILL.md`. Verify the exact behaviour in your current version.
5. Use Planning Mode for initial discovery and cross-cutting design; fast mode only for small low-risk edits.
6. Use `/browser` to test running web pages where available. Use `/teamwork-preview` for complex parallel campaigns only if supported by your surface/plan. Otherwise use available agents or explicitly managed sequential workstreams. Verify command availability in current docs.
7. Configure workspace/tool permissions according to `governance/SECURITY_AUTHORITY_MODEL.md`; do not enable blanket machine-wide access.

## Required Antigravity metadata (do not omit)
- Every immediate `.agents/rules/*.md` file must begin with YAML frontmatter containing a valid `trigger` value: `always_on`, `model_decision`, `glob` or `manual`. `model_decision` rules also require a concise `description`; `glob` rules require `globs`. Missing or invalid metadata can cause Antigravity to silently ignore a rule.
- Every `.agents/skills/<skill>/SKILL.md` must begin with YAML frontmatter containing a useful `description`; include a unique lowercase hyphenated `name` as well.
- This package was checked against the official Antigravity Rules and Agent Skills documentation on 2026-10-31. Recheck the installed version because support and surfaces can change.
- The workspace uses 12 `model_decision` rules for progressive disclosure. The root `AGENTS.md` contains short always-on invariants.

Official references: https://antigravity.google/docs/rules/ and https://antigravity.google/docs/skills

## Rules vs skills
Rules express persistent invariants (security first, no secrets, unknown is not safe). Skills express repeatable procedures (research, threat modelling, scanner review, UX audit, testing, security audit and release). `docs/` holds detailed reference knowledge.

## Agent team
Use an orchestrator and focused Product/Research, Architecture, UI/Client, Backend/Data, Detection/ML, Security, QA/Independent Audit and Platform/SRE workstreams. Define file ownership and interfaces; do not allow parallel edits to the same files. The orchestrator owns shared contracts and integration.

## Persistence
Antigravity plans, browser screenshots, code diffs and chat artifacts are not the only project record. Save final versions under this repository. Maintain status and next actions for session continuity.

## Model, quota and continuity
Use the strongest suitable reasoning model for security/architecture and efficient models for bounded routine work. Do not assume unlimited usage, indefinite unattended execution or uninterrupted sessions. Resume by inspecting Git state, `project-state/PROJECT_STATUS.md`, `project-state/CURRENT_MILESTONE.md`, `project-state/NEXT_ACTIONS.md` and the active plan.

## First prompt
Open a new Planning Mode conversation and paste `instructions/MASTER_MISSION.md`. The first campaign is inventory, research, requirements, security boundaries, architecture options and roadmap—not immediate full-platform coding.
