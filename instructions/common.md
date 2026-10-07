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

# Code Navigation

- Use native search for simple lookup; when available, use `cx` where structural navigation avoids broad reads.
- Treat structural navigation as guidance, not compiler-complete semantics; use compiler or LSP tooling when language semantics matter.
