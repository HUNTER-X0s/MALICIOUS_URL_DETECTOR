---
name: isolated-scanner
description: Build and verify isolated, controlled URL and webpage scanning infrastructure.
---

# Isolated scanner

Do not implement active fetch in the public API process. Define a separate trust zone with disposable workers, strong OS/container/VM isolation as justified, default-deny egress, controlled DNS, no cloud metadata reachability, strict protocol/port allowlists, connection and redirect validation, CPU/memory/time/output caps, browser sandboxing, ephemeral credentials and artifact quarantine. Verify destination IP at resolution and connection time; defend against DNS rebinding and redirects. Never mount host sockets/secrets or production credentials. Do not execute downloads. Use synthetic test targets and controlled lab infrastructure. Scanner escape or egress violation blocks release.
