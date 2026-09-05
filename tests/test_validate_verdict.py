import unittest

from tools.validate_verdict import VerdictValidationError, validate_verdict


VALID_VERDICT = {
    "run_id": "m00a-test",
    "date": "2026-09-04",
    "milestone": "m00a",
    "git_sha": "abc123",
    "ladder_source": "default",
    "titles": [
        {
            "title_id": "meridian-sports-regional-final",
            "content_class": "sports",
            "renditions": [
                {
                    "rung": "1080p",
                    "vmaf": 95.0,
                    "bitrate_kbps": 5000,
                    "codec": "avc",
                }
            ],
            "vmaf_min": 95.0,
            "delivered_bits_total": 1000,
            "mediaconvert_normalized_minutes": 2.0,
            "usd_actual": 0.0,
            "envelope_pass": True,
        }
    ],
    "totals": {
        "titles_pass": 1,
        "titles_total": 1,
        "bits_vs_default_pct": 0.0,
        "usd_vs_default_pct": 0.0,
    },
    "verdict": "PASS",
}


class VerdictValidationTests(unittest.TestCase):
    def test_accepts_spec_00_shape(self):
        validate_verdict(VALID_VERDICT)

    def test_rejects_missing_required_field(self):
        invalid_verdict = {**VALID_VERDICT, "verdict": "MAYBE"}

        with self.assertRaises(VerdictValidationError):
            validate_verdict(invalid_verdict)

    def test_rejects_totals_that_disagree_with_titles(self):
        invalid_verdict = {
            **VALID_VERDICT,
            "titles": [
                {**VALID_VERDICT["titles"][0], "envelope_pass": False},
            ],
        }

        with self.assertRaises(VerdictValidationError):
            validate_verdict(invalid_verdict)

    def test_rejects_non_string_title_id(self):
        invalid_verdict = {
            **VALID_VERDICT,
            "titles": [{**VALID_VERDICT["titles"][0], "title_id": ""}],
        }

        with self.assertRaises(VerdictValidationError):
            validate_verdict(invalid_verdict)

    def test_accepts_unknown_additive_fields(self):
        forward_compatible = {**VALID_VERDICT, "future_field": {"anything": 1}}

        validate_verdict(forward_compatible)

    def test_rejects_inconsistent_title_total(self):
        invalid_verdict = {
            **VALID_VERDICT,
            "totals": {**VALID_VERDICT["totals"], "titles_total": 2},
        }

        with self.assertRaises(VerdictValidationError):
            validate_verdict(invalid_verdict)


if __name__ == "__main__":
    unittest.main()
