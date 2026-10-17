---
name: cleanup
description: On explicit user request, inspect the current repository's .scratch working state, preserve unfinished work and durable knowledge, and propose a safe cleanup plan before any deletion.
disable-model-invocation: true
---

# Cleanup Working Artifacts

Run only when the user explicitly invokes `$cleanup`. This is a manual maintenance operation, never a post-implement hook or an automatic gate. Default to inspection and a dry-run report; never delete merely because this skill was invoked.

## Scope and ownership

- Work only within the current repository's `.scratch/` directory, or a narrower user-provided path inside it. Resolve real paths and symlinks; never follow links outside the allowed scope or operate on another repository.
- Read the project's `docs/agents/issue-tracker.md` if present. Its actual configured tracker is authoritative; do not infer tracker choice solely from Git remotes or `.scratch/` existence. If missing, treat tracker status as unknown.
- Read relevant project instructions, current Spec/Map/Tickets/Design, code/tests, and dependency references as needed. Use existing tracker operations to inspect GitHub/GitLab or local state; do not implement or assume Matt-specific internal APIs, filenames, skill names or ticket schemas.
- This skill does not alter GitHub/GitLab issues or comments, manage Wiki, delete branches/worktrees, scan OS temp, change `.gitignore`, or modify upstream skills.

## Classify by work unit

Identify related Spec, Tickets, Design, research notes, handoff, and other artifacts. Do not assume all files under `.scratch/` belong to the same work item. Check whether sibling or other active efforts reference each item.

- **Completed**: all in-scope deliverables are implemented, required verification and acceptance are evidenced, there are no open requirements or active dependencies. Candidate: the *entire related working directory*, including local Spec, Map, Tickets and Design, regardless of tracker type. A closed ticket alone is insufficient.
- **In progress**: preserve the latest effective Spec, Tickets, Map, Design and inputs needed to continue; do not prune completed ticket records from a still-active work unit. Only obsolete, unreferenced intermediate outputs are candidates.
- **Superseded**: keep the currently effective working version; older drafts are candidates after confirming significant rationale has been retained and no remaining work depends on them. Avoid silently choosing a latest version from names or timestamps where authority is unclear.
- **Unknown**: do not propose the whole unit for deletion. Report which evidence is missing.

For remote-backed work, read the relevant issues/PRs/MRs to establish status and dependencies. For local-only work, use the effective local tracker records. Both use the same cleanup policy; tracker choice changes evidence discovery, not retention policy.

## Knowledge preservation check

Before proposing deletion, check whether it would remove:
1. decisions or constraints that remain valid but are not evident from current code, tests, ADRs or maintained documentation;
2. evidence that would be difficult to recreate and matters for future development or an open issue;
3. material referenced by unfinished or shared work.

Preserve only durable, useful knowledge, not whole outdated Specs by default. Recommend an existing project documentation destination, usually `docs/adr/` for lasting architectural decisions, or an existing project convention. ADRs and other canonical documents must not be stored under `.scratch/` or deleted by this skill. GitHub Wiki management and automatic archival are out of scope.

When information needs promotion, mark affected files **blocked** until that separate save/decision is completed. Do not silently rewrite the Spec, create ADRs, post attachments, or copy files to a remote system as a cleanup side effect.

## Safety and execution

1. Inspect `git status` and `git check-ignore` / `git ls-files` for candidates; ignored and untracked files may be irrecoverable. Never assume Git can restore them.
2. Report exact path, work-unit status, proposed action, rationale, evidence, dependencies, and whether each candidate is tracked, ignored or untracked. Distinguish **DELETE CANDIDATE**, **RETAIN**, **BLOCKED**, and **UNKNOWN**. Prefer whole completed work units; do not sweep unrelated artifacts.
3. **Stop at dry-run**. Ask for explicit approval of the exact enumerated deletion targets. `$cleanup` alone is not approval. Do not delete wildcard-expanded or newly created paths that were not approved.
4. After approval, recheck paths, contents, tracker completion, active dependencies, working-tree changes and preservation blockers. If anything material changed, stop and issue a revised plan for approval.
5. Delete only approved files within the permitted scope; never use an unchecked recursive wipe. Do not remove tracked files with pending user modifications unless those exact modifications and their loss were explicitly disclosed and approved.
6. Verify the remaining paths and report deleted, retained, skipped and failed items. Do not claim cleanup succeeded without checking.

Never delete the `.scratch/` root automatically. If no safe candidates exist, report that and make no changes.
