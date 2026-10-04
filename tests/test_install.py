import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import install


ROOTS = (".agents/skills", ".codex/skills", ".claude/skills", ".cursor/skills")


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home"
        self.skills = self.root / "checkout" / "skills"
        (self.skills / "alpha/references").mkdir(parents=True)
        (self.skills / "beta").mkdir()
        (self.skills / "alpha/SKILL.md").write_text(
            "---\nname: alpha\ndescription: First fixture skill.\n---\n"
            "[Guide](references/planning.md)\n[Sibling](../beta/SKILL.md)\n"
        )
        (self.skills / "alpha/references/planning.md").write_text("A supporting guide.\n")
        (self.skills / "beta/SKILL.md").write_text(
            "---\nname: beta\ndescription: Second fixture skill.\n---\n"
            "[Sibling](../alpha/SKILL.md)\n"
        )
        self.common = self.skills.parent / "instructions/common.md"
        self.common.parent.mkdir()
        self.common.write_text(
            "# Engineering Rules\n\n- Inspect relevant code.\n\n"
            "# Code Navigation\n\n- Use native search.\n"
        )

    def actions(self, adopt=False, adopt_instructions=False):
        return install.plan_install(self.skills, self.home, adopt, adopt_instructions)

    def destinations(self):
        return [self.home / root / name for root in ROOTS
                for name in ("alpha", "beta")] + self.instruction_destinations()

    def instruction_destinations(self):
        return [self.home / target for target in install.INSTRUCTION_TARGETS]

    def assert_installed(self):
        for destination in self.destinations():
            self.assertTrue(destination.is_symlink())
            if destination in self.instruction_destinations():
                self.assertEqual(destination.resolve(), self.common)
                self.assertEqual(destination.read_bytes(), self.common.read_bytes())
            else:
                self.assertEqual(destination.resolve(), self.skills / destination.name)
        for root in ROOTS:
            alpha = self.home / root / "alpha"
            self.assertTrue((alpha / "references/planning.md").is_file())
            self.assertTrue((alpha / "../beta/SKILL.md").is_file())

    def test_packaged_skills_have_valid_names_and_local_references(self):
        skills = install.validate_skills(Path(install.__file__).resolve().parent / "skills")
        self.assertGreaterEqual(len(skills), 2)

    def test_fresh_install_preserves_references(self):
        self.assertIsNone(install.apply_install(self.actions(), self.home))
        self.assert_installed()
        self.assertFalse((self.home / ".local/share/agent-skills/backups").exists())

    def test_repeat_install_does_not_replace_existing_links(self):
        install.apply_install(self.actions(), self.home)
        before = [p.lstat().st_ino for p in self.destinations()]
        actions = self.actions()
        self.assertTrue(all(action.kind == "unchanged" for action in actions))
        install.apply_install(actions, self.home)
        self.assertEqual(before, [p.lstat().st_ino for p in self.destinations()])

    def test_source_update_is_visible_without_reinstall(self):
        install.apply_install(self.actions(), self.home)
        document = self.skills / "alpha/SKILL.md"
        updated = document.read_text() + "\nAn updated instruction.\n"
        document.write_text(updated)
        for root in ROOTS:
            self.assertEqual((self.home / root / "alpha/SKILL.md").read_text(), updated)
        self.common.write_text(self.common.read_text() + "\n- Verify side effects.\n")
        for destination in self.instruction_destinations():
            self.assertEqual(destination.read_bytes(), self.common.read_bytes())

    def test_conflict_is_found_before_any_link_is_created(self):
        conflict = self.home / ".cursor/skills/beta"
        conflict.mkdir(parents=True)
        original = conflict / "keep.txt"
        original.write_text("unrelated skill")
        with self.assertRaises(install.InstallError):
            self.actions()
        self.assertEqual(original.read_text(), "unrelated skill")
        for destination in self.destinations():
            self.assertFalse(destination.is_symlink())

    def test_identical_existing_directory_requires_explicit_adoption(self):
        existing = self.home / ".codex/skills/alpha"
        shutil.copytree(self.skills / "alpha", existing)
        with self.assertRaises(install.InstallError):
            self.actions()
        self.assertFalse(existing.is_symlink())

    def test_adoption_preserves_originals_and_retargets_old_aliases(self):
        originals = {}
        for name in ("alpha", "beta"):
            old = self.home / ".codex/skills" / name
            shutil.copytree(self.skills / name, old)
            originals[name] = install.tree_signature(old)
            for root in (".agents/skills", ".claude/skills", ".cursor/skills"):
                alias = self.home / root / name
                alias.parent.mkdir(parents=True, exist_ok=True)
                alias.symlink_to(old, target_is_directory=True)
        backup = install.apply_install(self.actions(adopt=True), self.home)
        self.assert_installed()
        for name, signature in originals.items():
            saved = backup / ".codex/skills" / name
            self.assertFalse(saved.is_symlink())
            self.assertEqual(install.tree_signature(saved), signature)
            self.assertTrue((backup / ".agents/skills" / name).is_symlink())
        (self.skills / "alpha/SKILL.md").write_text("updated source")
        self.assertEqual(install.tree_signature(backup / ".codex/skills/alpha"), originals["alpha"])

    def test_adoption_rejects_changed_contents(self):
        existing = self.home / ".codex/skills/alpha"
        shutil.copytree(self.skills / "alpha", existing)
        document = existing / "SKILL.md"
        document.write_text(document.read_text() + "\nLocal edits.\n")
        with self.assertRaises(install.InstallError):
            self.actions(adopt=True)
        self.assertTrue(document.read_text().endswith("Local edits.\n"))
        self.assertFalse((self.home / ".agents").exists())

    def test_dangling_symlink_is_never_adopted(self):
        existing = self.home / ".cursor/skills/beta"
        existing.parent.mkdir(parents=True)
        existing.symlink_to(self.root / "missing", target_is_directory=True)
        with self.assertRaises(install.InstallError):
            self.actions(adopt=True)
        self.assertTrue(existing.is_symlink())
        self.assertFalse((self.home / ".agents").exists())

    def test_broken_reference_stops_before_home_is_created(self):
        (self.skills / "alpha/references/planning.md").unlink()
        with self.assertRaises(install.InstallError):
            self.actions()
        self.assertFalse(self.home.exists())

    def test_nested_source_symlinks_are_rejected(self):
        external = self.root / "outside.txt"
        external.write_text("external")
        (self.skills / "alpha/linked.txt").symlink_to(external)
        with self.assertRaises(install.InstallError):
            self.actions()
        self.assertFalse(self.home.exists())

    def test_dry_run_makes_no_changes(self):
        script = self.skills.parent / "install.py"
        shutil.copyfile(install.__file__, script)
        with patch.object(install, "__file__", str(script)), \
                patch("sys.argv", ["install.py", "--home", str(self.home), "--dry-run"]), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(install.main(), 0)
        self.assertFalse(self.home.exists())

    def test_failed_creation_restores_adopted_directory_and_removes_new_links(self):
        existing = self.home / ".codex/skills/alpha"
        shutil.copytree(self.skills / "alpha", existing)
        signature = install.tree_signature(existing)
        real_symlink_to = Path.symlink_to

        def fail_at_adoption(path, target, target_is_directory=False):
            if path == existing:
                raise OSError("simulated symlink failure")
            return real_symlink_to(path, target, target_is_directory=target_is_directory)

        with patch.object(Path, "symlink_to", fail_at_adoption):
            with self.assertRaisesRegex(OSError, "simulated symlink failure"):
                install.apply_install(self.actions(adopt=True), self.home)
        self.assertFalse(existing.is_symlink())
        self.assertEqual(install.tree_signature(existing), signature)
        self.assertTrue(all(not destination.is_symlink() for destination in self.destinations()))

    def test_parent_file_is_detected_before_writes(self):
        self.home.mkdir()
        (self.home / ".cursor").write_text("keep")
        with self.assertRaises(install.InstallError):
            self.actions()
        self.assertFalse((self.home / ".agents").exists())
        self.assertEqual((self.home / ".cursor").read_text(), "keep")

    def test_dangling_parent_symlink_is_detected_before_writes(self):
        self.home.mkdir()
        parent = self.home / ".cursor"
        parent.symlink_to(self.root / "missing", target_is_directory=True)
        with self.assertRaises(install.InstallError):
            self.actions()
        self.assertFalse((self.home / ".agents").exists())
        self.assertTrue(parent.is_symlink())

    def write_existing_instruction(self, text, target=".claude/CLAUDE.md"):
        destination = self.home / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text)
        return destination

    def test_instruction_conflict_stops_before_skill_links_are_created(self):
        existing = self.write_existing_instruction("- Preserve my local rule.\n")
        with self.assertRaises(install.InstallError):
            self.actions()
        self.assertEqual(existing.read_text(), "- Preserve my local rule.\n")
        self.assertFalse((self.home / ".agents").exists())

    def test_identical_instruction_requires_explicit_adoption(self):
        existing = self.write_existing_instruction(self.common.read_text())
        with self.assertRaises(install.InstallError):
            self.actions()
        backup = install.apply_install(self.actions(adopt=True), self.home)
        self.assert_installed()
        saved = backup / existing.relative_to(self.home)
        self.assertFalse(saved.is_symlink())
        self.assertEqual(saved.read_bytes(), self.common.read_bytes())

    def test_contained_instruction_is_backed_up_before_adoption(self):
        old_text = "# Code Navigation\n\n- Use native search.\n"
        existing = self.write_existing_instruction(old_text)
        with self.assertRaises(install.InstallError):
            self.actions(adopt=True)
        backup = install.apply_install(self.actions(adopt_instructions=True), self.home)
        self.assert_installed()
        self.assertEqual((backup / existing.relative_to(self.home)).read_text(), old_text)
        self.common.write_text(self.common.read_text() + "\n- Verify side effects.\n")
        self.assertEqual((backup / existing.relative_to(self.home)).read_text(), old_text)

    def test_instruction_adoption_preserves_file_alias_in_backup(self):
        original = self.root / "old-common.md"
        original.write_text(self.common.read_text())
        alias = self.home / ".claude/CLAUDE.md"
        alias.parent.mkdir(parents=True)
        alias.symlink_to(original)
        backup = install.apply_install(self.actions(adopt_instructions=True), self.home)
        self.assert_installed()
        self.assertTrue((backup / ".claude/CLAUDE.md").is_symlink())
        self.assertEqual(original.read_bytes(), self.common.read_bytes())

    def test_unrepresented_instruction_cannot_be_adopted(self):
        existing = self.write_existing_instruction("- Use native search.\n- Keep another rule.\n")
        with self.assertRaises(install.InstallError):
            self.actions(adopt_instructions=True)
        self.assertTrue(existing.read_text().endswith("- Keep another rule.\n"))
        self.assertFalse((self.home / ".agents").exists())

    def test_instruction_adoption_requires_a_whole_text_block(self):
        self.common.write_text("- Never remove local rules.\n")
        existing = self.write_existing_instruction("remove local rules.")
        with self.assertRaises(install.InstallError):
            self.actions(adopt_instructions=True)
        self.assertEqual(existing.read_text(), "remove local rules.")

    def test_empty_instruction_is_not_silently_adopted(self):
        existing = self.write_existing_instruction("\n")
        with self.assertRaises(install.InstallError):
            self.actions(adopt_instructions=True)
        self.assertEqual(existing.read_text(), "\n")

    def test_instruction_flag_does_not_adopt_existing_skills(self):
        existing = self.home / ".codex/skills/alpha"
        shutil.copytree(self.skills / "alpha", existing)
        with self.assertRaises(install.InstallError):
            self.actions(adopt_instructions=True)
        self.assertFalse(existing.is_symlink())

    def test_missing_or_invalid_common_instructions_stop_before_writes(self):
        self.common.unlink()
        with self.assertRaises(install.InstallError):
            self.actions()
        self.common.write_text("\n")
        with self.assertRaises(install.InstallError):
            self.actions()
        self.common.unlink()
        external = self.root / "external.md"
        external.write_text("- External instruction.\n")
        self.common.symlink_to(external)
        with self.assertRaises(install.InstallError):
            self.actions()
        self.assertFalse(self.home.exists())

    def test_dangling_instruction_symlink_cannot_be_adopted(self):
        existing = self.home / ".claude/CLAUDE.md"
        existing.parent.mkdir(parents=True)
        existing.symlink_to(self.root / "missing.md")
        with self.assertRaises(install.InstallError):
            self.actions(adopt=True, adopt_instructions=True)
        self.assertTrue(existing.is_symlink())
        self.assertFalse((self.home / ".agents").exists())

    def test_adoption_dry_run_preserves_original_instruction(self):
        old_text = "# Code Navigation\n\n- Use native search.\n"
        existing = self.write_existing_instruction(old_text)
        script = self.skills.parent / "install.py"
        shutil.copyfile(install.__file__, script)
        with patch.object(install, "__file__", str(script)), \
                patch("sys.argv", ["install.py", "--home", str(self.home),
                                   "--adopt-instructions", "--dry-run"]), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(install.main(), 0)
        self.assertFalse(existing.is_symlink())
        self.assertEqual(existing.read_text(), old_text)
        self.assertFalse((self.home / ".agents").exists())
        self.assertFalse((self.home / ".local").exists())

    def test_failed_instruction_install_restores_both_global_files_and_skills(self):
        originals = {}
        for target in install.INSTRUCTION_TARGETS:
            old_text = "# Code Navigation\n\n- Use native search.\n"
            originals[self.write_existing_instruction(old_text, target)] = old_text
        real_symlink_to = Path.symlink_to

        def fail_at_last_instruction(path, target, target_is_directory=False):
            if path == self.home / ".claude/CLAUDE.md":
                raise OSError("simulated global instruction failure")
            return real_symlink_to(path, target, target_is_directory=target_is_directory)

        with patch.object(Path, "symlink_to", fail_at_last_instruction):
            with self.assertRaisesRegex(OSError, "simulated global instruction failure"):
                install.apply_install(self.actions(adopt_instructions=True), self.home)
        for destination, old_text in originals.items():
            self.assertFalse(destination.is_symlink())
            self.assertEqual(destination.read_text(), old_text)
        self.assertTrue(all(not destination.is_symlink() for destination in self.destinations()))

    def test_instruction_edited_after_preflight_is_preserved(self):
        existing = self.write_existing_instruction(self.common.read_text())
        actions = self.actions(adopt=True)
        changed = self.common.read_text() + "\n- New local rule.\n"
        existing.write_text(changed)
        with self.assertRaisesRegex(install.InstallError, "changed after preflight"):
            install.apply_install(actions, self.home)
        self.assertFalse(existing.is_symlink())
        self.assertEqual(existing.read_text(), changed)
        self.assertTrue(all(not destination.is_symlink() for destination in self.destinations()))


if __name__ == "__main__":
    unittest.main()
