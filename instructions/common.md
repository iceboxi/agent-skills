# Engineering Rules

- Inspect relevant code before making codebase-specific technical conclusions.
- Support important technical claims with `file:line` evidence.
- For the one or two facts a change's safety depends on, push the evidence as far as is cheap and state where it stopped: asserted → `file:line` → failure path walked → real code run (a script/test that fails loudly if wrong) → reproduced in the running app/device. Do not present a lower level as proof.
- Do not reinforce unverified assumptions.
- When two fixes built on the same assumption fail the same check, stop patching. State that assumption in one sentence, verify it against code or runtime evidence, and revise it before attempting another fix.
- Prefer minimal, verifiable changes over broad refactors.
- Follow existing codebase and platform patterns.
- Include appropriate regression verification for behavioral changes.
- Fix the cause of a failure. A guard, `try?`, fallback default, retry, or catch-all that only hides the symptom is mitigation: report it as mitigation, not as a fix.
- Resolve compiler, type-checker, and linter errors at their cause. Any suppression (`as!`, a force unwrap added only to compile, `@ts-ignore`, `swiftlint:disable`, `# type: ignore`) needs a stated reason in the code or the response.
- When the same mistake class recurs, fix it at the highest layer that works: architecture/ownership → types → a lint/CI check whose error names the fix → behavior test → docs/agent rules only for judgment calls. Prove any new check fails on a real past instance.
- Verify side effects before modifying repository flows.
- Do not duplicate state ownership.
- Names over comments: names, types, small functions, and tests should say what code does. In code you write or modify, delete comments that only restate them: signature-echo docs, field-name echoes, narration of the next line. Descriptions of runtime behavior get no exemption. Doc comments required by the project's linter or public-API convention (for example SwiftLint `missing_docs`, or DocC for a published SDK) take precedence over this rule. Otherwise only two kinds of comment are allowed:
  - Module/class header: 1–3 lines stating its role and the invariant every change must preserve, i.e. the rule a new caller or new function could break.
  - Why-not: beside code that looks wrong, redundant, or arbitrary but is deliberate, stating the constraint, observed failure, or decision behind it. Name the code it protects so later changes can re-check it, and delete it together with that code.
- Use Traditional Chinese for explanations and reasoning, following terminology natural to Taiwan software engineering teams.
- Keep code identifiers and API names unchanged. Do not force-translate established engineering terms when the English term is clearer or more natural in Taiwan usage (for example: API, protocol, callback, workflow, state, snapshot, cache, payload, codec, timeout, retry, commit, rollback).
- Avoid Mainland-China-specific engineering translations when Taiwan usage, repository terminology, or the original English term is more natural.
- Preserve terminology already established by the repository, source documents, domain model, and platform conventions; do not create a second vocabulary merely for prose.
- Explicit terminology requested by the user takes precedence for audience-facing wording, while quoted source text and code identifiers remain unchanged. Apply such terminology consistently across the output.
- Ask before adding newly discovered conventions to project `AGENTS.md`.

# UI Rules

- Avoid unnecessary secondary labels and descriptions. Let the layout do the explaining.

# Workflow Overlay

Matt skills are the generic workflow base. Apply these local differences only when the branch matches:

- Follow Matt upstream by default: `grill-with-docs → to-spec → to-tickets → implement` (or its small-work shortcut). Requirements and architecture decisions belong to the existing discussion/spec process, not a mandatory local design stage.
- During `grill-with-docs`, when a frontier question needs a runnable answer (a state model, business logic, a UI to see, or Apple framework/device behavior), recommend the `/prototype` detour for that question instead of settling it in conversation, and keep it open until the verdict returns. `to-spec` records a question still waiting on its prototype as unresolved. Product and preference calls stay with the user.
- On explicit user request, run local `design` **after** the spec and work breakdown to publish an independently readable Markdown Design Doc for technical/manager communication, normally before implementation. Extract and visualize source decisions; do not redesign or override the spec.
- Do not expose individual tickets (IDs, names, statuses, URLs, ticket-to-phase mapping) in the Design Doc. Summarize planned work as meaningful engineering phases, keeping relevant dependencies, gates and evidence.
- `challenge` and `review` are both optional **user-invoked** skills, never automatic acceptance gates. Challenge explores blind spots; review assesses a selected design/spec only when asked.

Many skills named in these instructions are user-invoked: installed, but hidden from your skill list. To run one, ask the user to type `/name` (Claude Code) or `$name` (Codex) instead of executing it yourself.

# Phased Delivery Overlay

When the user asks to split a spec into phases:

- A **phase** lands on trunk on its own and leaves trunk releasable. It ends on an **exit check**: the surface (per Runtime validation below), a concrete scenario, and a pass predicate. A phase that claims a performance effect also names the metric, the probe, the trunk baseline measured before the change, and the number that fails. A phase that only works once a later phase lands merges into that phase or becomes an expand–contract step.
- `to-spec`: add a `## Phases` section giving each phase its delivered user stories, deferred scope, and exit check. Confirm the phase boundaries with the user together with the test seams.
- `to-tickets`: assign every ticket to exactly one phase (a `**Phase:**` line in local tickets; a milestone or label on a real tracker). Blocking edges point to the same or an earlier phase.
- `implement-spec`: implement one phase per invocation, on its own integration branch and PR started from trunk after the previous phase lands, instead of one branch for the whole spec. The phase is done when its exit check has run and passed.
- `design`: take the Design Doc phases from the spec's `## Phases` section.

# Prototype / Verification Overlay

- Apple-platform prototype: when `prototype` depends on Swift/Objective-C compilation, UIKit/SwiftUI, Apple framework behavior, lifecycle, persistence, hardware, or device/runtime semantics, use the smallest native executable, test target, demo controller/view, preview, or integration harness that can answer the single question instead of forcing an HTML/web artifact.
- Behavior-preserving refactor: before changing behavior-bearing legacy code, characterize the current observable behavior at an existing seam, then refactor in small green steps. Expected values must come from current behavior, a known fixture, protocol/spec, or another independent oracle.
- Vacuous-test check: before relying on a new or changed test, confirm by inspection that it would fail if the code under test returned an empty or default result (`nil`, `0`, empty collection, no-op side effect). If it would still pass, strengthen the assertion to check the observable outcome, or remove the test.
- XCUITest verdict: read the result bundle (`xcrun xcresulttool get test-results summary`), not the `xcodebuild` exit code. It exits 0 when every selected test skipped; a skip is not a pass.
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

Cleanup is manual-only: completed .scratch work may be proposed for deletion after checking unfinished dependencies and durable knowledge. Non-canonical status alone never authorizes deletion; require explicit approval of exact paths. Durable ADRs belong in the project's canonical docs (for example docs/adr/), not .scratch. Do not automatically archive or modify Wiki.

For promoted temp artifacts, final responses should report the project-local path and auto-open that copy when possible. Mention the OS-temp path only for debugging.

# Code Navigation

- Use native search for simple lookup; when available, use `cx` where structural navigation avoids broad reads.
- Treat structural navigation as guidance, not compiler-complete semantics; use compiler or LSP tooling when language semantics matter.
