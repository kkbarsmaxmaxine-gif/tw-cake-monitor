"""
tw_cake_monitor/config.py – 台股 AI + 機器人輪動監控設定（14 層）
整合 Tide (tide-tw.app) 族群架構與標的
"""
from __future__ import annotations
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

LAYERS: dict[str, dict] = {
    # ── Cake Layer 1: 最核心基礎 ──────────────────────────────────────────────
    "chip_foundry": {
        "label": "🏭 晶片/代工",
        "cake_layer": 1,
        # Tide: 晶圓代工 + CPU與Agentic AI + 客製ASIC
        "tickers": ["2330.TW", "2454.TW", "2303.TW", "3661.TW", "3443.TW"],
        "ticker_labels": {
            "2330.TW": "台積電",
            "2454.TW": "聯發科",
            "2303.TW": "聯電",
            "3661.TW": "世芯",
            "3443.TW": "創意",
        },
    },

    # ── Cake Layer 2: AI 直接供應鏈 ──────────────────────────────────────────
    "ai_server": {
        "label": "🖥️ AI伺服器/ODM",
        "cake_layer": 2,
        # Tide: AI伺服器組裝
        "tickers": ["2317.TW", "2382.TW", "6669.TW", "2356.TW", "3231.TW"],
        "ticker_labels": {
            "2317.TW": "鴻海",
            "2382.TW": "廣達",
            "6669.TW": "緯穎",
            "2356.TW": "英業達",
            "3231.TW": "緯創",
        },
    },
    "memory": {
        "label": "💾 記憶體/HBM",
        "cake_layer": 2,
        # Tide: NOR Flash利基記憶體 + HBM高頻寬記憶體 + 記憶體模組
        "tickers": ["2408.TW", "2344.TW", "2337.TW", "8046.TW", "5269.TW"],
        "ticker_labels": {
            "2408.TW": "南亞科",
            "2344.TW": "華邦電",
            "2337.TW": "旺宏",
            "8046.TW": "南電",
            "5269.TW": "祥碩",
        },
    },
    "adv_packaging": {
        "label": "📦 先進封裝",
        "cake_layer": 2,
        # Tide: AI先進封裝 + 封測代工
        "tickers": ["3711.TW", "8150.TW", "2449.TW", "2329.TW", "2369.TW"],
        "ticker_labels": {
            "3711.TW": "日月光投控",
            "8150.TW": "南茂",
            "2449.TW": "京元電子",
            "2329.TW": "華泰",
            "2369.TW": "菱生精密",
        },
    },
    "facility": {
        "label": "🏗️ 廠務工程",
        "cake_layer": 2,
        # Tide: 晶圓廠設備 + 前段製程材料
        "tickers": ["2404.TW", "6139.TW", "6196.TW", "5434.TW", "6271.TW"],
        "ticker_labels": {
            "2404.TW": "漢唐",
            "6139.TW": "亞翔",
            "6196.TW": "帆宣",
            "5434.TW": "崇越科",
            "6271.TW": "同欣電",
        },
    },

    # ── Cake Layer 3: 關鍵零組件 ──────────────────────────────────────────────
    "power_thermal": {
        "label": "⚡ 電源/氣冷",
        "cake_layer": 3,
        # Tide: 電源供應器 + 氣冷與核心組件
        "tickers": ["2308.TW", "2301.TW", "3044.TW", "3017.TW", "2421.TW"],
        "ticker_labels": {
            "2308.TW": "台達電",
            "2301.TW": "光寶科",
            "3044.TW": "健策",
            "3017.TW": "奇鋐",
            "2421.TW": "建準",
        },
    },
    "liquid_cooling": {
        "label": "💧 液冷散熱",
        "cake_layer": 3,
        # Tide: 液冷散熱 — AI伺服器液冷趨勢
        "tickers": ["6230.TW", "3338.TW", "3653.TW", "3043.TW", "2059.TW"],
        "ticker_labels": {
            "6230.TW": "超眾",
            "3338.TW": "泰碩",
            "3653.TW": "健策精",
            "3043.TW": "健鼎",
            "2059.TW": "川湖",
        },
    },
    "networking": {
        "label": "🔌 網路/交換機",
        "cake_layer": 3,
        # Tide: 高速交換器與無線網路
        "tickers": ["2345.TW", "6285.TW", "4977.TW", "3380.TW", "2332.TW"],
        "ticker_labels": {
            "2345.TW": "智邦",
            "6285.TW": "啟碁",
            "4977.TW": "眾達-KY",
            "3380.TW": "明泰",
            "2332.TW": "友訊",
        },
    },
    "optical": {
        "label": "💡 高速光模組",
        "cake_layer": 3,
        # Tide: 高速光模組 + 矽光子與CPO
        "tickers": ["2393.TW", "3450.TW", "6177.TW", "6243.TW", "3030.TW"],
        "ticker_labels": {
            "2393.TW": "億光",
            "3450.TW": "聯鈞",
            "6177.TW": "台灣精銳",
            "6243.TW": "精材",
            "3030.TW": "科佳",
        },
    },
    "passive_components": {
        "label": "🔩 被動元件",
        "cake_layer": 3,
        # Tide: 被動元件MLCC + 電容器 + 功率電感
        "tickers": ["2327.TW", "2492.TW", "2375.TW", "6112.TW", "2478.TW"],
        "ticker_labels": {
            "2327.TW": "國巨",
            "2492.TW": "華新科",
            "2375.TW": "智寶",
            "6112.TW": "聚鼎",
            "2478.TW": "大毅",
        },
    },
    "power_devices": {
        "label": "🔋 功率/類比IC",
        "cake_layer": 3,
        # Tide: 類比與功率IC + 第三代半導體
        "tickers": ["8261.TW", "2481.TW", "3046.TW", "3014.TW", "6443.TW"],
        "ticker_labels": {
            "8261.TW": "富鼎",
            "2481.TW": "強茂",
            "3046.TW": "尼克森",
            "3014.TW": "聯陽",
            "6443.TW": "元晶",
        },
    },

    # ── Cake Layer 4: 終端應用 ────────────────────────────────────────────────
    "robotics": {
        "label": "🦾 機器人/自動化",
        "cake_layer": 4,
        # Tide: 工業自動化 + CNC工具機
        "tickers": ["2049.TW", "2395.TW", "1504.TW", "2453.TW", "1597.TW"],
        "ticker_labels": {
            "2049.TW": "上銀",
            "2395.TW": "研華",
            "1504.TW": "東元",
            "2453.TW": "盟立",
            "1597.TW": "直得",
        },
    },
    "aipc": {
        "label": "💻 AIPC/消費電子",
        "cake_layer": 4,
        # Tide: AI PC筆電與平板
        "tickers": ["2357.TW", "2353.TW", "2376.TW", "2377.TW", "4938.TW"],
        "ticker_labels": {
            "2357.TW": "華碩",
            "2353.TW": "宏碁",
            "2376.TW": "技嘉",
            "2377.TW": "微星",
            "4938.TW": "和碩",
        },
    },
    "satellite": {
        "label": "🛰️ 衛星通訊",
        "cake_layer": 4,
        # Tide: 低軌衛星 + 高速交換器部分
        "tickers": ["2314.TW", "3596.TW", "3062.TW", "3045.TW", "2412.TW"],
        "ticker_labels": {
            "2314.TW": "台揚",
            "3596.TW": "智易",
            "3062.TW": "建漢",
            "3045.TW": "台灣大",
            "2412.TW": "中華電",
        },
    },
}

BENCHMARK = "^TWII"
LOG_LEVEL  = "INFO"
