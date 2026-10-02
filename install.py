#!/usr/bin/env python3
"""Install the repository's skills as shared, protected directory symlinks."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


TARGET_ROOTS = (".agents/skills", ".codex/skills", ".claude/skills", ".cursor/skills")


class InstallError(Exception):
    pass


@dataclass(frozen=True)
class Action:
    source: Path
    destination: Path
    kind: str


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


def validate_skills(skills_root: Path) -> list[Path]:
    if not skills_root.is_dir():
        raise InstallError(f"Missing skills directory: {skills_root}")
    skills = sorted(skills_root.iterdir())
    if not skills:
        raise InstallError("No skills found.")
    for skill in skills:
        if skill.is_symlink() or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill.name):
            raise InstallError(f"Invalid skill directory: {skill}")
        tree_signature(skill)
        entry = skill / "SKILL.md"
        if not entry.is_file():
            raise InstallError(f"Missing SKILL.md: {skill}")
        text = entry.read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
        if not frontmatter:
            raise InstallError(f"Missing frontmatter: {entry}")
        fields = frontmatter.group(1)
        if not re.search(rf"^name: {re.escape(skill.name)}\s*$", fields, re.M):
            raise InstallError(f"Skill name must match directory: {entry}")
        if not re.search(r"^description: \S.+$", fields, re.M):
            raise InstallError(f"Missing description: {entry}")
        for document in sorted(skill.rglob("*.md")):
            for href in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", document.read_text(encoding="utf-8")):
                if href.startswith("#") or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", href):
                    continue
                target = (document.parent / href.split("#", 1)[0]).resolve()
                if not target.is_relative_to(skills_root) or not target.is_file():
                    raise InstallError(f"Broken or external local reference in {document}: {href}")
    return skills


def plan_install(skills_root: Path, home: Path, adopt_identical: bool) -> list[Action]:
    skills = validate_skills(skills_root)
    signatures = {skill: tree_signature(skill) for skill in skills}
    actions = []
    for target_root in TARGET_ROOTS:
        for skill in skills:
            destination = home / target_root / skill.name
            for parent in destination.parents:
                if (parent.exists() or parent.is_symlink()) and not parent.is_dir():
                    raise InstallError(f"Parent path is not a directory: {parent}")
            if destination.is_symlink() and destination.resolve() == skill:
                kind = "unchanged"
            elif not destination.exists() and not destination.is_symlink():
                kind = "create"
            elif adopt_identical and destination.is_dir() and tree_signature(destination) == signatures[skill]:
                kind = "adopt"
            else:
                raise InstallError(
                    f"Existing entry blocks installation: {destination}\n"
                    "--adopt-identical only accepts entries whose complete contents match this repository."
                )
            actions.append(Action(skill, destination, kind))
    return actions


def apply_install(actions: list[Action], home: Path) -> Path | None:
    backup_root = None
    if any(action.kind == "adopt" for action in actions):
        backup_parent = home / ".local/share/agent-skills/backups"
        backup_parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-")
        backup_root = Path(tempfile.mkdtemp(prefix=stamp, dir=backup_parent))
    changes = []
    try:
        for action in actions:
            if action.kind == "unchanged":
                continue
            destination = action.destination
            destination.parent.mkdir(parents=True, exist_ok=True)
            backup = None
            if action.kind == "adopt":
                backup = backup_root / destination.relative_to(home)
                backup.parent.mkdir(parents=True, exist_ok=True)
                destination.rename(backup)
            changes.append((destination, backup, False))
            destination.symlink_to(action.source, target_is_directory=True)
            changes[-1] = (destination, backup, True)
        for action in actions:
            if not action.destination.is_symlink() or action.destination.resolve() != action.source:
                raise InstallError(f"Installed link failed verification: {action.destination}")
    except BaseException as error:
        rollback_errors = []
        for destination, backup, created in reversed(changes):
            try:
                if created:
                    destination.unlink()
                if backup is not None:
                    backup.rename(destination)
            except OSError as rollback_error:
                rollback_errors.append(str(rollback_error))
        if rollback_errors:
            raise InstallError(
                f"Installation failed: {error}\nRecovery errors: {rollback_errors}\nBackups: {backup_root}"
            ) from error
        raise
    return backup_root


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(), help="Install for this home directory.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and show the plan without writing.")
    parser.add_argument(
        "--adopt-identical", action="store_true",
        help="Back up and replace existing entries only when all contents are identical.",
    )
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    skills_root = Path(__file__).resolve().parent / "skills"
    try:
        actions = plan_install(skills_root, home, args.adopt_identical)
        for action in actions:
            print(f"{action.kind:9} {action.destination} -> {action.source}")
        if args.dry_run:
            print("Dry run complete; no changes made.")
            return 0
        backup_root = apply_install(actions, home)
        if backup_root is not None:
            print(f"Previous entries backed up to: {backup_root}")
        print(f"Verified {len(actions)} skill links.")
        return 0
    except (InstallError, OSError, ValueError) as error:
        print(f"Installation stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
