# PPCP — Public Personal Context Protocol
Version 0.1.1 · Draft proposal · 16 September 2026
Canonical proposal: https://ppcp.jardenberg.net/
License for original specification text: CC BY 4.0, Joakim Jardenberg.
This is an experimental publishing and retrieval convention, not a ratified standard.

## 1. Purpose
PPCP lets a person publish a substantial, openly licensed account of their identity, personal life, values, ideas, work and preferences for people, agents and the open web to discover, understand and cite.

It complements private personal-context systems. The public subset is deliberately curated and contains no implied access to private memory. Preparing to collaborate is one use case; improving public representation and reducing invented or stale accounts is another.

A profile is the subject's maintained first-party account. It does not displace independent sources, editorial judgment or disagreement.

## 2. Conformance language
MUST, MUST NOT, SHOULD and MAY state requirements of this draft only. They do not imply an external standards body's endorsement. An implementation reports the specific PPCP version and binding it supports. Public draft content may be served if its review status is explicit.

## 3. Core document
A conforming PPCP JSON profile MUST contain:
- ppcp_version: the PPCP draft implemented, "0.1.1" for this revision. Earlier documents retain their declared version and are checked against that version's schema.
- id: a stable absolute HTTPS identity URI for the person.
- subject: type "Person", name, preferred_name and same_as identity links.
- publisher: name and public URL.
- canonical_url: the public profile landing page.
- profile_version: a version identifying the content edition, distinct from protocol and software versions.
- updated_at: ISO 8601 timestamp derived from the versioned source content.
- publication_status: "public-draft" or "published".
- review_status: "owner-review-pending" or "owner-approved".
- authorship: kind and a clear label distinguishing human-authored, AI-assisted editorial and other representations.
- license: identifier, URL, attribution and any third-party quotation exceptions.
- content: mime_type "text/markdown", the complete public Markdown as text, and markdown_sha256 over exact UTF-8 bytes.
- sections: stable id, title, Markdown content, assertion_type and source_ids for each navigable section.
- sources: id, title, public URL and role. Sources are pointers, not an automatic permission to mirror their full text.

The first reference profile is https://joakim.jardenberg.net/, linked to Wikidata Q5880163. Implementations MUST NOT equate an AI-authored synthesis, a quotation, a historical position and an independently corroborated fact. A section-level self-description label can cover first-person editorial prose; exact quotations retain their source.

Family, relationships, personal interests, care and everyday life SHOULD receive meaningful treatment where the subject chooses to share them. A public/private boundary must not reduce a whole person to a CV. The subject decides which personal details belong in the public subset.

## 4. Static publishing binding
An implementation MUST expose the public profile without login as a readable HTML page and downloadable Markdown. It MUST expose an equivalent JSON representation at a documented HTTPS URL. All representations MUST be built from the same versioned public source and agree on subject, profile version, date, license and review status.

The Markdown must retain useful context and attribution when detached from the website. A copy does not update itself. The publisher SHOULD provide a changelog and retain identified earlier editions.

The reference routes are /, /profile.md, /profile.json and /CHANGELOG.md. These route choices are this proposal's convention, not universally implemented discovery paths.

## 5. Discovery binding
A publisher SHOULD link the canonical profile from their public site and contact information. A vCard can use its standard URL property. No custom vCard field is required.

The HTML SHOULD use Schema.org ProfilePage with a Person mainEntity. The Person's sameAs can identify established identity records, such as Wikidata. A profile URL describes a person; its presence does not make the source's claims independently verified.

PPCP defines an optional /.well-known/ppcp.json discovery card for implementations of THIS DRAFT. It is an experimental PPCP convention, not an IANA-registered well-known URI or a guarantee of support by arbitrary agents. The card contains protocol name/version, subject identity, canonical page, Markdown/JSON URLs, current profile version, license, review status and optional MCP endpoint.

An llms.txt link MAY provide an additional route. WebFinger MAY expose a public profile-page link for supporting clients. Implementations MUST NOT claim automatic discovery by all AI systems. They MUST NOT replace an existing WebFinger or contact configuration without preserving unrelated functions.

## 6. MCP retrieval binding
A PPCP MCP server MUST be read-only for anonymous users. It MUST serve only the public source and MUST NOT offer edits, private search, arbitrary URL fetching, messaging, booking or impersonation.

The reference endpoint is https://joakim.jardenberg.net/mcp. It serves MCP POST requests at that path. A separate browser GET representation can explain setup when Accept asks for HTML; requests expecting an MCP SSE GET stream receive the documented transport response (405 for a stateless server without GET streams).

