"""
tw_cake_monitor/reporter.py – Markdown report + terminal summary (台股版)
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from config import LAYERS, OUTPUT_DIR

logger = logging.getLogger(__name__)


def _pct(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    sign = "+" if float(v) > 0 else ""
    return f"{sign}{float(v):.2f}%"


def _f(v, d: int = 2) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    return f"{float(v):.{d}f}"


def _bar(v, width: int = 10) -> str:
    if v is None or np.isnan(v):
        return "─" * width
    norm   = min(max((float(v) + 5.0) / 10.0, 0.0), 1.0)
    filled = round(norm * width)
    return "█" * filled + "░" * (width - filled)


def generate_report(
    analysis:      dict,
    benchmark_chg: float | None,
    date_str:      str,
) -> str:
    layer_perf = analysis["layer_perf"]
    resilience = analysis["resilience"]
    rebound    = analysis["rebound"]
    narrative  = analysis["narrative"]
    snapshot   = analysis["snapshot"]

    now    = datetime.now().strftime("%Y-%m-%d %H:%M")
    bm_str = f"加權指數 {_pct(benchmark_chg)}" if benchmark_chg is not None else "加權指數 N/A"
    lines: list[str] = []

    lines += [
        f"# 台股 AI 輪動監控日報 — {date_str}",
        f"> 產生時間: {now} | 基準: {bm_str}",
        "",
        "---",
        "",
    ]

    # Q1+Q2
    lines.append("## Q1 + Q2 各族群漲跌排行\n")
    if not layer_perf.empty:
        lines.append("| # | 族群 | 均漲跌 | 趨勢 | 最強 | 最弱 | Vol倍率 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for rank, row in layer_perf.iterrows():
            bar = _bar(row["avg_change"])
            lines.append(
                f"| {rank+1} | {row['layer_label']} "
                f"| **{_pct(row['avg_change'])}** | `{bar}` "
                f"| {row['best_ticker']} ({_pct(row['best_pct'])}) "
                f"| {row['worst_ticker']} ({_pct(row['worst_pct'])}) "
                f"| {_f(row['avg_vol_ratio'])}x |"
            )
        top = layer_perf.iloc[0]
        bot = layer_perf.iloc[-1]
        lines += [
            "",
            f"> 🏆 **最強族群**: {top['layer_label']} — 均漲 **{_pct(top['avg_change'])}**",
            f"> 💀 **最弱族群**: {bot['layer_label']} — 均跌 **{_pct(bot['avg_change'])}**",
            "",
        ]

    # Q3
    lines.append("## Q3 各族群抗跌冠軍\n")
    if not resilience.empty and "relative_strength" in resilience.columns:
        lines.append("| 族群 | 排名 | 個股 | 漲跌 | 相對強弱 | Vol倍率 |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for layer_id, cfg in LAYERS.items():
            sub = resilience[resilience["layer"] == layer_id]
            if sub.empty:
                continue
            for rank, (_, row) in enumerate(sub.iterrows(), 1):
                rs     = row["relative_strength"]
                rs_str = f"+{rs:.2f}%" if (not np.isnan(rs) and rs > 0) else f"{rs:.2f}%"
                medal  = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"  {rank}")
                lines.append(
                    f"| {cfg['label']} | {medal} | **{row['display_name']}** "
                    f"| {_pct(row['change_pct'])} | {rs_str} | {_f(row['vol_ratio'])}x |"
                )

    # Q4
    lines += ["", "## Q4 從日內低點反彈最快\n"]
    if not rebound.empty and "rebound_ratio" in rebound.columns:
        top_reb = rebound[rebound["rebound_ratio"].notna()].head(10)
        if not top_reb.empty:
            lines.append("| # | 個股 | 族群 | rebound_ratio | 漲跌 |")
            lines.append("| --- | --- | --- | --- | --- |")
            for rank, (_, row) in enumerate(top_reb.iterrows(), 1):
                lbl = LAYERS.get(row["layer"], {}).get("label", row["layer"])
                lines.append(
                    f"| {rank} | **{row['display_name']}** | {lbl} "
                    f"| {_f(row['rebound_ratio'], 3)} | {_pct(row['change_pct'])} |"
                )

    # Q5
    lines += ["", "## Q5 市場現在交易哪個敘事？\n"]
    if narrative:
        verdict = narrative.get("verdict", "未知")
        leading = narrative.get("leading", {})
        weakest = narrative.get("weakest", {})
        mflow   = narrative.get("money_flow", {})
        signal  = narrative.get("signal", "")
        signal_map = {
            "strong":    "✅ **強訊號** — 主流族群明顯跑贏",
            "weak":      "⚠️ **弱訊號** — 各族群表現分散",
            "defensive": "🚨 **防禦模式** — 全面回跌",
        }
        lines += [
            f"### 🎯 當前主線: **{verdict}**",
            "",
            f"- 🔥 **最強**: {leading.get('label', '')} ({_pct(leading.get('avg_pct'))})",
            f"- 🥶 **最弱**: {weakest.get('label', '')} ({_pct(weakest.get('avg_pct'))})",
            f"- 💰 **資金流入**: {mflow.get('label', '')} (Vol倍率 {_f(mflow.get('avg_vol_ratio'))}x)",
            "",
            f"> {signal_map.get(signal, '')}",
        ]
        if not layer_perf.empty and benchmark_chg is not None:
            lines += ["", "### 各族群 vs 加權指數", ""]
            lines.append("| 族群 | 均漲跌 | vs 大盤 | 方向 |")
            lines.append("| --- | --- | --- | --- |")
            for _, row in layer_perf.iterrows():
                vs = row["avg_change"] - benchmark_chg
                direction = "↑ 跑贏" if vs > 0.3 else ("↓ 跑輸" if vs < -0.3 else "→ 持平")
                lines.append(
                    f"| {row['layer_label']} | {_pct(row['avg_change'])} "
                    f"| {'+' if vs>0 else ''}{vs:.2f}% | {direction} |"
                )

    # Snapshot
    lines += ["", "---", "## 全股票快照\n"]
    if not snapshot.empty:
        rs_map = (
            resilience[["ticker", "relative_strength"]]
            .drop_duplicates("ticker").set_index("ticker")["relative_strength"]
            if not resilience.empty and "relative_strength" in resilience.columns
            else pd.Series(dtype=float)
        )
        lines.append("| 個股 | 族群 | 今日% | 相對強弱 | Rebound | Vol倍率 |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for _, row in snapshot.sort_values("change_pct", ascending=False).iterrows():
            lbl = LAYERS.get(row["layer"], {}).get("label", row["layer"])
            rs  = rs_map.get(row["ticker"], float("nan"))
            rs_str = f"+{rs:.2f}%" if (not np.isnan(rs) and rs > 0) else (f"{rs:.2f}%" if not np.isnan(rs) else "N/A")
            icon = "🟢" if row["change_pct"] > 0 else "🔴"
            lines.append(
                f"| {icon} {row['display_name']} | {lbl} "
                f"| {_pct(row['change_pct'])} | {rs_str} "
                f"| {_f(row.get('rebound_ratio', float('nan')), 3)} "
                f"| {_f(row.get('vol_ratio', float('nan')), 2)}x |"
            )

    n = len(snapshot) if not snapshot.empty else 0
    lines += ["", "---", f"_監控個股數: **{n}** | 不構成投資建議_"]
    return "\n".join(lines)


def print_terminal_summary(analysis: dict, benchmark_chg: float | None) -> None:
    layer_perf = analysis["layer_perf"]
    narrative  = analysis["narrative"]

    print("\n" + "=" * 60)
    print("  台股 AI 輪動監控")
    if benchmark_chg is not None:
        print(f"  加權指數: {'+' if benchmark_chg > 0 else ''}{benchmark_chg:.2f}%")
    print("=" * 60)
    if not layer_perf.empty:
        print("\n  族群表現:")
        for _, row in layer_perf.iterrows():
            bar  = _bar(row["avg_change"], 8)
            sign = "+" if row["avg_change"] > 0 else ""
            print(f"  {row['layer_label']:<36} {sign}{row['avg_change']:.2f}%  [{bar}]")
    if narrative:
        print(f"\n  🎯 主線: {narrative.get('verdict', '')}")
    print("=" * 60 + "\n")


def save_report(content: str, date_str: str) -> Path:
    path = OUTPUT_DIR / f"tw_cake_monitor_{date_str}.md"
    path.write_text(content, encoding="utf-8")
    logger.info("Report saved: %s", path)
    return path
