# Contributing to PPCP

Open an issue for a question, interoperability problem or proposed change. Include the profile/protocol version and a small public or fictional example. Pull requests are welcome for clearer wording, examples, schemas and implementation guidance. Contributions are made under the repository's CC BY 4.0 licence; preserve attribution for material you adapt.

Explain the problem and the behavior your change would produce. Distinguish requirements for all implementations from a choice made by one reference server. Source technical claims to a dated primary specification. Describe which claims were tested and where.

Keep personal life and family within the scope of the proposal while respecting what a person chooses to publish. Use fictional examples for diagnostics. Do not include private source documents, customer details, access tokens or material that was not selected for public release.

## Changes and releases

1. Published files under `spec/` and `schema/` are immutable. Propose a new draft in a new versioned file; preserve old schema URLs and their original constraints. The same rule applies to versioned examples and release tags.
2. Keep protocol version, profile edition, implementation software version, MCP revision and signing version distinct. Do not declare new support by changing a version label alone.
3. For a new draft, update the current `SPEC.md`, `VERSION`, `release.json`, example, changelog and links together. `SPEC.md` must exactly equal the current versioned specification. Update release fingerprints to the intended versioned artifacts, then inspect the diff.
4. Run `python tools/validate.py --check-repo` in the prepared environment. Test changed behavior with appropriate negative cases as well as valid examples. The checks do not certify a deployed MCP server.
5. Coordinate publication of the same exact specification/schema bytes to the proposal website. GitHub and the Lovable website are not automatically synchronized. Verify both live copies before announcing the release, then create an identified GitHub release. Existing versioned files and tags must not be moved to newer content.
6. Test any affected MCP implementation separately, including retained host definitions, complete catalogs and relevant caching behavior. Report any host inventory that was not checked.

Joakim Jardenberg maintains this draft. External standards-body review or adoption is not implied by accepting a contribution.
