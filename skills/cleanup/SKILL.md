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
- Do not modify GitHub/GitLab issues or comments, upload attachments, or write maintained documentation without separate explicit approval of the destination and content. Never manage Wiki, delete branches/worktrees, scan OS temp, change `.gitignore`, or modify upstream skills.

## Incidental filesystem metadata

Ignore Finder-generated `.DS_Store` files inside `.scratch/` **by default**, provided they are untracked and ignored: do not hash them, classify them as work artifacts, include them in deletion proposals or actionable file counts, or treat them as cleanup blockers. Finder can rewrite or recreate these files at any time, so repeatedly chasing them does not improve cleanup. At most, note their excluded count separately; leave them untouched.

This narrow exception applies only to files whose exact basename is `.DS_Store`. Do not generalize it to other hidden files, tracked files, or unrecognized OS/tool artifacts. If the user *explicitly* wants particular `.DS_Store` files deleted, enumerate their exact paths and obtain normal deletion approval. At execution, verify each remains an untracked, ignored, regular (not symlink) file within the permitted scope. Content or SHA256 changes **alone** are not material for these approved, disposable metadata files; do not demand reapproval for hash churn, but stop on path, type, scope, tracking, or authorization changes.

## Classify by work unit

Identify related Spec, Tickets, Design, research notes, handoff, and other artifacts. Do not assume all files under `.scratch/` belong to the same work item. Check whether sibling or other active efforts reference each item. Inspect artifacts within each directory rather than assuming a whole directory shares one retention need.

- **Completed**: all in-scope deliverables are implemented, required verification and acceptance are evidenced, there are no open requirements or active dependencies. Candidate: the *entire related working directory*, including local Spec, Map, Tickets and Design, regardless of tracker type. A closed ticket alone is insufficient.
- **In progress**: preserve the latest effective Spec, Tickets, Map, Design and inputs needed to continue; do not prune completed ticket records from a still-active work unit. Keep only those local inputs necessary for active or imminent work. Obsolete outputs can be deletion candidates; historical evidence not needed locally should be considered for preservation elsewhere.
- **Superseded**: keep the currently effective working version; older drafts are candidates after confirming significant rationale has been retained and no remaining work depends on them. Avoid silently choosing a latest version from names or timestamps where authority is unclear.
- **Unknown**: do not propose the whole unit for deletion. Report which evidence is missing.

For remote-backed work, read the relevant issues/PRs/MRs to establish status and dependencies. For local-only work, use the effective local tracker records. Both use the same cleanup policy; tracker choice changes evidence discovery, not retention policy.

## Retention value gate

**Decide whether the artifact merits preservation before deciding where to store it.** Historical uniqueness, irreproducibility, size, or the existence of a convenient GitHub destination do not by themselves justify retention. For each artifact or meaningful group:

1. Identify a **specific future consumer or obligation**: an open investigation, reproducibility or rollback need, crash symbolication, regulatory/audit requirement, contractual retention rule, or durable decision not already captured in code/tests/docs. Distinguish a demonstrated requirement from hypothetical "might be useful someday."
2. Check whether **existing trusted sources are sufficient** (Git history, tests, ADRs, issue/PR outcome summaries, Xcode archives, app distribution records, established backups). Retain the smallest useful subset only if something important is missing.
3. Apply **proportionality**: does retaining this evidence materially help a likely future task, enough to justify ongoing storage, disclosure, retrieval, and maintenance cost? If not, classify it as a delete candidate, even if the file cannot be reconstructed. Note any irreversible loss in the dry-run and require explicit deletion approval.

Do not manufacture an archive requirement merely because a file is unique. Preserve authentic evidence when a real requirement exists; when the evidence is not needed, recommend deletion rather than transfer. If future need, ownership, or mandated retention is genuinely unclear, mark it `BLOCKED / UNKNOWN` and name the decision needed instead of guessing.

## Locality and disposition

Only after the retention value gate, decide whether valuable data must remain in `.scratch/`. Historical value alone is not sufficient. Independently assess (a) whether the data still merits retention and (b) whether active or imminent work needs direct local access. For each artifact, choose:

- **KEEP ACTIVE**: active or imminent work needs direct local access; identify the specific ticket, verification gate, or consumer, and preferably the files it needs rather than retaining an entire directory by association.
- **PRESERVE ELSEWHERE**: evidence that passed the retention value gate is not needed locally. Identify a concrete existing destination (for example, a relevant issue comment or attachment, PR, release artifact store, or project documentation convention), what to save, and how to verify retrieval. This is a **proposal**, not an automatic upload. Keep the source until preservation is verified, then reclassify the local copy as a delete candidate if no active dependency remains. A preservation proposal is not a final retention state.
- **DELETE CANDIDATE**: finished, obsolete, recoverable, reproducible, or low-value data with no active dependency or demonstrated retention obligation. Non-reproducible data may qualify when its loss has been explicitly evaluated and disclosed.
- **BLOCKED / UNKNOWN**: a decision, verification requirement, ownership, or destination is unresolved. State the exact missing fact; do not silently default every historical file to KEEP ACTIVE.

