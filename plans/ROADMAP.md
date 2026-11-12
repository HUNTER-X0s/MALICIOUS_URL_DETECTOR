# Roadmap Overview

**Updated:** 2026-11-03  
**Detail:** See `plans/M0-IMPLEMENTATION-ROADMAP.md` for full milestone specifications

| # | Milestone | Status | Gate |
|---|---|---|---|
| M0 | Workspace Intake & Planning Baseline | IN PROGRESS | — |
| M1 | Requirements, Personas & Research | NOT STARTED | Owner review of M0; owner decisions on ADRs |
| M2 | Architecture, Contracts & Threat Model | NOT STARTED | M1 complete; provider licensing confirmed |
| M3 | Secure Foundation & CI | NOT STARTED | M2 ADRs approved; deployment target chosen |
| M4 | URL Parsing, Lexical Detection & Verdict Core | NOT STARTED | M3 foundation + SSRF guard tested |
| M5 | Threat Intelligence Integration | NOT STARTED | M4 complete; legal license confirmation per provider |
| M6 | Domain, DNS & TLS Intelligence | NOT STARTED | M5 complete; DNS security gate |
| M7 | Web MVP & Browser Extension MVP | NOT STARTED | M6 complete; UX direction approved (M1) |
| M8 | Advanced Detection & ML | NOT STARTED | M7 stable; labeled dataset; MLOps infrastructure |
| M9 | Isolated Deep Scanner | NOT STARTED | M8 stable; **independent security sign-off on scanner** |
| M10 | Auth, API Productization & Community | NOT STARTED | M7 stable; API contract stable |
| M11 | Enterprise Capabilities | NOT STARTED | M10 complete; customer demand validated |
| M12 | Production Hardening & Controlled Launch | NOT STARTED | All prior complete; external security assessment |

## Key architectural decisions pending

See `project-state/DECISIONS.md` for full decision briefs.

1. ADR-001: Backend language (Python vs TypeScript) — owner input or M2 decision
2. ADR-003: Deployment target — **owner input required before M3**
3. ADR-008: Blockchain vs tamper-evident log — **owner input required**
4. Provider licensing — **legal review required before M5**
