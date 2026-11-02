---
name: verify-harness
description: Generate or maintain a project-owned verify-<app> skill that drives the real app the way a user does and keeps evidence a reviewer can reopen.
disable-model-invocation: true
---

# Verify Harness

A build or a green unit test does not prove what a user sees. This skill gives a repository its own `verify-<app>` skill: one fixed CLI that launches the real app in an isolated instance, drives a user path, and leaves evidence a reviewer can reopen, plus a feature map that says how to reach each feature.

The output is read cold by the next agent, mid-task, with no memory of this session. Every command, selector, and path in it comes from this repo and was run here.

## Pick the mode

- No verification skill in the repo → **create** (below).
- A `verify-*` skill already exists in the repo's project-skill directory → **maintain**: follow [maintenance.md](maintenance.md). Several candidates → ask which one.

## Create

### 1. Interview the repo

Answer from the codebase. Ask the user only what you cannot observe, or what is theirs to decide.

- **Surface**: what a user touches. An Apple-platform app, web UI, CLI/TUI, service/API, or library. Pick the primary surface; list the others as not mapped.
- **Run**: the repo's own build/start command (scheme, package script, Makefile, README). Ports, env vars, seed data, auth.
- **Drive**: existing harnesses first (UI test targets, Playwright/Cypress specs, PTY/expect scripts, HTTP endpoints, deep links). Read how existing tests launch the app, find elements, and dismiss first-run alerts. Those helpers are the drive vocabulary.
- **Observe**: structured test results, screenshots, transcripts, response bodies, stored data, logs.
- **Isolate**: whether a second instance can run beside the user's (own simulator, port, data dir, profile). List the instances the user already keeps (named simulators, local databases, browser profiles). The generated skill leaves those untouched.
- **Fixtures**: an existing seed script or test-data generator that reaches a known state without the network.
- **Boundaries**: what an isolated instance cannot reach (device hardware, cloud sync, purchases, third-party accounts).

Then read the matching recipe: Apple platforms → [apple.md](apple.md); web, CLI/TUI, services → [other-surfaces.md](other-surfaces.md).

Ask the user before creating an instance whose name resembles an existing one, installing any tool, changing `.gitignore`, or touching data the fixture did not create. If the checkout does not build or start, fix that or report it precisely before generating: a skill written against a broken base teaches wrong steps.

Done when every bullet has an answer backed by a file path or command output, or is listed as a question for the user.

### 2. Place the skill

- Follow the repo's existing project-skill location and format (`.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, sibling `agents/openai.yaml`). Match sibling skills' frontmatter.
- With no existing location, use `.agents/skills/verify-<app>/` plus a relative symlink `.claude/skills/verify-<app> -> ../../.agents/skills/verify-<app>`, so Claude Code and Codex read one copy.
- Evidence goes to `.scratch/artifacts/verify/<run-id>/`. Instance state and build products go to a directory the repo already ignores (often `build/`). Check both with `git check-ignore`. If neither is ignored, ask.

### 3. Write the CLI

One executable entry point owns every step, in the language the repo already uses for tooling (stdlib Python when there is no preference).

| Subcommand | Contract |
| --- | --- |
| `launch` | Create or reuse the dedicated instance, build, install, seed the fixture. Reaches *usable*, not merely *started*. `--skip-build` reinstalls and reseeds. |
| `doctor` | Read-only. Instance exists and runs, installed build matches the built products, data is exactly the fixture. Prints `doctor: OK`, or `FAIL` with the command that fixes it. |
| `test` | Run a scripted journey (UI test, spec, script) and judge it from its structured result. |
| `shot`, `state`, `logs` | Capture screen, persisted data, and app logs into the run's evidence directory. |
| `cleanup` | Stop only what this run started. Evidence survives. Fails if the evidence directory is missing or empty. |

The CLI enforces these, so the next agent cannot skip them:

- **Verdict from the structured result.** Parse the result bundle or report. Fail on any failure, any skip, or zero executed checks. Runner exit codes and success banners are not the verdict.
- **Refuse unsafe states.** Seeding refuses an instance holding data it did not create. A lock refuses a second concurrent drive on one instance; parallel agents pass a different instance name.
- **Kill what you started.** Record PIDs and whether this run booted the instance. Kill by recorded PID, shut down only what this run booted, and keep shared instances' data.
- **Loud failures.** Every error names the command that fixes it.

### 4. Write the generated SKILL.md

Frontmatter: `name: verify-<app>` and a model-facing `description` naming the app, the surface, and the triggers (a change needs runtime proof; a reported behavior needs reproducing). Leave it model-invoked, so agents reach for it when proof is needed.

Sections, each grounded in step 1:

- **Launch**: command, first-run duration, what *ready* means.
- **Doctor**: when to run it. On `FAIL`, run the named fix before any drive.
- **Drive**: ordered options, first fit wins. An existing scripted test covers the journey → run it. None does → write the journey as a real test in the repo's test target; it becomes the change's regression test and is kept. What cannot be scripted yet → launch-state observation or an exploration tool from the recipe. Real identifiers from this repo.
- **Evidence**: a table of command → files written, then the proof standards: the real user path, never internal setters or test-only shortcuts; the action plus the resulting state; for data-writing changes, `state` before and after with the diff; mocks only where the app already isolates the external system; the reply names feature, entry point, command, and evidence paths.
- **Cleanup** and **Isolation**: as the CLI enforces them.
- **What this cannot prove**: the boundaries from step 1, stated as runtime gates.
- **Feature map**: a pointer to `features/README.md`, plus the rule that a change adding or moving a user path updates its feature file in the same change, and that a journey blocked by a missing precondition reports failure and records the reason under `Gotchas` with the journey kept at full strength.

### 5. Seed the feature map

`features/README.md` indexes one file per user-facing feature. Start with the 3–5 most used (from routes, tabs, commands, docs). Each feature file has these H2s: `Sub-features`, `How to get to it (user POV)`, `Driving it with <cli>`, `Gotchas`. Give sub-features short kebab-case ids (`paging-turn`) so a report can name exactly what was covered.

The README records which sub-features were driven live, on which instance, and when. Recipes written only from reading tests are labeled as such: their first failure may be map drift before it is a regression. List the user-facing areas not mapped yet.

### 6. Prove it end to end

A generated skill never executed is a draft. Run its own instructions once, through the CLI only:

1. `launch` from nothing (no instance, no build products), then `doctor: OK`.
2. Drive one mapped sub-feature to a pass and capture its evidence.
3. Turn the gate **red**: drive something it must reject (a test that skips on the fixture, an unknown test id, a broken precondition) and confirm a non-zero exit. A gate never seen red is unproven.
4. `cleanup`, then confirm the evidence is still at its named location and the instance is back to how this run found it.

Run `cleanup` after every failed attempt before retrying. If a step ran in a stand-in (another device model or OS, a local stack for a remote one), list what the stand-in did that the real target will not; those stay unverified.

Done when all four steps passed in one run and their output sits in the evidence directory.

### 7. Hand over

Report the files created, the step 6 commands with their results, the evidence directory, which sub-features were driven live versus read from tests, and the open user decisions (commit, tool installs, instance names). Generated files stay uncommitted until the user asks. Maintain mode of `verify-harness` is the upkeep path when the app changes.

---

Adapted in our own words from `create-verification-skill` and `maintain-verification-skill` in Lauren Tan's pstack (MIT, © 2026 Lauren Tan).
