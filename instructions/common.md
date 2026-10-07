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

- Architecture-changing feature/refactor: after requirements/decisions are sufficiently aligned, use `design` to create the architecture proposal. Use `challenge` optionally to adversarially strengthen a complex/high-risk draft, then use `review` to independently accept or reject the baseline before `to-spec` or implementation.
- `challenge` and `review` have different authorities: challenge is high-recall multi-perspective critique with no verdict; review is low-noise independent acceptance based on authoritative requirements and repository evidence.
- Architecture-focused `wayfinder`: when the fog clears into a coherent architecture change, hand off through `design → optional challenge → review → to-spec`. If architecture is already accepted and wayfinding only resolved execution uncertainty, go directly to `to-spec`.
- For high-risk or multi-session implementation specs, the same `review` skill may use its spec-fidelity mode; do not create a separate review skill.

# Prototype / Verification Overlay

- Apple-platform prototype: when `prototype` depends on Swift/Objective-C compilation, UIKit/SwiftUI, Apple framework behavior, lifecycle, persistence, hardware, or device/runtime semantics, use the smallest native executable, test target, demo controller/view, preview, or integration harness that can answer the single question instead of forcing an HTML/web artifact.
- Behavior-preserving refactor: before changing behavior-bearing legacy code, characterize the current observable behavior at an existing seam, then refactor in small green steps. Expected values must come from current behavior, a known fixture, protocol/spec, or another independent oracle.
- Runtime validation: keep unit/integration/device evidence distinct. BLE, Watch, background lifecycle, entitlement, hardware timing, and similar OS/device behavior remain runtime gates even when unit tests pass.

# Artifact Lifecycle Overlay

Use three storage tiers; choose by artifact authority, not by file type.

## 1. Canonical project knowledge

Keep durable source-of-truth material in the repository's established tracked location. Examples:

- `GLOSSARY.md`, `GLOSSARY-MAP.md`, ADRs;
- `docs/agents/*` project configuration;
- accepted Design Docs or other documents the user/project explicitly wants maintained;
- production documentation.

Follow an existing project convention when one exists. Do not move canonical documents into `.scratch` merely because an agent generated them.

## 2. Project-local reasoning artifacts

When a repository context exists, any non-canonical artifact worth showing to the human, referencing later, or carrying across sessions belongs under:

```text
<repo-root>/.scratch/artifacts/<category>/
```

Resolve `<repo-root>` from the repository root (for Git repositories, prefer `git rev-parse --show-toplevel`).

Use a stable category that describes the artifact's role. Preferred categories:

- `architecture/` — architecture surveys/reviews, before-after HTML, diagrams;
- `research/` — research notes that are inputs to decisions but not canonical project docs;
- `handoff/` — cross-session handoff documents;
- `prototype/` — prototype summaries/evidence pointers; prototype source may still follow the prototype skill's branch convention;
- `reports/` — other human-facing analysis/report artifacts.

Examples:

```text
.scratch/artifacts/architecture/architecture-review-20261008-000920.html
.scratch/artifacts/research/core-nfc-entitlement.md
.scratch/artifacts/handoff/scooter-setting-design.md
```

This is the default when an upstream skill otherwise says "somewhere sensible" or writes a human-facing result only to an OS temp directory.

Specific overlays:

- `improve-codebase-architecture`: it may render in `$TMPDIR`, but copy/move the final HTML to `.scratch/artifacts/architecture/`, open that copy, and report that path.
- `handoff`: with repository context, save the handoff under `.scratch/artifacts/handoff/` instead of delivering only a `$TMPDIR` file.
- `research`: follow an existing project research-note convention if one exists; otherwise use `.scratch/artifacts/research/`.
- `prototype`: preserve upstream source/throwaway-branch semantics; use `.scratch/artifacts/prototype/` only for summaries, evidence, or pointers that should survive the current session.

Do not redirect tracker artifacts (`to-spec`, `to-tickets`, `wayfinder`) away from their configured issue tracker/local tracker. Do not redirect glossary/ADR/setup outputs away from their canonical paths.

Treat `.scratch/artifacts/` as non-canonical working state. Do not silently add it to tracked `.gitignore` or commit it unless the user/project explicitly chooses that policy.

## 3. Machine-temporary files

`$TMPDIR`, `/tmp`, macOS `/var/folders/.../T`, and equivalent OS temp locations are for intermediate generation only: render inputs, conversion files, caches, downloads, or disposable scratch work.

If a temp-produced result is worth handing to the user or a later session, promote it to tier 1 or tier 2 before reporting completion.

## Delivery

- Final responses must report the durable/project-local path, not only the temp path.
- If auto-open is attempted, open the promoted copy.
- Mention the temp path only for debugging.
- If no repository context exists, fall back to `${AGENT_ARTIFACTS_DIR:-$HOME/Documents/agent-artifacts}/`; if unavailable, use `$HOME/Downloads/agent-artifacts/`.

# Code Navigation

- Use native search for simple lookup; when available, use `cx` where structural navigation avoids broad reads.
- Treat structural navigation as guidance, not compiler-complete semantics; use compiler or LSP tooling when language semantics matter.
