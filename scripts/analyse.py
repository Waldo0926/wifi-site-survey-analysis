from __future__ import annotations

import csv
from pathlib import Path

from src.wifi_survey import load_measurements, roaming_summary

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "survey_measurements.csv"
RESULTS = ROOT / "results"


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    measurements = load_measurements(DATA)
    rows = roaming_summary(measurements)
    out = RESULTS / "roaming_summary.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Loaded {len(measurements)} sanitised measurements")
    print("Cross-AP roaming overlap candidates (5 GHz):")
    for row in rows:
        marker = "YES" if row["roaming_overlap_candidate"] else "no"
        print(
            f"  {row['point']}: {row['top1_ap']} {row['top1_rssi_dbm']} dBm; "
            f"secondary={row['top2_ap']} {row['top2_rssi_dbm']} dBm; "
            f"delta={row['delta_db']} dB -> {marker}"
        )


if __name__ == "__main__":
    main()
