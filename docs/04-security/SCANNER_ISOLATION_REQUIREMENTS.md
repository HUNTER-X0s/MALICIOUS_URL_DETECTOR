# Isolated scanner security requirements

The deep scanner is a separate high-risk product capability. It must not be implemented in the public API or ordinary worker process before the isolation design is approved and tested.

Required design review:
- Threat model and trust-zone diagram.
- Disposable worker lifecycle and clean teardown.
- VM/microVM or other isolation choice justified against threat and budget; containers alone are not automatically a sufficient boundary for hostile browser content.
- Default-deny network egress enforced outside the guest; explicit proxy/egress gateway; DNS control; block internal, loopback, private, link-local, reserved and metadata endpoints.
- Destination validation at DNS and socket-connect time; redirect-by-redirect validation; IP pinning or equivalent rebinding defenses.
- CPU, RAM, process, disk, bandwidth, file count, response bytes, navigation count and wall-time limits.
- No production secrets, host mounts, Docker socket, privileged mode or long-lived credentials.
- Browser sandbox, patched runtime, disabled downloads unless safe pipeline; no user data/cookies.
- Artifact quarantine, malware-safe handling and retention policy.
- Kill switch, fleet isolation, audit events, image provenance, patch SLA and escape-response exercise.

Release blockers: any route to metadata/internal network, host filesystem, privileged API, shared credential, uncontrolled egress, persistent artifact execution or missing teardown verification.
