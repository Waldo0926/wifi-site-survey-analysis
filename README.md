# Wi-Fi Site Survey Analysis

[![Type](https://img.shields.io/badge/Type-Coursework-2563eb?style=for-the-badge)](#)
[![Tech](https://img.shields.io/badge/Tech-Python-7c3aed?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-16a34a?style=for-the-badge)](LICENSE)


**English** · [中文](README.zh-CN.md)

A post-course, privacy-safe refactor of an indoor WLAN survey: **RSSI analysis, channel observations, physical-AP-aware roaming overlap, and reproducible visualisation in Python**.

> This repository is **not the original assessment submission**. It was rebuilt after the course as a portfolio project. Real campus locations, floor plans, BSSIDs/MAC addresses, gateway addresses, packet captures, student identifiers, and other infrastructure details are intentionally excluded.

## Why this project

Wireless surveys often collect multiple BSSIDs belonging to the same physical AP. A naive Top-1/Top-2 RSSI calculation can therefore claim “roaming overlap” when both candidates are merely two radios from the **same device**.

This refactor fixes that issue by collapsing radios by physical AP before evaluating cross-AP roaming potential.

## What it analyses

- sanitised RSSI measurements across nine abstract indoor points;
- 2.4 GHz / 5 GHz observations and channel usage;
- strongest AP at each point;
- Top-1 / Top-2 **physical AP** RSSI delta;
- a simple roaming-overlap heuristic;
- repeatable charts and CSV outputs.

The reference heuristic marks a point as a roaming-overlap candidate when the second-best **distinct physical AP** is at least `-75 dBm` and the Top-1/Top-2 difference is no more than `15 dB`. These are analysis thresholds, not universal roaming guarantees: real client roaming also depends on driver logic, SNR, retry rate, channel utilisation, 802.11k/v/r support, and policy.

## Repository structure

```text
wifi-site-survey-analysis/
├── data/
│   ├── survey_measurements.csv
│   └── README.md
├── src/
│   └── wifi_survey.py
├── scripts/
│   ├── analyse.py
│   └── plot_results.py
├── tests/
│   └── test_wifi_survey.py
├── results/
│   ├── roaming_summary.csv
│   ├── strongest_rssi_by_point.png
│   ├── roaming_delta_by_point.png
│   └── channel_observations.png
└── .github/workflows/tests.yml
```

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/analyse.py
python scripts/plot_results.py
python -m unittest discover -s tests -v
```

## Reference findings

After physical-radio de-duplication, the strongest 5 GHz signal varies substantially across the nine abstract points. Points **D, E and I** satisfy the repository's cross-AP overlap heuristic; other points either have a weak second AP, a larger RSSI gap, or only one distinct physical AP visible strongly enough.

This is deliberately more conservative than treating two BSSIDs from the same AP chassis as two independent roaming candidates.

## Engineering improvements over the coursework version

- removed all real infrastructure identifiers and campus topology;
- converted spreadsheet-only analysis into reusable Python functions;
- separated `radio_id` from `physical_ap`;
- corrected roaming logic to de-duplicate radios from the same AP;
- added automated tests and CI;
- made result generation reproducible from a small sanitised CSV.

## Skills demonstrated

`Python` · `Wi-Fi` · `802.11` · `RSSI` · `wireless networking` · `roaming analysis` · `channel planning` · `data analysis` · `matplotlib` · `testing`

## Origin

The underlying measurements originated from a wireless networking exercise completed while studying **FIT1047 Introduction to Computer Systems, Networks and Security** at Monash University. This repository contains only a post-course reimplementation and sanitised derivative data.
