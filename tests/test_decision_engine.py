
import unittest

from decision_engine import compare_hotspots


def make_report(
    hotspot_id,
    temperature,
    data_status="synthetic",
    evidence_status="synthetic",
):
    return {
        "status": "FOUND",
        "hotspot": {
            "id": hotspot_id,
            "name": f"Test Hotspot {hotspot_id}",
            "temperature_c": temperature,
            "measurement_date": "2026-10-10",
            "data_status": data_status,
        },
        "evidence": [
            {
                "id": f"evidence_{hotspot_id}",
                "name": "Test evidence",
                "data_status": evidence_status,
            }
        ],
    }


class DecisionEngineTests(unittest.TestCase):

    def test_synthetic_data_never_selects_winner(self):
        report_a = make_report("a", 42.0)
        report_b = make_report("b", 35.0)

        result = compare_hotspots(report_a, report_b)

        self.assertEqual(
            result["status"], "INSUFFICIENT_EVIDENCE"
        )
        self.assertIsNone(result["winner"])

    def test_unverified_hotspot_never_selects_winner(self):
        report_a = make_report(
            "a", 42.0, data_status="unverified"
        )
        report_b = make_report(
            "b", 35.0, data_status="verified",
            evidence_status="verified"
        )

        result = compare_hotspots(report_a, report_b)

        self.assertEqual(
            result["status"], "INSUFFICIENT_EVIDENCE"
        )
        self.assertIsNone(result["winner"])

    def test_missing_hotspot_never_selects_winner(self):
        report_a = {
            "status": "NOT_FOUND",
            "hotspot_id": "missing",
        }
        report_b = make_report("b", 35.0)

        result = compare_hotspots(report_a, report_b)

        self.assertEqual(
            result["status"], "INSUFFICIENT_EVIDENCE"
        )
        self.assertIsNone(result["winner"])


if __name__ == "__main__":
    unittest.main()
