import unittest

from src.wifi_survey import Measurement, collapse_radios_by_physical_ap, roaming_summary, rssi_quality


class WifiSurveyTests(unittest.TestCase):
    def test_radio_collapse_keeps_strongest_radio_from_same_ap(self):
        rows = [
            Measurement("A", "ap1-r1", "AP-1", 5.0, -70, 40),
            Measurement("A", "ap1-r2", "AP-1", 5.0, -55, 149),
            Measurement("A", "ap2-r1", "AP-2", 5.0, -65, 100),
        ]
        self.assertEqual(collapse_radios_by_physical_ap(rows)["A"], {"AP-1": -55, "AP-2": -65})

    def test_roaming_candidate_requires_distinct_physical_aps(self):
        rows = [
            Measurement("A", "ap1-r1", "AP-1", 5.0, -50, 40),
            Measurement("A", "ap1-r2", "AP-1", 5.0, -52, 149),
            Measurement("A", "ap2-r1", "AP-2", 5.0, -62, 100),
        ]
        summary = roaming_summary(rows)[0]
        self.assertEqual(summary["top1_ap"], "AP-1")
        self.assertEqual(summary["top2_ap"], "AP-2")
        self.assertTrue(summary["roaming_overlap_candidate"])

    def test_weak_secondary_is_not_candidate(self):
        rows = [
            Measurement("A", "a", "AP-1", 5.0, -55, 40),
            Measurement("A", "b", "AP-2", 5.0, -80, 100),
        ]
        self.assertFalse(roaming_summary(rows)[0]["roaming_overlap_candidate"])

    def test_rssi_quality_bands(self):
        self.assertEqual(rssi_quality(-55), "strong")
        self.assertEqual(rssi_quality(-66), "good")
        self.assertEqual(rssi_quality(-75), "edge")
        self.assertEqual(rssi_quality(-85), "weak")


if __name__ == "__main__":
    unittest.main()
