import contextlib
import io
import json
import os
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import faers_disproportionality as faers
import openfda_query as client


class SafetyTests(unittest.TestCase):
    def test_balanced_yates_is_zero(self):
        self.assertEqual(faers.stats(1, 1, 1, 1)["chi2_yates"], 0)
        self.assertEqual(faers.stats(10, 10, 10, 10)["chi2_yates"], 0)

    def test_known_table(self):
        result = faers.stats(20, 80, 10, 90)
        self.assertEqual(result["PRR"], 2)
        self.assertEqual(result["ROR"], 2.25)
        self.assertAlmostEqual(result["chi2_yates"], 3.18)

    def test_negative_counts_fail(self):
        with self.assertRaises(ValueError):
            faers.stats(1, -1, 2, 3)
        self.assertNotIn("PRR", faers.stats(0, 1, 2, 3))

    def test_date_range_is_encoded_once(self):
        self.assertEqual(faers.date_clause("2025-01-01", "2025-12-31"),
                         "receivedate:[20250101 TO 20251231]")
        with self.assertRaises(ValueError):
            faers.date_clause("2025-12-31", "2025-01-01")

    def test_named_comparator_excludes_target_reports(self):
        with patch.object(faers, "total", side_effect=[20, 100, 10, 100]) as total, \
             patch.object(sys, "argv", ["faers", "--drug", "target", "--events", "EVENT", "--comparator-drugs", "other"]), \
             contextlib.redirect_stdout(io.StringIO()):
            faers.main()
        for call in total.call_args_list[2:]:
            self.assertIn('AND NOT (patient.drug.openfda.generic_name:"target")', call.args[0])

    def test_404_is_only_zero_for_documented_no_matches(self):
        for module, invoke in [(faers, lambda: faers.total("x")),
                               (client, lambda: client.call("drug/event", {}))]:
            for message, expected_zero in [("No matches found!", True), ("Unknown endpoint", False)]:
                error = urllib.error.HTTPError("https://example.invalid", 404, "not found", {},
                    io.BytesIO(json.dumps({"error": {"code": "NOT_FOUND", "message": message}}).encode()))
                with patch.object(module, "user_agent", return_value={}), \
                     patch("urllib.request.urlopen", side_effect=error):
                    if expected_zero:
                        result = invoke()
                        self.assertEqual(result if module is faers else result["meta"]["results"]["total"], 0)
                    else:
                        with self.assertRaises(RuntimeError):
                            invoke()

    def test_error_does_not_expose_api_key(self):
        with patch.dict(os.environ, {"OPENFDA_API_KEY": "synthetic-secret"}), \
             patch.object(client, "user_agent", return_value={}), \
             patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError("https://example.invalid", 403, "forbidden", {}, None)):
            with self.assertRaises(RuntimeError) as error:
                client.call("drug/event", {})
            self.assertNotIn("synthetic-secret", str(error.exception))


if __name__ == "__main__":
    unittest.main()
