"""The hooks are load-bearing, so they get tests like anything else."""

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / ".claude" / "hooks"))

import guard_bash  # noqa: E402
import pre_commit  # noqa: E402


TABLE_HEADER = (
    "| M | Milestone | Branch | Tag | Golden titles | VMAF envelope "
    "| $ journaled | Status |\n"
    "|---|-----------|--------|-----|---------------|---------------"
    "|-------------|--------|\n"
)


class ReadmeTableGuardTests(unittest.TestCase):
    def test_placeholder_row_is_allowed(self):
        markdown = TABLE_HEADER + (
            "| 00a | Foundation | `m00a-foundation` | `m00a` | n/a | n/a | – | ⬜ |\n"
        )

        self.assertEqual(pre_commit.table_violations(markdown, REPO_ROOT), [])

    def test_number_without_an_artifact_is_refused(self):
        markdown = TABLE_HEADER + (
            "| 03 | Evals | `m03-evals` | `m03` | 12/12 | 93.1 | $41.20 | ✅ |\n"
        )

        violations = pre_commit.table_violations(markdown, REPO_ROOT)

        self.assertEqual(len(violations), 1)
        self.assertIn("no linked artifact", violations[0])

    def test_number_with_a_link_to_a_missing_artifact_is_refused(self):
        markdown = TABLE_HEADER + (
            "| 03 | Evals | `m03-evals` | `m03` | "
            "[12/12](evals/history/never-ran.json) | – | – | ✅ |\n"
        )

        violations = pre_commit.table_violations(markdown, REPO_ROOT)

        self.assertEqual(len(violations), 1)

    def test_number_with_a_real_artifact_is_allowed(self):
        # tests/fixtures/valid-verdict.json stands in for a recorded run; the
        # rule is about the link resolving, not about which file it points to.
        markdown = TABLE_HEADER + (
            "| 00a | Foundation | `m00a-foundation` | `m00a` | n/a | n/a | "
            "[$0.00](milestones/M00a/journal.md) | ⬜ |\n"
        )

        self.assertEqual(pre_commit.table_violations(markdown, REPO_ROOT), [])

    def test_branch_and_tag_columns_do_not_trip_the_digit_check(self):
        """`m00a` is full of digits and is not a claim about results."""
        markdown = TABLE_HEADER + (
            "| 07 | Live capstone | `m07-live` | `m07` | – | – | – | ⬜ |\n"
        )

        self.assertEqual(pre_commit.table_violations(markdown, REPO_ROOT), [])

    def test_missing_table_is_a_warning_not_a_block(self):
        self.assertEqual(pre_commit.table_violations("# no table here", REPO_ROOT), [])


class LiveReadmeTests(unittest.TestCase):
    def test_committed_readme_passes_its_own_guard(self):
        markdown = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertEqual(pre_commit.table_violations(markdown, REPO_ROOT), [])


class DispatcherMatchingTests(unittest.TestCase):
    """The dispatcher must fire on commands and not on prose about commands."""

    def test_guarded_command_is_matched(self):
        self.assertEqual(guard_bash.guards_for("make deploy-dev"), ["pre_deploy.py"])

    def test_guarded_command_after_a_separator_is_matched(self):
        self.assertEqual(
            guard_bash.guards_for("uv sync && cdk deploy --context stage=dev"),
            ["pre_deploy.py"],
        )

    def test_commit_is_matched(self):
        self.assertEqual(guard_bash.guards_for('git commit -m "x"'), ["pre_commit.py"])

    def test_teardown_is_never_guarded(self):
        self.assertEqual(guard_bash.guards_for("make destroy-dev"), [])

    def test_unrelated_command_is_not_guarded(self):
        self.assertEqual(guard_bash.guards_for("ls -la && uv run pytest"), [])

    def test_documentation_inside_a_heredoc_does_not_trip_the_guard(self):
        """The bug that found this rule: writing docs about a guarded command."""
        command = "\n".join(
            [
                "cat > README.md <<'EOF'",
                "Run `make deploy-dev` after the budget exists.",
                "Then git commit the result.",
                "EOF",
                "echo done",
            ]
        )

        self.assertEqual(guard_bash.guards_for(command), [])

    def test_quoted_mention_is_not_a_command_position(self):
        self.assertEqual(guard_bash.guards_for('echo "make deploy-dev"'), [])

    def test_heredoc_stripping_keeps_commands_after_the_delimiter(self):
        command = "\n".join(
            ["cat > f <<'EOF'", "irrelevant text", "EOF", "make deploy-dev"]
        )

        self.assertEqual(guard_bash.guards_for(command), ["pre_deploy.py"])


if __name__ == "__main__":
    unittest.main()
