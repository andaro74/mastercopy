"""The gate the CI job consumes: the validator CLI, exercised end to end.

A schema is only a gate if it can fail. These tests assert the CLI exits
nonzero on each way a verdict can lie, so the M00a gate is demonstrably red
before it is green.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATOR = REPO_ROOT / "tools" / "validate_verdict.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_validator(path):
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


class VerdictGateTests(unittest.TestCase):
    def test_valid_verdict_exits_zero(self):
        result = run_validator(FIXTURES / "valid-verdict.json")

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS", result.stdout)

    def test_every_bad_fixture_exits_nonzero(self):
        bad_fixtures = sorted(FIXTURES.glob("bad-*.json"))
        self.assertTrue(bad_fixtures, "no bad fixtures found to prove the gate fails")

        for fixture in bad_fixtures:
            with self.subTest(fixture=fixture.name):
                result = run_validator(fixture)

                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("FAIL", result.stdout)

    def test_missing_file_exits_nonzero(self):
        result = run_validator(FIXTURES / "does-not-exist.json")

        self.assertEqual(result.returncode, 1, result.stdout)

    def test_recorded_history_still_validates(self):
        """Every verdict ever committed must still satisfy the frozen schema."""
        history = sorted((REPO_ROOT / "evals" / "history").glob("*.json"))

        for verdict_file in history:
            with self.subTest(verdict=verdict_file.name):
                result = run_validator(verdict_file)

                self.assertEqual(result.returncode, 0, result.stdout)


class FixtureIntegrityTests(unittest.TestCase):
    def test_valid_fixture_matches_spec_example_fields(self):
        """The fixture is the worked example SPEC-00 documents."""
        verdict = json.loads(
            (FIXTURES / "valid-verdict.json").read_text(encoding="utf-8")
        )

        self.assertEqual(verdict["ladder_source"], "default")
        self.assertEqual(verdict["totals"]["bits_vs_default_pct"], 0.0)
        self.assertEqual(verdict["totals"]["usd_vs_default_pct"], 0.0)


if __name__ == "__main__":
    unittest.main()
