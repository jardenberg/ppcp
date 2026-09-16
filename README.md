# PPCP: Public Personal Context Protocol

**Draft 0.1.1 · [Read the proposal](https://ppcp.jardenberg.net/) · [Specification](SPEC.md) · [Try the validator](https://ppcp.jardenberg.net/validate)**

PPCP is an open proposal for publishing a substantial, first-party account of a person so people, AI assistants and the web can discover, retrieve and cite it. It covers identity, family and everyday life, values, ideas, practical ways of working and preferences. The person chooses the public subset.

Publish it as a readable page, downloadable Markdown and structured JSON. An optional read-only MCP connector lets an assistant retrieve relevant sections and sources. Public context complements private memory; it grants no access to it and no authority to act or speak for the subject.

This is an experimental draft by Joakim Jardenberg, developed with AI assistance. It is published for use, criticism and improvement. It is not a ratified standard or a claim that every AI service supports automatic discovery.

## Start here

| What you need | Where to go |
|---|---|
| Understand the proposal | [Website](https://ppcp.jardenberg.net/) |
| Read the current specification | [SPEC.md](SPEC.md) or [pinned draft 0.1.1](spec/0.1.1.md) |
| Create a profile | [Fictional 0.1.1 example](examples/profile-0.1.1.json) and [schema](schema/profile-0.1.1.json) |
| Check a profile | [Browser validator](https://ppcp.jardenberg.net/validate), or the local commands below |
| See a real profile | [Joakim Jardenberg](https://joakim.jardenberg.net/) |
| Connect an AI client | [Reference MCP setup](https://joakim.jardenberg.net/mcp) |
| Understand updates and caching | [Specification section 11](SPEC.md#11-freshness-updates-and-compatibility) and [practical guide](https://ppcp.jardenberg.net/mcp#freshness) |
| Propose an improvement | [Open an issue](https://github.com/jardenberg/ppcp/issues) or read [CONTRIBUTING.md](CONTRIBUTING.md) |

The Alex Example profiles are fictional teaching examples. Their identity links and statements are illustrative. Joakim's real profile is maintained at its own canonical URL; this repository links to it.

## Versions and scope

This repository contains the protocol documents, schemas, examples and portable validation helper. The documentation website and reference MCP server are separately deployed applications. GitHub changes do not automatically deploy either application.

- `SPEC.md` follows the current draft, recorded in [VERSION](VERSION) and [release.json](release.json).
- `spec/0.1.0.md` and `spec/0.1.1.md` preserve exact published editions. Versioned schemas are preserved alongside them.
- Draft 0.1.1 adds freshness and compatibility guidance without new required profile fields. A document declaring 0.1.0 still uses the 0.1.0 schema.
- The reference server currently declares PPCP 0.1.0, with profile edition 0.6. Publishing draft 0.1.1 here does not relabel that separate implementation.

Profile editions, software builds, the PPCP draft, MCP revisions and signing specifications are distinct. A valid signature or successful connection does not prove that the newest content or tool definitions were used. Host adoption is a separate step.

## Validate locally

Use Python 3.11 or newer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/validate.py examples/profile-0.1.1.json
.venv/bin/python tools/validate.py --check-repo
```

Validation selects a bundled schema from the declared version, checks its structure, reproduces the Markdown digest, and checks section/source IDs. It does not verify identity, the truth of statements, review approval, signatures, live MCP behavior or an AI app's enabled tools. Input stays local; no profile is uploaded or schema fetched from a user-supplied URL.

The GitHub workflow runs the repository checks on pushes and pull requests. [Contributing guidance](CONTRIBUTING.md) explains how to preserve published versions and coordinate a new release with the website.

## Licence

Original material in this repository is © 2026 Joakim Jardenberg and licensed under **[Creative Commons Attribution 4.0 International](LICENSE)**. Reuse and adaptations require attribution and identification of changes. Suggested attribution: “PPCP, Joakim Jardenberg, https://ppcp.jardenberg.net/, CC BY 4.0.”

Identified third-party quotations, linked standards and dependencies retain their own rights and licences. Their presence is not a relicensing or endorsement. Reuse of a profile does not turn an adaptation into the subject's current approved statement.

## Related work

PPCP builds on personal user manuals, context portfolios and existing web standards. It does not replace [MCP](https://modelcontextprotocol.io/specification/latest). The reference server uses [Verifiable MCP](https://github.com/jardenberg/verifiable-mcp) for origin, integrity and declared provenance. See [the specification's precedents](SPEC.md#10-precedents) for the broader context.