Classify mixed-content directories at file or meaningful subgroup granularity. Do not retain all release artifacts, all baseline measurements, or all files listed in an earlier retention manifest merely because one item is valuable. Revalidate previous `RETAINED.md`-style decisions against current issues, code, tests, and release state; prior retention labels are evidence, not permanent protection.

For release-related artifacts, distinguish current operational needs from hypothetical reconstruction. An old signed IPA, per-file source hash manifest, dirty-worktree patch, or full build log is **not automatically worth preserving**, even when unique or impossible to reproduce. Check whether that exact release is still supported, investigated, needed for rollback/forensics, or subject to an explicit retention rule; a later release and adequate tracker summary may make those files disposable. Treat dSYM separately when needed to symbolicate crashes from a still-relevant shipped version; check existing Xcode archives and symbol storage before proposing deletion. Keep only the evidence necessary for an actual need; never equate "upload succeeded" with proof that required crash or recovery artifacts are disposable. Prefer existing project retention arrangements rather than creating new archive machinery.

## Converge preservation proposals

A cleanup session should produce an actionable path to closure, not indefinitely repeat `PRESERVE ELSEWHERE`. For each preservation proposal, report:

- **Source**: exact local files (and relevant checksum/size when useful).
- **Destination**: specific existing Issue/PR/Release/artifact location or repository documentation path; no invented generic archive.
- **Minimum content**: preserve the decision, evidence, or recovery asset actually needed, not necessarily the entire old work directory.
- **Verification**: how to retrieve and check the preserved content, including integrity or version linkage for unique binaries and patches when applicable.
- **Local dependency**: named active work still requiring direct local access, or `none`.
- **Exit condition**: once preservation is verified and dependencies are resolved, reclassify the local source as `DELETE CANDIDATE`.

Before proposing a transfer, apply the retention value gate again: a prepared ZIP, manifest, previously labeled preservation proposal, or already-approved *destination* does not itself establish the content's value. If no concrete future need or retention duty survives, withdraw the preservation proposal and recommend direct deletion (with explicit approval), even for unique historical artifacts. If sufficient trusted records already exist, avoid duplicating them remotely. If an active issue still needs the local data, classify only the necessary files as `KEEP ACTIVE`, with a concrete revisit condition (for example, the relevant verification gate closing).

After the initial dry-run, invite **separate, explicit approval** of any proposed remote upload, issue/comment change, or maintained-document write, specifying the exact targets and content. Only an approved transfer can be performed; verify its existence and integrity before proposing removal of local originals. Deletion needs its own explicit approval of exact local paths even if preservation was approved. A single user-invoked cleanup workflow may progress through these approval checkpoints without requiring a newly invoked skill, but it never runs autonomously or treats approval of one operation as approval of another.

If transfer tooling or permissions are unavailable, report the precise manual action needed and leave affected local files intact. Do not invent an upload result or promise a later background cleanup.

## Knowledge preservation check

Before proposing deletion, check whether it would remove:
1. decisions or constraints that remain valid but are not evident from current code, tests, ADRs or maintained documentation;
2. evidence that would be difficult to recreate and matters for future development or an open issue;
3. material referenced by unfinished or shared work.

Preserve only durable, useful knowledge supported by an actual future use or obligation, not whole outdated Specs or full release evidence packages by default. Recommend an existing project documentation destination, usually `docs/adr/` for lasting architectural decisions, or an existing project convention. ADRs and other canonical documents must not be stored under `.scratch/` or deleted by this skill. GitHub Wiki management and automatic archival are out of scope.

When information needs promotion, mark local deletion **blocked** until the separately authorized save and its verification are complete. Never silently rewrite the Spec, create ADRs, post attachments, or copy files to a remote system as a cleanup side effect.

## Safety and execution

1. Inspect `git status` and `git check-ignore` / `git ls-files` for candidates; ignored and untracked files may be irrecoverable. Never assume Git can restore them.
2. Report exact path, work-unit status, proposed action, rationale, evidence, dependencies, and whether each candidate is tracked, ignored or untracked. Distinguish **KEEP ACTIVE**, **PRESERVE ELSEWHERE**, **DELETE CANDIDATE**, and **BLOCKED / UNKNOWN**. For preservation proposals, specify target and verification needed before deleting the local copy. Prefer a whole completed work unit only when every included file has been checked; do not sweep unrelated artifacts.
3. **Stop at dry-run**. Ask for explicit approval of the exact enumerated deletion targets. `$cleanup` alone is not approval. Do not delete wildcard-expanded or newly created paths that were not approved.
4. After approval, recheck paths, contents, tracker completion, active dependencies, working-tree changes and preservation blockers. If anything material changed, stop and issue a revised plan for approval. The only content-hash exception is for explicitly approved `.DS_Store` deletion under the narrow safeguards above.
5. Delete only approved files within the permitted scope; never use an unchecked recursive wipe. Do not remove tracked files with pending user modifications unless those exact modifications and their loss were explicitly disclosed and approved.
6. Verify the remaining paths and report deleted, retained, skipped and failed items. Do not claim cleanup succeeded without checking.

Never delete the `.scratch/` root automatically. If no safe candidates exist, report that and make no changes.
