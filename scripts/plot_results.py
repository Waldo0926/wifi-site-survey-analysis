from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt

from src.wifi_survey import channel_observations, load_measurements, roaming_summary

ROOT = Path(__file__).resolve().parents[1]
MEASUREMENTS = load_measurements(ROOT / "data" / "survey_measurements.csv")
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def plot_rssi() -> None:
    by_point: dict[str, list[int]] = defaultdict(list)
    for m in MEASUREMENTS:
        if m.band_ghz == 5.0:
            by_point[m.point].append(m.rssi_dbm)
    points = sorted(by_point)
    strongest = [max(by_point[p]) for p in points]
    plt.figure(figsize=(8, 4.5))
    plt.bar(points, strongest)
    plt.axhline(-67, linestyle="--", linewidth=1, label="reference: -67 dBm")
    plt.axhline(-75, linestyle=":", linewidth=1, label="reference: -75 dBm")
    plt.xlabel("Anonymised survey point")
    plt.ylabel("Strongest 5 GHz RSSI (dBm)")
    plt.title("Strongest observed 5 GHz signal by survey point")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "strongest_rssi_by_point.png", dpi=160)
    plt.close()


def plot_roaming_margin() -> None:
    rows = roaming_summary(MEASUREMENTS)
    rows = [r for r in rows if r["delta_db"] is not None]
    points = [str(r["point"]) for r in rows]
    deltas = [int(r["delta_db"]) for r in rows]
    plt.figure(figsize=(8, 4.5))
    plt.bar(points, deltas)
    plt.axhline(15, linestyle="--", linewidth=1, label="candidate threshold: 15 dB")
    plt.xlabel("Anonymised survey point")
    plt.ylabel("Top-1 vs Top-2 physical AP RSSI delta (dB)")
    plt.title("Cross-AP roaming margin after radio de-duplication")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "roaming_delta_by_point.png", dpi=160)
    plt.close()


def plot_channels() -> None:
    counts = channel_observations(MEASUREMENTS)
    channels = sorted(counts)
    values = [counts[ch] for ch in channels]
    plt.figure(figsize=(8, 4.5))
    plt.bar([str(c) for c in channels], values)
    plt.xlabel("5 GHz channel")
    plt.ylabel("Number of observations")
    plt.title("Observed 5 GHz channel usage in the sanitised survey")
    plt.tight_layout()
    plt.savefig(RESULTS / "channel_observations.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    plot_rssi()
    plot_roaming_margin()
    plot_channels()
