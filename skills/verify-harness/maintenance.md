# Maintain mode

A feature map drifts as the app changes. This mode keeps an existing `verify-<app>` skill honest. The unit of rigor is the feature: every feature file is checked against source, and every feature is driven live at least once.

State the outcome:

- **clean**: every feature covered from source and live; nothing to change.
- **changed**: proven corrections to the skill's own files, left uncommitted for the user.
- **blocked**: coverage could not finish; name the blocker.

Edit scope is the verify skill's own directory (its SKILL.md, `features/`, and CLI). When the app no longer does what the map says, it is either map drift (fix the map) or a product regression (report it to the user; product code stays as it is).

## Pass

1. **Index**: `features/README.md` matches its sibling files, with no missing, extra, or dead entries.
2. **Source**: for each feature file, read the code and tests behind it and note drift with `file:line`. Sweep history since the last driven-live date (`git log --since=<date> --stat`) for user-facing paths missing from the map; call one missing only with a concrete source path.
3. **Live**: drive every feature through the CLI, merging recipes that share an app state. Run `doctor` before the first drive and after any failed or surprising one. A wedged UI on a healthy process means reset or relaunch. After each cleanup, check that the evidence captured so far is still at its location.
4. **Triage**:
   - Wrong or missing user-POV description → map drift; fix it.
   - Working behavior the CLI cannot drive → harness gap; fix it and re-drive live.
   - A `doctor` failure caused by the skill itself → drift; fix it and retry once before calling the pass blocked.
   - Broken app behavior → product gap; report it.
   - A feature that cannot be reached is `unreachable` only with the attempted route and the concrete missing prerequisite (device only, account, entitlement). That prerequisite belongs in its `Gotchas`.
5. **Close**: update the README's driven-live record with instance and date, run `cleanup` after the last drive, and report the outcome, features covered, unreachable prerequisites, drift fixed, product gaps, and evidence paths.
