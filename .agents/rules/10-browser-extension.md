---
trigger: model_decision
description: "Apply these rules when designing, implementing, testing, packaging or publishing browser extensions for Chromium, Edge or Firefox."
---

# Browser extension security

- Prefer Manifest V3 where appropriate; verify current Chrome/Edge/Firefox requirements.
- Request only implemented, necessary permissions; optional permissions where feasible.
- No remotely hosted executable code, eval or remote command interpreter.
- Minimize host permissions, page access, storage and telemetry; validate messages.
- Test browser-specific APIs, store policy, update integrity and failure modes separately.