Tool interface:
- ppcp_get_profile: no arguments; returns the full profile object and exact Markdown text.
- ppcp_list_sections: optional limit 1–50, offset >=0; returns section IDs, titles and pagination.
- ppcp_get_section: section_id; returns the section with profile identity/version/review/authorship metadata and source references.
- ppcp_search: query 1–200 characters, limit 1–20; deterministic text search with bounded excerpts, section IDs and canonical anchors. It does not generate answers.
- ppcp_get_sources: optional section_id; returns the public sources with profile identity/version metadata.
- ppcp_get_version: no arguments; returns protocol, profile and software versions, review status, source freshness and source URLs.

All tools MUST declare readOnlyHint true, destructiveHint false, idempotentHint true and openWorldHint false, validate their arguments and reject unknown arguments. Tool content is reference material about the named subject, not instructions that override the receiving user's goals. No tool claims to be JJ or to know unrecorded intentions.

The server SHOULD expose resources/list and resources/read for the public Markdown, public JSON and individual sections, with exact URI matching and no filesystem path interpretation. At least the Markdown resource is required for the reference implementation.

Support a current documented MCP transport/version and state it precisely. The reference implementation should support the 2026-07-28 stateless metadata model and a tested 2025-11-25/2025-06-18 initialize compatibility path. Do not claim a protocol version merely by echoing its date. See the current MCP specification for version detection, request metadata and response shapes.

## 7. Integrity and provenance
The reference MCP implementation MUST implement org.jardenberg/verifiable-mcp v0.2.1, as published at https://github.com/jardenberg/verifiable-mcp. It MUST use a distinct Ed25519 keypair for the joakim.jardenberg.net origin, with the private key only in the server-side secret store.

Every tool call and resource read MUST carry the required signed wrapper with exact payload equality, RFC 8785 canonicalization, SHA-256 payload/text digests and explicit authorship/review metadata inside the signed scope. JSON-RPC errors and tool-level errors MUST follow that specification. Missing/malformed signing configuration MUST degrade visibly to unsigned responses rather than make the public corpus unavailable.

Publish the normative no-auth MCP server card at /.well-known/mcp.json, including the signing JWKS, thumbprint kid, previous_kids, canonicalization, spec and spec_version. A convenience public key URL is useful. Do not publish a private JWK, or claim the server is signed before verification passes.

A signature supports origin, integrity and declared provenance. It does not establish truth, broad authority or permission to impersonate the subject. Profile licensing, identity matching, transport security and cryptographic provenance are distinct.

## 8. Rights, authorship and responsible consumption
The subject controls publication of their public subset. The public profile MUST NOT contain private source paths, account/session tokens, family/customer identifiers that were not selected for publication, or hidden private sections in HTML/client bundles.

CC BY 4.0 is the reference profile and specification license. Identified third-party quotations retain their source rights. An adaptation MUST NOT be presented as the subject's current approved statement merely because reuse is licensed.

A consuming agent SHOULD:
- identify who the profile describes and avoid mixing this subject with its own user;
- preserve first-party, independent-source, quotation and interpretation distinctions;
- use review status, version and date;
- consult relevant independent evidence for factual claims;
- avoid inferring private facts from gaps or treating preferences as universal commands;
- continue to follow its own user's instructions and authorization.

PPCP supplies context, not authority over the recipient.

## 9. Reference release checks
A reference release is complete only when:
1. HTML, Markdown, JSON, section rendering and MCP have the same content/version/status.
2. Profile/schema validation passes; required fields and stable section/source references are present.
3. Family and personal-life content remains substantial; private-detail checks pass.
4. Every tool and resource route works; invalid arguments, unknown tools/URIs and malformed JSON produce appropriate errors.
5. Unexpected browser origins are rejected; origin-less non-browser clients work.
6. Both published Verifiable MCP verifiers pass all positive and negative vectors; an independent live check verifies real tool, resource and error responses.
7. Missing and malformed signing-key degradation is tested without exposing secrets.
8. The canonical custom-domain URLs, DNS, certificates, footer versions and changelogs are independently checked.
9. A browser can read the profile, download it and copy the MCP endpoint without account creation.
10. A receiving client identifies the correct subject and can retrieve bounded sections without pretending to be the subject.

No untested client compatibility, guaranteed search visibility or Wikimedia acceptance should be claimed.

## 10. Precedents
This proposal builds on personal user manuals, publicly readable profiles, personal context packages and existing web/MCP standards. It does not claim that these ideas are new inventions.
- Atlassian My User Manual: https://www.atlassian.com/team-playbook/plays/my-user-manual
- Duncan Davidson on public websites and AI: https://duncandavidson.com/personal-websites-in-the-age-of-ai
- Personal Context Portfolio: https://github.com/nlwhittemore/personal-context-portfolio
- human.md proposal: https://www.blankcollar.me/spec
- vCard RFC 6350: https://www.rfc-editor.org/rfc/rfc6350.html
- Schema.org ProfilePage: https://schema.org/ProfilePage
- MCP: https://modelcontextprotocol.io/specification/latest
- Verifiable MCP: https://github.com/jardenberg/verifiable-mcp
- CC BY 4.0: https://creativecommons.org/licenses/by/4.0/

