# Wi-Fi 现场勘测与漫游分析

[![类型](https://img.shields.io/badge/%E7%B1%BB%E5%9E%8B-%E8%AF%BE%E7%A8%8B%E4%BD%9C%E4%B8%9A-2563eb?style=for-the-badge)](#)
[![技术](https://img.shields.io/badge/%E6%8A%80%E6%9C%AF-Python-7c3aed?style=for-the-badge)](#)
[![许可证](https://img.shields.io/badge/%E8%AE%B8%E5%8F%AF%E8%AF%81-MIT-16a34a?style=for-the-badge)](LICENSE)


[English](README.md)

这是一个在课程结束后重新整理的、适合公开展示的 WLAN 分析项目，涵盖 **RSSI、信道观察、按物理 AP 去重的漫游重叠分析，以及可复现的 Python 可视化**。

> 本仓库**不是原始课程作业提交**。为了公开展示，真实校区位置、楼层平面图、BSSID/MAC、网关地址、抓包文件、学生信息和其他基础设施细节均已删除。

## 为什么要重构

无线勘测经常会看到同一个物理 AP 广播多个 BSSID。如果直接用信号最强的 Top-1 / Top-2 BSSID 判断漫游，就可能把**同一台 AP 的两个 radio**误当成两个可漫游 AP。

这个版本会先按 `physical_ap` 合并同一设备的 radio，再计算真正的跨 AP 漫游重叠。

## 分析内容

- 9 个匿名室内测量点的 RSSI；
- 2.4 GHz / 5 GHz 与信道观察；
- 每个位置最强的物理 AP；
- Top-1 / Top-2 **不同物理 AP** 的 RSSI 差值；
- 简单的漫游重叠判定；
- 自动生成 CSV 和图表。

参考规则为：第二强的不同物理 AP 至少达到 `-75 dBm`，且与最强 AP 的差值不超过 `15 dB`。这只是分析阈值，并不代表真实客户端一定无缝漫游；实际还会受到 SNR、重传率、信道利用率、驱动策略以及 802.11k/v/r 等因素影响。

## 运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/analyse.py
python scripts/plot_results.py
python -m unittest discover -s tests -v
```

## 参考结论

在把同一物理 AP 的多个 radio 去重后，匿名测量点 **D、E、I** 符合本项目设定的跨 AP 漫游重叠条件；其他位置则因为第二 AP 较弱、RSSI 差距较大，或可见的独立物理 AP 不足而不满足条件。

## 相比原课程工作的改进

- 删除真实网络和校区基础设施信息；
- 把 Excel 手工分析重构为 Python 模块；
- 明确区分 `radio_id` 与 `physical_ap`；
- 修正同一 AP 多 BSSID 导致的漫游误判；
- 增加自动测试和 GitHub Actions CI；
- 使用小型匿名 CSV 实现可复现分析。

## 技术点

`Python` · `Wi-Fi` · `802.11` · `RSSI` · `无线网络` · `漫游分析` · `信道规划` · `数据分析` · `matplotlib` · `自动测试`

## 来源说明

底层测量数据最初来自 Monash University 的 **FIT1047 Introduction to Computer Systems, Networks and Security** 无线网络练习。本仓库仅保留课程结束后的重新实现和匿名化衍生数据。
