# PPCP changelog

Current draft: 0.1.1. This repository distributes the same published specification and schemas as https://ppcp.jardenberg.net/.

### 0.1.1 — 2026-09-16
- Added freshness, version identity, complete catalog discovery and compatibility guidance.
- Distinguished source editions, HTTP caching, MCP freshness hints and host adoption.
- Documented optional catalog diagnostics and the limits of signatures and version-tool checks.
- No new required profile fields. Preserved the 0.1.0 specification and schema for existing documents.

### 0.1.0 — 2026-09-13
- Initial PPCP proposal, renamed and expanded from the Public Context Profile working concept.
- Static/download, discovery and read-only MCP bindings.
- Public/private separation with whole-person scope.
- Version, provenance, rights and receiving-agent authority distinctions.
- First reference profile at joakim.jardenberg.net.

## GitHub distribution

### 2026-09-16
- Initial public repository with drafts 0.1.0 and 0.1.1, versioned schemas, fictional examples, CC BY 4.0 licence, contribution guidance and automated validation.
- Specification and schema bytes match the published website. The deployed website and reference MCP remain separate applications.

## Diagnostic tooling

### Reference access probe 0.1.1 - 2026-09-17
- Added direct IPv4 UDP and TCP checks against every discovered authoritative nameserver, with raw responses and a separate hostname NS lookup. A failed or unavailable authoritative check fails the diagnostic run. Correctly labels the empty HTTP 202 MCP notification acknowledgement.

### Reference access probe 0.1.0 - 2026-09-17
- Added an on-demand GitHub-hosted DNS/HTTP/MCP probe for the public reference implementation. Client-specific blocking is reported explicitly, separately from successful named-client retrieval. It does not claim search indexing, actual crawler access, or cryptographic verification. No scheduled monitoring was created.
