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

# Workflow Overlay

Matt skills are the generic workflow base. Apply these local differences only when the branch matches:

- Follow Matt upstream by default: `grill-with-docs → to-spec → to-tickets → implement` (or its small-work shortcut). Requirements and architecture decisions belong to the existing discussion/spec process, not a mandatory local design stage.
- On explicit user request, run local `design` **after** the spec and work breakdown to publish an independently readable Markdown Design Doc for technical/manager communication, normally before implementation. Extract and visualize source decisions; do not redesign or override the spec.
- Do not expose individual tickets (IDs, names, statuses, URLs, ticket-to-phase mapping) in the Design Doc. Summarize planned work as meaningful engineering phases, keeping relevant dependencies, gates and evidence.
- `challenge` and `review` are both optional **user-invoked** skills, never automatic acceptance gates. Challenge explores blind spots; review assesses a selected design/spec only when asked.
- Architecture-focused `wayfinder` rejoins upstream at `to-spec`; no Design Doc is required unless the user asks for one.

# Prototype / Verification Overlay

- Apple-platform prototype: when `prototype` depends on Swift/Objective-C compilation, UIKit/SwiftUI, Apple framework behavior, lifecycle, persistence, hardware, or device/runtime semantics, use the smallest native executable, test target, demo controller/view, preview, or integration harness that can answer the single question instead of forcing an HTML/web artifact.
- Behavior-preserving refactor: before changing behavior-bearing legacy code, characterize the current observable behavior at an existing seam, then refactor in small green steps. Expected values must come from current behavior, a known fixture, protocol/spec, or another independent oracle.
- Runtime validation: keep unit/integration/device evidence distinct. BLE, Watch, background lifecycle, entitlement, hardware timing, and similar OS/device behavior remain runtime gates even when unit tests pass.

# Temp Artifact Overlay

Keep Matt upstream artifact ownership unchanged except for the following UX fixes.

- `handoff`: when a repository context exists, save the handoff under `<repo-root>/.scratch/artifacts/handoff/` instead of delivering only an OS-temp file. With no repository context, keep the upstream OS-temp behavior.
- `improve-codebase-architecture`: it may render the HTML report in `$TMPDIR` as upstream specifies, but when a repository context exists, copy/move the final report to `<repo-root>/.scratch/artifacts/architecture/`, open that copy, and report that path. With no repository context, keep the upstream OS-temp behavior.
- `research`: follow the repository's existing research-note convention. Only when no convention exists, use `<repo-root>/.scratch/artifacts/research/`.

Do not redirect other upstream artifacts:

- `to-spec`, `to-tickets`, and `wayfinder` keep using their configured tracker/local-tracker locations.
- prototype source keeps the upstream prototype/throwaway-branch semantics.
- glossary, ADR, `docs/agents/*`, and other canonical project documents keep their established project paths.

`.scratch/artifacts/*` is non-canonical working state. Do not silently add it to tracked `.gitignore` or commit it unless the user/project explicitly chooses that policy.

For promoted temp artifacts, final responses should report the project-local path and auto-open that copy when possible. Mention the OS-temp path only for debugging.

# Code Navigation

- Use native search for simple lookup; when available, use `cx` where structural navigation avoids broad reads.
- Treat structural navigation as guidance, not compiler-complete semantics; use compiler or LSP tooling when language semantics matter.
