---
name: architecture-review
description: Design or review secure, reliable, scalable architecture without premature complexity.
---

# Architecture review

Inspect current code and constraints first. Define system context, trust boundaries, data flows, failure modes, deployment topology, interfaces, data lifecycle, capacity and cost assumptions. Compare at least two plausible options for material decisions. Prefer modular monolith initially unless evidence supports service separation. Isolate active URL fetching from the public API. Produce diagrams, ADRs, threat model deltas and migration/testing plans. Save under `records/architecture/`.
