# Engineering Rules

- Inspect relevant code before making codebase-specific technical conclusions.
- Support important technical claims with `file:line` evidence.
- Do not reinforce unverified assumptions.
- Prefer minimal, verifiable changes over broad refactors.
- Follow existing codebase and platform patterns.
- Include appropriate regression verification for behavioral changes.
- Verify side effects before modifying repository flows.
- Do not duplicate state ownership.
- Use Traditional Chinese for explanations and reasoning; keep code, APIs, and technical terms in their original language.
- Ask before adding newly discovered conventions to project `AGENTS.md`.

# Code Navigation

- Use native search for simple lookup; when available, use `cx` where structural navigation avoids broad reads.
- Treat structural navigation as guidance, not compiler-complete semantics; use compiler or LSP tooling when language semantics matter.
