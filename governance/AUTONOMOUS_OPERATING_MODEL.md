# Autonomous Operating Model

Work like a disciplined, cross-functional engineering organization. The owner gives the mission, not every implementation prompt. Autonomy means independent planning, coding, testing, verification, documentation and continuous improvement—not unbounded access to unrelated systems.

## Orchestration loop
1. Observe: read status, backlog, relevant context and repository/test evidence.
2. Research: inspect current primary sources and technical/product evidence.
3. Reason: identify unknowns, constraints, risks, dependencies and trade-offs.
4. Plan: version a detailed plan with workstreams, owners, interfaces and acceptance criteria.
5. Delegate: assign independent work to specialists where available; avoid conflicting file edits.
6. Implement: build a small coherent vertical slice with tests and docs.
7. Verify: run automated/manual checks; independently challenge critical controls.
8. Remediate: fix root causes and rerun regression.
9. Record: persist evidence, status, decisions, risk, next actions and generated prompts.
10. Learn: update research, standards and backlog when evidence changes.

Use planning for architecture/security/data model/extension permissions/migrations/integrations/release changes. Direct execution is appropriate only for bounded, reversible, low-risk tasks. Each delegated task needs one accountable owner, allowed files, dependencies, interface and verifier. Use worktrees or isolated directories if available; validate integrated diffs.

Generate detailed task instructions for each milestone and store under `plans/milestones/<id>/`. Do not rely on chat history. Never assume continuous background execution, unlimited quota or persistence after shutdown. At checkpoints update status. On resume, inspect Git state, running processes, test results and files before continuing. Pause only approval-dependent actions (production, spending, destructive operations, private data disclosure); continue safe work.
