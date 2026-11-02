---
trigger: model_decision
description: "Apply these architecture, design, maintainability and coding requirements when planning or changing project structure, interfaces, schemas or implementation."
---

# Architecture and code quality

- Plan cross-cutting changes; define interfaces and acceptance criteria.
- Prefer simplest architecture that meets security/isolation/scale/reliability needs. No complexity for prestige.
- Keep shared API/verdict contracts canonical and versioned.
- Use typed boundaries, schema validation, parameterized access, safe errors and explicit timeouts.
- Add tests with features; document material trade-offs in ADRs.
