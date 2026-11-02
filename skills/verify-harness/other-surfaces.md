# Web, CLI/TUI, and service recipes

Not yet proven in a pilot here. The first generation on one of these surfaces is its pilot: record in the hand-over what had to change from this file.

## Web UI

- **Launch**: the repo's dev command on a dedicated port, with its own database or data dir, so it never collides with the user's running dev server. Ready means a page renders the seeded data, not a port that answers.
- **Drive**: existing Playwright/Cypress specs first; they bring selectors and fixtures. For exploration, a browser automation tool available in the session. Select by role, ARIA label, or `data-testid`.
- **Isolate**: a separate browser profile per instance, never the user's logged-in profile.
- **Verdict**: the runner's JSON/JUnit report. Zero tests run, or all skipped, is a failure.
- **Evidence**: a screenshot per step, console errors, failed network requests, and the rows or files the action wrote.

## CLI / TUI

- **Launch** builds the binary once. Each drive runs in its own tmux or PTY session with a temporary `HOME`/config dir, so no state leaks between drives or into the user's config.
- **Drive** by sending keystrokes and waiting for a prompt string.
- **Evidence**: the full transcript, the exit code, and the files the command wrote.
- **Dry-run modes**: observe what they actually skip (network, files, git refs) before trusting the name.

## Service / API

- **Launch** with its own port and database. Ready means migrations and seeding finished and a real request returns seeded data; a health endpoint can pass while init scripts still run.
- **Drive** through the public API with the requests a real client sends.
- **Evidence**: request, status, response body, resulting rows, emitted messages.
- **Mocks** only for external systems the code already isolates behind a boundary.
