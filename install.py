#!/usr/bin/env python3
"""Install local workflow skills plus a pinned upstream skill set using protected symlinks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


TARGET_ROOTS = (".agents/skills", ".codex/skills", ".claude/skills", ".cursor/skills")
INSTRUCTION_TARGETS = (".codex/AGENTS.md", ".claude/CLAUDE.md")
MANIFEST_NAME = "skills-manifest.json"


class InstallError(Exception):
    pass


@dataclass(frozen=True)
class Action:
    source: Path
    destination: Path
    kind: str
    expected_bytes: bytes | None = None
    previous_link: Path | None = None


def tree_signature(root: Path) -> dict[str, tuple[str, str]]:
    """Compare every file and directory; never adopt nested symlinks."""
    if not root.is_dir():
        raise InstallError(f"Not a skill directory: {root}")
    signature = {}
    for entry in sorted(root.rglob("*")):
        name = entry.relative_to(root).as_posix()
        if entry.is_symlink():
            raise InstallError(f"Nested symlinks are not supported: {entry}")
        if entry.is_dir():
            signature[name] = ("directory", "")
        elif entry.is_file():
            signature[name] = ("file", hashlib.sha256(entry.read_bytes()).hexdigest())
        else:
            raise InstallError(f"Unsupported entry: {entry}")
    return signature


def _validate_skill(
    skill: Path,
    reference_root: Path,
    require_metadata: bool,
    validate_references: bool = True,
) -> Path:
    if skill.is_symlink() or not skill.is_dir():
        raise InstallError(f"Invalid skill directory: {skill}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name):
        raise InstallError(f"Invalid skill directory name: {skill}")
    tree_signature(skill)

    entry = skill / "SKILL.md"
    if not entry.is_file():
        raise InstallError(f"Missing SKILL.md: {skill}")
    text = entry.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
    if not frontmatter:
        raise InstallError(f"Missing frontmatter: {entry}")
    fields = frontmatter.group(1)
    if not re.search(rf"^name:\s*{re.escape(skill.name)}\s*$", fields, re.M):
        raise InstallError(f"Skill name must match directory: {entry}")
    if not re.search(r"^description:\s*\S.+$", fields, re.M):
        raise InstallError(f"Missing description: {entry}")

    if require_metadata:
        metadata = skill / "agents/openai.yaml"
        if not metadata.is_file():
            raise InstallError(f"Missing OpenAI skill metadata: {metadata}")
        metadata_text = metadata.read_text(encoding="utf-8")
        required_metadata = (
            (r"^\s*display_name:\s*.+$", "display_name"),
            (r"^\s*short_description:\s*.+$", "short_description"),
            (r"^\s*default_prompt:\s*.+$", "default_prompt"),
            (r"^\s*allow_implicit_invocation:\s*(?:true|false)\s*$", "allow_implicit_invocation"),
        )
        for pattern, field in required_metadata:
            if not re.search(pattern, metadata_text, re.M):
                raise InstallError(f"Missing or invalid {field} in {metadata}")

    if validate_references:
        root = reference_root.resolve()
        for document in sorted(skill.rglob("*.md")):
            for href in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", document.read_text(encoding="utf-8")):
                if href.startswith("#") or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", href):
                    continue
                target = (document.parent / href.split("#", 1)[0]).resolve()
                if not target.is_relative_to(root) or not target.is_file():
                    raise InstallError(f"Broken or external local reference in {document}: {href}")
    return skill


def validate_skills(skills_root: Path) -> list[Path]:
    """Validate locally-owned skills. Kept as a public helper for tests and tooling."""
    if not skills_root.is_dir():
        raise InstallError(f"Missing skills directory: {skills_root}")
    skills = sorted(path for path in skills_root.iterdir() if path.is_dir() or path.is_symlink())
    if not skills:
        raise InstallError("No local skills found.")
    return [_validate_skill(skill, skills_root, require_metadata=True) for skill in skills]


def load_upstream_skills(repository_root: Path) -> tuple[list[Path], Path]:
    manifest_path = repository_root / MANIFEST_NAME
    if not manifest_path.is_file():
        raise InstallError(f"Missing skill manifest: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        upstream = manifest["upstream"]
        upstream_root = repository_root / upstream["path"]
        relative_skills = upstream["skills"]
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise InstallError(f"Invalid skill manifest: {manifest_path}") from error

    if not isinstance(relative_skills, list) or not relative_skills:
        raise InstallError(f"No upstream skills selected in {manifest_path}")
    if not upstream_root.is_dir():
        raise InstallError(
            f"Pinned upstream checkout is not initialized: {upstream_root}\n"
            "Run: git submodule update --init --recursive"
        )

    selected = []
    seen = set()
    for relative in relative_skills:
        if not isinstance(relative, str) or not relative:
            raise InstallError(f"Invalid upstream skill path in {manifest_path}: {relative!r}")
        skill = (upstream_root / relative).resolve()
        if not skill.is_relative_to(upstream_root.resolve()):
            raise InstallError(f"Upstream skill escapes checkout: {relative}")
        validated = _validate_skill(
            skill,
            upstream_root,
            require_metadata=False,
            validate_references=False,
        )
        if validated.name in seen:
            raise InstallError(f"Duplicate upstream skill name: {validated.name}")
        seen.add(validated.name)
        selected.append(validated)
    return sorted(selected, key=lambda path: path.name), upstream_root


def load_install_skills(repository_root: Path) -> tuple[list[Path], list[Path]]:
    local_root = repository_root / "skills"
    local = validate_skills(local_root)
    upstream, upstream_root = load_upstream_skills(repository_root)

    by_name = {}
    for skill in [*local, *upstream]:
        previous = by_name.get(skill.name)
        if previous is not None:
            raise InstallError(
                f"Skill name collision: {skill.name}\n"
                f"Local/upstream composition must choose exactly one source.\n"
                f"{previous}\n{skill}"
            )
        by_name[skill.name] = skill

    return [by_name[name] for name in sorted(by_name)], [local_root, upstream_root]


def _resolved_link_target(destination: Path) -> Path | None:
    if not destination.is_symlink():
        return None
    raw = destination.readlink()
    target = raw if raw.is_absolute() else destination.parent / raw
    return target.resolve(strict=False)


def _is_managed_skill_link(destination: Path, managed_roots: list[Path]) -> bool:
    target = _resolved_link_target(destination)
    if target is None:
        return False
    for root in managed_roots:
        resolved_root = root.resolve(strict=False)
        if target == resolved_root or target.is_relative_to(resolved_root):
            return True
    return False


def plan_action(
    source: Path,
    destination: Path,
    adopt_identical: bool,
    adopt_instructions: bool = False,
    managed_skill_roots: list[Path] | None = None,
) -> Action:
    for parent in destination.parents:
        if (parent.exists() or parent.is_symlink()) and not parent.is_dir():
            raise InstallError(f"Parent path is not a directory: {parent}")

    if destination.is_symlink():
        try:
            if destination.resolve() == source:
                return Action(source, destination, "unchanged")
        except (OSError, RuntimeError):
            pass

        if managed_skill_roots and _is_managed_skill_link(destination, managed_skill_roots):
            return Action(
                source,
                destination,
                "retarget",
                previous_link=destination.readlink(),
            )

    if not destination.exists() and not destination.is_symlink():
        return Action(source, destination, "create")

    if source.is_dir() and adopt_identical and destination.is_dir():
        if tree_signature(destination) == tree_signature(source):
            return Action(source, destination, "adopt")
    elif source.is_file() and destination.is_file():
        existing = destination.read_bytes()
        common = source.read_bytes()
        if adopt_identical and existing == common:
            return Action(source, destination, "adopt", existing)
        if adopt_instructions:
            old_text = existing.decode("utf-8").strip()
            common_text = common.decode("utf-8").strip()
            if old_text and f"\n{old_text}\n" in f"\n{common_text}\n":
                return Action(source, destination, "adopt", existing)

    raise InstallError(
        f"Existing entry blocks installation: {destination}\n"
        "--adopt-identical accepts only complete content matches.\n"
        "--adopt-instructions accepts only global instruction files whose entire "
        "non-empty text is already contained in instructions/common.md."
    )


def plan_install_sources(
    skills: list[Path],
    home: Path,
    adopt_identical: bool,
    adopt_instructions: bool = False,
    managed_skill_roots: list[Path] | None = None,
) -> list[Action]:
    repository_root = Path(__file__).resolve().parent
    common = repository_root / "instructions/common.md"
    if common.is_symlink() or not common.is_file() or not common.read_text(encoding="utf-8").strip():
        raise InstallError(f"Missing, empty, or symlinked common instructions: {common}")

    actions = []
    for target_root in TARGET_ROOTS:
        for skill in skills:
            destination = home / target_root / skill.name
            actions.append(
                plan_action(
                    skill,
                    destination,
                    adopt_identical,
                    managed_skill_roots=managed_skill_roots,
                )
            )
    for target in INSTRUCTION_TARGETS:
        actions.append(plan_action(common, home / target, adopt_identical, adopt_instructions))
    return actions


def plan_install(
    skills_root: Path,
    home: Path,
    adopt_identical: bool,
    adopt_instructions: bool = False,
) -> list[Action]:
    """Backwards-compatible local-only planner used by tests and migrations."""
    skills = validate_skills(skills_root)
    repository_root = skills_root.parent
    common = repository_root / "instructions/common.md"
    if common.is_symlink() or not common.is_file() or not common.read_text(encoding="utf-8").strip():
        raise InstallError(f"Missing, empty, or symlinked common instructions: {common}")

    actions = []
    for target_root in TARGET_ROOTS:
        for skill in skills:
            actions.append(
                plan_action(
                    skill,
                    home / target_root / skill.name,
                    adopt_identical,
                    managed_skill_roots=[skills_root],
                )
            )
    for target in INSTRUCTION_TARGETS:
        actions.append(plan_action(common, home / target, adopt_identical, adopt_instructions))
    return actions


def verify_install(actions: list[Action]) -> None:
    """Every managed entry must be a live symlink to its selected source."""
    for action in actions:
        destination = action.destination
        if not destination.is_symlink():
            raise InstallError(f"Installed entry is not a symlink: {destination}")
        try:
            target = destination.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise InstallError(f"Installed symlink cannot be resolved: {destination}") from error
        if target != action.source:
            raise InstallError(
                f"Installed symlink points to the wrong source: {destination}\n"
                f"Expected: {action.source}\nActual: {target}"
            )


def apply_install(actions: list[Action], home: Path) -> Path | None:
    backup_root = None
    if any(action.kind == "adopt" for action in actions):
        backup_parent = home / ".local/share/agent-skills/backups"
        backup_parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-")
        backup_root = Path(tempfile.mkdtemp(prefix=stamp, dir=backup_parent))

    changes: list[tuple[Path, Path | None, Path | None]] = []
    try:
        for action in actions:
            if action.kind == "unchanged":
                continue

            destination = action.destination
            destination.parent.mkdir(parents=True, exist_ok=True)
            backup = None
            previous_link = action.previous_link

            if action.kind == "adopt":
                if action.expected_bytes is not None and destination.read_bytes() != action.expected_bytes:
                    raise InstallError(f"Instruction file changed after preflight: {destination}")
                backup = backup_root / destination.relative_to(home)
                backup.parent.mkdir(parents=True, exist_ok=True)
                destination.rename(backup)
            elif action.kind == "retarget":
                destination.unlink()

            changes.append((destination, backup, previous_link))
            destination.symlink_to(action.source, target_is_directory=action.source.is_dir())

        verify_install(actions)
    except BaseException as error:
        rollback_errors = []
        for destination, backup, previous_link in reversed(changes):
            try:
                if destination.exists() or destination.is_symlink():
                    destination.unlink()
                if backup is not None:
                    backup.rename(destination)
                elif previous_link is not None:
                    destination.symlink_to(previous_link, target_is_directory=True)
            except OSError as rollback_error:
                rollback_errors.append(str(rollback_error))
        if rollback_errors:
            raise InstallError(
                f"Installation failed: {error}\n"
                f"Recovery errors: {rollback_errors}\nBackups: {backup_root}"
            ) from error
        raise
    return backup_root


def find_stale_managed_skill_links(
    home: Path,
    managed_roots: Path | list[Path],
    current_skill_names: set[str],
) -> list[Path]:
    """Find obsolete skill symlinks owned by this repository."""
    roots = [managed_roots] if isinstance(managed_roots, Path) else managed_roots
    resolved_roots = [root.resolve(strict=False) for root in roots]
    stale = []

    for target_root in TARGET_ROOTS:
        installed_root = home / target_root
        if not installed_root.is_dir():
            continue
        for destination in installed_root.iterdir():
            if not destination.is_symlink() or destination.name in current_skill_names:
                continue
            target = _resolved_link_target(destination)
            if target is None:
                continue
            if any(target == root or target.is_relative_to(root) for root in resolved_roots):
                stale.append(destination)
    return sorted(stale)


def remove_stale_managed_skill_links(paths: list[Path]) -> None:
    for path in paths:
        path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(), help="Install for this home directory.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Validate and show the plan without writing.")
    mode.add_argument(
        "--verify",
        action="store_true",
        help="Check installed symlinks against the local+upstream manifest; do not write.",
    )
    parser.add_argument(
        "--adopt-identical",
        action="store_true",
        help="Back up and replace existing entries only when all contents are identical.",
    )
    parser.add_argument(
        "--adopt-instructions",
        action="store_true",
        help="Back up and adopt global instruction files only when their entire non-empty "
             "text is already contained in instructions/common.md.",
    )
    args = parser.parse_args()

    if args.verify and (args.adopt_identical or args.adopt_instructions):
        parser.error("--verify cannot be combined with adoption options.")

    home = args.home.expanduser().resolve()
    repository_root = Path(__file__).resolve().parent

    try:
        skills, managed_roots = load_install_skills(repository_root)
        actions = plan_install_sources(
            skills,
            home,
            args.adopt_identical,
            args.adopt_instructions,
            managed_skill_roots=managed_roots,
        )
        current_skill_names = {skill.name for skill in skills}
        stale_links = find_stale_managed_skill_links(home, managed_roots, current_skill_names)

        if args.verify:
            verify_install(actions)
            if stale_links:
                raise InstallError(
                    "Stale managed skill symlinks remain: " + ", ".join(map(str, stale_links))
                )
            print(f"Verified {len(actions)} symlinks; upstream manifest is consistent.")
            return 0

        for action in actions:
            print(f"{action.kind:9} {action.destination} -> {action.source}")
        for destination in stale_links:
            print(f"{'remove':9} {destination}")

        if args.dry_run:
            print("Dry run complete; no symlink changes made.")
            return 0

        backup_root = apply_install(actions, home)
        remove_stale_managed_skill_links(stale_links)

        if backup_root is not None:
            print(f"Previous entries backed up to: {backup_root}")
        print(f"Verified {len(actions)} symlinks (local + pinned upstream skills + global instructions).")
        return 0
    except (InstallError, OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
