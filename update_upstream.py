#!/usr/bin/env python3
"""Check or move the Matt Pocock skills submodule to the latest upstream main commit."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import install


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update",
        action="store_true",
        help="Checkout origin/main in the submodule after fetching. Without this flag, only check.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    upstream = root / "upstream/mattpocock-skills"

    try:
        if not (upstream / ".git").exists():
            run("git", "submodule", "update", "--init", "--recursive", cwd=root)

        current = run("git", "rev-parse", "HEAD", cwd=upstream)
        run("git", "fetch", "origin", "main", cwd=upstream)
        latest = run("git", "rev-parse", "origin/main", cwd=upstream)

        print(f"Current checkout: {current}")
        print(f"Latest origin/main: {latest}")

        if current == latest:
            print("Upstream is already current.")
            return 0

        if not args.update:
            print("Update available. Run: python3 update_upstream.py --update")
            return 0

        run("git", "checkout", "--detach", latest, cwd=upstream)
        selected, _ = install.load_upstream_skills(root)
        print(f"Checked out {latest} and validated {len(selected)} selected upstream skills.")
        print("Next:")
        print("  git diff --submodule=log")
        print("  python3 -m unittest discover -s tests -v")
        print("  python3 install.py --dry-run")
        print("  git add upstream/mattpocock-skills")
        print('  git commit -m "Update Matt skills upstream"')
        return 0
    except (install.InstallError, OSError, subprocess.SubprocessError) as error:
        print(f"Upstream update stopped: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
