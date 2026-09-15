from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Measurement:
    point: str
    radio_id: str
    physical_ap: str
    band_ghz: float
    rssi_dbm: int
    channel: int


def load_measurements(path: str | Path) -> list[Measurement]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        return [
            Measurement(
                point=row["point"],
                radio_id=row["radio_id"],
                physical_ap=row["physical_ap"],
                band_ghz=float(row["band_ghz"]),
                rssi_dbm=int(row["rssi_dbm"]),
                channel=int(row["channel"]),
            )
            for row in rows
        ]


def rssi_quality(rssi_dbm: int) -> str:
    if rssi_dbm >= -60:
        return "strong"
    if rssi_dbm >= -70:
        return "good"
    if rssi_dbm >= -80:
        return "edge"
    return "weak"


def collapse_radios_by_physical_ap(
    measurements: list[Measurement], *, band_ghz: float = 5.0
) -> dict[str, dict[str, int]]:
    """Return point -> physical AP -> strongest RSSI for that AP on the selected band."""
    collapsed: dict[str, dict[str, int]] = defaultdict(dict)
    for m in measurements:
        if m.band_ghz != band_ghz:
            continue
        previous = collapsed[m.point].get(m.physical_ap)
        if previous is None or m.rssi_dbm > previous:
            collapsed[m.point][m.physical_ap] = m.rssi_dbm
    return dict(collapsed)


def roaming_summary(
    measurements: list[Measurement],
    *,
    band_ghz: float = 5.0,
    min_secondary_rssi: int = -75,
    max_delta_db: int = 15,
) -> list[dict[str, object]]:
    """Assess cross-AP roaming overlap after collapsing radios from the same physical AP."""
    collapsed = collapse_radios_by_physical_ap(measurements, band_ghz=band_ghz)
    summaries: list[dict[str, object]] = []
    for point in sorted(collapsed):
        ranked = sorted(collapsed[point].items(), key=lambda item: item[1], reverse=True)
        top1_ap, top1_rssi = ranked[0]
        if len(ranked) >= 2:
            top2_ap, top2_rssi = ranked[1]
            delta = abs(top1_rssi - top2_rssi)
            candidate = top2_rssi >= min_secondary_rssi and delta <= max_delta_db
        else:
            top2_ap, top2_rssi, delta, candidate = None, None, None, False
        summaries.append(
            {
                "point": point,
                "top1_ap": top1_ap,
                "top1_rssi_dbm": top1_rssi,
                "top2_ap": top2_ap,
                "top2_rssi_dbm": top2_rssi,
                "delta_db": delta,
                "roaming_overlap_candidate": candidate,
            }
        )
    return summaries


def channel_observations(
    measurements: list[Measurement], *, band_ghz: float = 5.0
) -> Counter[int]:
    return Counter(m.channel for m in measurements if m.band_ghz == band_ghz)


def strongest_ap_by_point(
    measurements: list[Measurement], *, band_ghz: float = 5.0
) -> dict[str, tuple[str, int]]:
    collapsed = collapse_radios_by_physical_ap(measurements, band_ghz=band_ghz)
    return {
        point: max(aps.items(), key=lambda item: item[1])
        for point, aps in collapsed.items()
        if aps
    }