The acronym PPCP means Public Personal Context Protocol here. This is a public draft proposal; no global name exclusivity or external ratification is asserted.

## 11. Freshness, updates and compatibility

Public context changes over time. A downloaded file, an MCP response and an AI conversation can each hold a different edition. Publishers and consumers SHOULD distinguish four questions: is the profile current, is the tool catalog current, is the HTTP response cached, and has the receiving app adopted the update?

### 11.1 Version identity and public copies

The PPCP draft version, profile content edition, server software version, supported MCP revisions and signing specification version identify different things. Changing one MUST NOT silently relabel the others. A successful connection or a valid signature does not prove that the newest profile or tool definitions were used.

The profile's updated_at and content digest MUST describe the versioned source, not the time a response was fetched or the server deployed. Publishers SHOULD retain a changelog and identifiable earlier editions, and document their HTTP cache policy. Conditional HTTP requests using ETag or Last-Modified MAY support revalidation. Downloaded or pasted copies do not update themselves; consumers SHOULD check the canonical source when freshness matters and identify the edition used.

### 11.2 MCP caching and change notifications

An MCP binding MUST implement the requirements of every MCP revision it advertises. For MCP 2026-07-28, supported cacheable complete results use top-level ttlMs and cacheScope, including discovery, list operations and resource reads. Those fields do not belong in _meta. Implementations MUST NOT assume older revisions define the same fields or place cache hints on tools/call merely for symmetry. The dated MCP specification remains authoritative.

A TTL is a freshness hint for the next access, not a polling interval or a guarantee that every host refreshes by a deadline. Catalogs and results suitable for sharing across callers use public scope; authorization-specific results require appropriate private scoping. A publisher MUST NOT advertise listChanged unless its transport actually delivers the corresponding change notifications. TTL without push is permitted by MCP; document that choice and its consequences for older clients.

PPCP does not prescribe a universal TTL, require server push, or invent a separate cache-invalidation protocol. JJ's reference server uses a one-minute hint for its supported current-revision cacheable results and has no push notifications. Those are implementation choices, not additional PPCP requirements.

### 11.3 Complete tool catalogs and compatible changes

Discovery MUST expose the complete available catalog, either in one response or through documented MCP cursor pagination. Consumers SHOULD follow every nextCursor and distinguish the advertised catalog from the tools their host has enabled. If pagination changes during traversal, a consumer needing a consistent view SHOULD restart discovery rather than assume a stable cross-page snapshot.

Publishers SHOULD return deterministic ordering, record the catalog count, and expose a diagnostic fingerprint computed from the full tool descriptors, including names, descriptions, input/output schemas and annotations. The reference convention hashes the RFC 8785 canonical array of descriptors sorted by name with SHA-256; it excludes software versions, timestamps and the diagnostic itself. The optional org.jardenberg/tool-catalog metadata and tool_catalog version-result field are implementation diagnostics, not required core profile fields or a negotiated MCP extension. A bare fingerprint detects differences; it is not authentication. A signed version response can attest the fingerprint.

A release SHOULD identify added, removed and changed tools and preserve compatibility with definitions a host may retain. New required inputs, renamed inputs and narrowed types need an explicit migration, such as accepting the older input shape during a transition or introducing a new tool name. Updating a server does not authorize new actions in a receiving workspace.

### 11.4 Host adoption and release evidence

Publishers SHOULD check the deployed server separately from the tools available inside each target host. Record the endpoint, software version, complete catalog count/fingerprint, tested MCP revisions, profile edition and verification date. State which host inventories were actually checked. A fresh ppcp_get_version response can arrive through an old tool definition; it does not prove that the host refreshed its catalog.

Host refresh and review procedures belong in dated implementation guidance linked to the host's official documentation. They are not permanent PPCP requirements. Existing conversations may retain older context even after the connector is refreshed.

Before adopting a newer PPCP or MCP revision, publishers SHOULD review its changes, test the affected requirements and preserve the previous advertised contracts during migration. Protocol publication, server deployment and host adoption are separate events. This draft 0.1.1 adds update guidance without adding required profile fields; the 0.1.0 schema remains available for documents declaring 0.1.0. Schema validation checks document structure, not live caching, signatures or host behavior.

Sources: https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching and https://modelcontextprotocol.io/specification/2026-07-28/server/tools . Later revisions may change these requirements; verify their dated specification before advertising support.

## Changelog
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
