# Context Authority and Reading Order

1. `AGENTS.md` — workspace-level agent entry point.
2. `instructions/MASTER_CONTEXT_AND_EXECUTION_CHARTER.md` — complete project intent and operating model.
3. `instructions/MASTER_MISSION.md` — mission and mandatory outcomes.
4. `instructions/MASTER_PROJECT_INSTRUCTIONS.md` — detailed permanent engineering instructions.
5. `instructions/PROJECT_DESCRIPTION.md` — product description and scope.
6. `docs/00-overview/CONVERSATION_DECISIONS_AND_FULL_SCOPE.md` — all cross-cutting decisions from planning conversations.
7. `docs/01-product/COMPLETE_PRODUCT_BLUEPRINT_103.md` — full 103-section blueprint.
8. `docs/01-product/FEATURE_TRACEABILITY_103.md` — section-by-section disposition register.
9. `.agents/rules/` — applicable rules for security, research, code, tests, UX, performance, privacy, records, authority, extension and ML.
10. `.agents/skills/` — use relevant skills for each task.
11. `docs/` — detailed domain specifications and requirements seeds.
12. `plans/` and `project-state/` — current execution plan and persistent state.
13. `research/` and `records/` — cited evidence and engineering records.

If Antigravity cannot load any file through a built-in mechanism, it must still read the file as workspace content when directed, and record any tool-specific limitation. Do not assume a file is loaded merely because it exists. Verify actual behavior.
