# Engineering Rules

- Inspect relevant code before making codebase-specific technical conclusions.
- Support important technical claims with `file:line` evidence.
- Do not reinforce unverified assumptions.
- Prefer minimal, verifiable changes over broad refactors.
- Follow existing codebase and platform patterns.
- Include appropriate regression verification for behavioral changes.
- Verify side effects before modifying repository flows.
- Do not duplicate state ownership.
- Use Traditional Chinese for explanations and reasoning, following terminology natural to Taiwan software engineering teams.
- Keep code identifiers and API names unchanged. Do not force-translate established engineering terms when the English term is clearer or more natural in Taiwan usage (for example: API, protocol, callback, workflow, state, snapshot, cache, payload, codec, timeout, retry, commit, rollback).
- Avoid Mainland-China-specific engineering translations when Taiwan usage, repository terminology, or the original English term is more natural.
- Preserve terminology already established by the repository, source documents, domain model, and platform conventions; do not create a second vocabulary merely for prose.
- Explicit terminology requested by the user takes precedence for audience-facing wording, while quoted source text and code identifiers remain unchanged. Apply such terminology consistently across the output.
- Ask before adding newly discovered conventions to project `AGENTS.md`.

# Code Navigation

- Use native search for simple lookup; when available, use `cx` where structural navigation avoids broad reads.
- Treat structural navigation as guidance, not compiler-complete semantics; use compiler or LSP tooling when language semantics matter.
