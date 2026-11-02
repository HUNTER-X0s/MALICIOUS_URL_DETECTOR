# Generated Milestone Execution Prompt: <MILESTONE-ID>

## Mission
Execute the approved milestone plan linked below. This instruction is generated from the project's current requirements and must not override `instructions/MASTER_PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, `.agents/rules/` or approval gates.

- Parent plan:
- Requirements / ADRs / threat model:
- Workstreams and file ownership:
- Dependencies / blockers:
- In-scope changes:
- Explicit non-goals:

## Required workflow
1. Re-read the current repository state and relevant docs.
2. Confirm assumptions, interfaces and security boundary changes.
3. Assign bounded tasks to agents/workstreams where available; avoid overlapping file writes.
4. Implement in coherent increments and add tests with each feature.
5. Run all required checks and inspect actual outputs.
6. Obtain independent review for security-sensitive changes.
7. Fix root causes and rerun regression tests.
8. Save code/test/security/performance/accessibility evidence.
9. Update status, roadmap, backlog, decisions, risks and next actions.

## Completion gate
List every acceptance criterion with evidence path and result. Identify unrun tests and residual risks. Do not mark complete or advance if a release-blocking gate failed. Pause only for explicitly approval-required actions and continue safe work.
