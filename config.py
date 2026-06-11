"""
tw_cake_monitor/config.py – 台股 AI + 機器人輪動監控設定（11 層）
"""
from __future__ import annotations
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

LAYERS: dict[str, dict] = {
    "chip_foundry": {
        "label": "🏭 晶片/代工",
        "cake_layer": 1,
        "tickers": ["2330.TW", "2454.TW", "2303.TW", "3661.TW", "3443.TW"],
        "ticker_labels": {
            "2330.TW": "台積電",
            "2454.TW": "聯發科",
            "2303.TW": "聯電",
            "3661.TW": "世芯",
            "3443.TW": "創意",
        },
    },
    "ai_server": {
        "label": "🖥️ AI伺服器/ODM",
        "cake_layer": 2,
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
        "label": "💾 記憶體",
        "cake_layer": 2,
        "tickers": ["2408.TW", "2344.TW", "2337.TW", "8046.TW"],
        "ticker_labels": {
            "2408.TW": "南亞科",
            "2344.TW": "華邦電",
            "2337.TW": "旺宏",
            "8046.TW": "南電",
        },
    },
    "facility": {
        "label": "🏗️ 廠務工程",
        "cake_layer": 2,
        "tickers": ["2404.TW", "6139.TW", "6196.TW", "5434.TW", "6271.TW"],
        "ticker_labels": {
            "2404.TW": "漢唐",
            "6139.TW": "亞翔",
            "6196.TW": "帆宣",
            "5434.TW": "崇越科",
            "6271.TW": "同欣電",
        },
    },
    "power_thermal": {
        "label": "⚡ 電源/散熱",
        "cake_layer": 3,
        "tickers": ["2308.TW", "2301.TW", "3044.TW", "3017.TW", "2421.TW"],
        "ticker_labels": {
            "2308.TW": "台達電",
            "2301.TW": "光寶科",
            "3044.TW": "健策",
            "3017.TW": "奇鋐",
            "2421.TW": "建準",
        },
    },
    "networking": {
        "label": "🔌 網路/交換機",
        "cake_layer": 3,
        "tickers": ["2345.TW", "6285.TW", "4977.TW", "5388.TW", "3706.TW"],
        "ticker_labels": {
            "2345.TW": "智邦",
            "6285.TW": "啟碁",
            "4977.TW": "眾達-KY",
            "5388.TW": "中磊",
            "3706.TW": "神達",
        },
    },
    "optical": {
        "label": "💡 光通訊",
        "cake_layer": 3,
        "tickers": ["2393.TW", "3030.TW", "6176.TW", "4952.TW", "3665.TW"],
        "ticker_labels": {
            "2393.TW": "億光",
            "3030.TW": "科佳",
            "6176.TW": "瑞儀",
            "4952.TW": "越峰",
            "3665.TW": "貿聯-KY",
        },
    },
    "passive_components": {
        "label": "🔩 被動元件",
        "cake_layer": 3,
        "tickers": ["2327.TW", "3026.TW", "2492.TW", "3006.TW", "2478.TW"],
        "ticker_labels": {
            "2327.TW": "國巨",
            "3026.TW": "禾伸堂",
            "2492.TW": "華新科",
            "3006.TW": "晶豪科",
            "2478.TW": "大毅",
        },
    },
    "power_devices": {
        "label": "🔋 功率元件",
        "cake_layer": 3,
        "tickers": ["8261.TW", "2481.TW", "3046.TW", "2457.TW", "6443.TW"],
        "ticker_labels": {
            "8261.TW": "富鼎",
            "2481.TW": "強茂",
            "3046.TW": "尼克森",
            "2457.TW": "飛宏",
            "6443.TW": "元晶",
        },
    },
    "robotics": {
        "label": "🦾 機器人/自動化",
        "cake_layer": 4,
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
