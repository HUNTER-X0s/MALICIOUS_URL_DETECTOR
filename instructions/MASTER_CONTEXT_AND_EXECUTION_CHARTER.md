# URLSentinel Master Context and Execution Charter

This file is the single entry point that consolidates the project owner's full intent. Read it alongside `MASTER_MISSION.md`, `MASTER_PROJECT_INSTRUCTIONS.md`, `PROJECT_DESCRIPTION.md`, `AGENTS.md`, all applicable `.agents/rules/`, and the complete 103-section product blueprint.

## Authoritative source order
1. This charter and `docs/00-overview/CONVERSATION_DECISIONS_AND_FULL_SCOPE.md` capture the overall intent agreed with the owner.
2. `docs/01-product/COMPLETE_PRODUCT_BLUEPRINT_103.md` preserves the complete 103-section blueprint.
3. `docs/01-product/FEATURE_TRACEABILITY_103.md` records section-by-section disposition and mapping.
4. Security, privacy, abuse-prevention and release rules constrain how features may be implemented.
5. Current, cited research and verified runtime constraints determine technical choices.
6. Generated plans and ADRs explain implementation decisions and changes over time.

If sources conflict, do not silently discard content. Record the conflict, source, security/product implications and proposed resolution in `project-state/DECISIONS.md` or a formal ADR. Preserve original scope while making explicit decisions about priority and release.

## The mission in one paragraph
Build URLSentinel from a clean codebase into a production-grade cybersecurity startup platform with a distinctive and trustworthy website, browser extension, detection and threat-intelligence systems, APIs, and staged enterprise/operational capabilities. Act as an autonomous, cross-functional engineering organization: research broadly, identify gaps, generate detailed plans, implement, test, secure, debug, document and improve. The owner should not have to manually issue every phase prompt. Keep all work and project knowledge persistent. Security and truthful user trust outrank speed, feature count or visual spectacle.

## Required first deliverables
Before broad application coding, produce and save:
- Workspace and instruction inventory, including missing/duplicate/conflicting material.
- Current Antigravity capability/permission matrix verified against official docs and this installed environment.
- Global research report and competitor/capability comparison.
- All-103-section assessment with disposition, evidence, dependencies, risk and acceptance criteria.
- Formal requirements/SRS and requirement-to-test traceability.
- Personas, user journeys and abuse/misuse cases.
- UI/UX competitive research, concept exploration, design direction and responsive/accessibility test plan.
- System context, trust boundaries, data-flow diagrams, architecture options and ADRs.
- Threat model, scanner isolation design and abuse-prevention model.
- Detection taxonomy, verdict contract, data/source governance and evaluation methodology.
- Privacy/legal/licensing/provider cost review.
- CI/CD, deployment, observability, recovery and startup operations plan.
- Measurable quality budgets and a dependency-aware roadmap.
- Generated milestone plans, focused task instructions, agent/workstream assignments and quality gates.

## Execution loop
For each milestone:
1. Refresh relevant context and current status.
2. Research unknowns and cite material findings.
3. Update the plan, dependencies, acceptance criteria and risks.
4. Divide work into bounded tasks with clear ownership and interfaces.
5. Implement on a branch/worktree when supported; avoid concurrent conflicting edits.
6. Run relevant tests and inspect actual output.
7. Run independent review for security-sensitive or high-impact changes.
8. Fix root causes and rerun tests, including regression.
9. Record evidence, known limitations and deviations.
10. Update status, decisions, backlog, risk register and next actions.
11. Advance only when quality gates pass or a documented, approved exception exists.

## What not to do
- Do not start with a decorative frontend and invent backend behavior later.
- Do not treat the 103 sections as 103 equally sized V1 features or silently omit them.
- Do not blindly implement every technology or idea found online.
- Do not claim a security scan, test, benchmark, review or deployment happened unless it did.
- Do not expose secrets, bypass safeguards or deploy to production without authorization.
- Do not fetch arbitrary user URLs from the main API without a proven isolated boundary.
- Do not classify unknown evidence as safe.
- Do not rely on transient chat context for decisions or project state.
- Do not guarantee perfect detection, zero vulnerabilities, top search rankings or unlimited autonomous operation.

## Owner interaction policy
Prefer autonomous progress. Ask the owner only when a decision genuinely requires owner preference, legal authority, credentials, spending, production impact, destructive action, sensitive data sharing or a major product trade-off that cannot be resolved from the documented principles. When waiting for approval, continue unrelated safe work and present a concise decision brief with options and consequences.
