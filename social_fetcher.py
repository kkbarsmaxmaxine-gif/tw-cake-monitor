"""
social_fetcher.py – social media buzz tracker for tw_cake_monitor (TW stocks).

Platforms:
  PTT     — scraping (no auth, free)
  YouTube — set YOUTUBE_API_KEY env var (free Google Cloud key)
  News    — TrendForce TW + DigiTimes + MoneyDJ (scraping, no auth)

All platforms degrade gracefully if credentials are absent.
Search terms use Chinese display names (e.g., "台積電") from ticker_labels.
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

_PTT_BOARDS = ["Stock", "Tech_Job"]

_NEWS_URLS = [
    ("trendforce_tw", "https://www.trendforce.com.tw/"),
    ("trendforce_en", "https://www.trendforce.com/news/"),
    ("digitimes",     "https://www.digitimes.com/news/"),
]

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _search_terms(ticker: str, ticker_labels: dict[str, str]) -> list[str]:
    """Return [numeric_code, chinese_name] for PTT/news search."""
    base  = ticker.split(".")[0]   # "2330.TW" → "2330"
    label = ticker_labels.get(ticker, "")
    terms = [base]
    if label and label != base:
        terms.append(label)
    return terms


def _get(url: str, *, timeout: int = 15, extra_headers: dict | None = None) -> str:
    headers = {"User-Agent": _UA}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


# ── PTT ───────────────────────────────────────────────────────────────────────

def _fetch_ptt(tickers: list[str], ticker_labels: dict[str, str]) -> dict[str, int]:
    """Scrape PTT Stock board for today's posts and count ticker/name mentions."""
    today_str = datetime.now().strftime("%-m/%-d")   # e.g., "6/11"
    term_map  = {t: _search_terms(t, ticker_labels) for t in tickers}
    counts: dict[str, int] = {t: 0 for t in tickers}

    for board in _PTT_BOARDS:
        # Fetch index and gather article links for today
        try:
            html  = _get(
                f"https://www.ptt.cc/bbs/{board}/index.html",
                extra_headers={"Cookie": "over18=1"},
            )
            # Find articles with today's date
            # PTT date format in HTML: <div class="date"> 6/11</div>
            entries = re.findall(
                r'<div class="r-ent">(.*?)</div>\s*</div>',
                html, re.DOTALL,
            )
            for entry in entries:
                date_match = re.search(r'<div class="date">\s*(\S+)\s*</div>', entry)
                if not date_match:
                    continue
                if date_match.group(1) != today_str:
                    continue
                title_match = re.search(r'<div class="title"[^>]*>.*?<a[^>]*>([^<]+)</a>', entry, re.DOTALL)
                title = title_match.group(1).strip() if title_match else ""
                for ticker, terms in term_map.items():
                    if any(t in title for t in terms):
                        counts[ticker] += 1
            time.sleep(0.3)
        except Exception as exc:
            # PTT often blocks non-Taiwan IPs; expected when running from GitHub Actions
            logger.info("PTT %s: %s (blocked outside TW?)", board, type(exc).__name__)

    logger.info("PTT: %d tickers with mentions", sum(1 for v in counts.values() if v))
    return {t: v for t, v in counts.items() if v > 0}


# ── YouTube ───────────────────────────────────────────────────────────────────

def _fetch_youtube(tickers: list[str], ticker_labels: dict[str, str]) -> dict[str, int]:
    api_key = os.environ.get("YOUTUBE_API_KEY", "")
    if not api_key:
        logger.info("YouTube: no API key — skipping")
        return {}

    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    counts: dict[str, int] = {}

    for ticker in tickers:
        terms = _search_terms(ticker, ticker_labels)
        # Use Chinese name if available for TW stock search
        primary = terms[-1] if len(terms) > 1 else terms[0]
        q = f"{primary} 股票 分析"
        params = urllib.parse.urlencode({
            "key":            api_key,
            "q":              q,
            "type":           "video",
            "publishedAfter": yesterday,
            "part":           "snippet",
            "maxResults":     50,
            "relevanceLanguage": "zh-TW",
        })
        try:
            data   = json.loads(_get(f"https://www.googleapis.com/youtube/v3/search?{params}"))
            counts[ticker] = len(data.get("items", []))
            time.sleep(0.2)
        except Exception as exc:
            logger.warning("YouTube %s: %s", ticker, exc)

    logger.info("YouTube: %d tickers with results", sum(1 for v in counts.values() if v))
    return {t: v for t, v in counts.items() if v > 0}


# ── News scraping ─────────────────────────────────────────────────────────────

def _fetch_news(tickers: list[str], ticker_labels: dict[str, str]) -> dict[str, int]:
    term_map = {t: _search_terms(t, ticker_labels) for t in tickers}
    counts: dict[str, int] = {t: 0 for t in tickers}

    for source, url in _NEWS_URLS:
        try:
            html = _get(url).lower()
            for ticker, terms in term_map.items():
                for term in terms:
                    counts[ticker] += html.count(term.lower())
        except Exception as exc:
            logger.warning("News %s: %s", source, exc)

    logger.info("News: %d tickers with mentions", sum(1 for v in counts.values() if v))
    return {t: v for t, v in counts.items() if v > 0}


# ── Public API ────────────────────────────────────────────────────────────────

def build_buzz(
    tickers:         list[str],
    ticker_labels:   dict[str, str],
    ticker_to_layer: dict[str, str],
) -> dict:
    """
    Fetch social buzz from all configured platforms and return aggregated results.

    Return schema:
      updated_at  : ISO timestamp
      sources     : list of platforms that returned data
      by_ticker   : ticker → {display_name, ptt, youtube, news, total, score}
      by_layer    : layer_id → {total, score, top_ticker}
      top5        : list of top-5 tickers by weighted score
    """
    logger.info("Social buzz: starting fetch (TW mode)")

    ptt_counts     = _fetch_ptt(tickers, ticker_labels)
    youtube_counts = _fetch_youtube(tickers, ticker_labels)
    news_counts    = _fetch_news(tickers, ticker_labels)

    sources = (
        (["ptt"]     if ptt_counts     else []) +
        (["youtube"] if youtube_counts else []) +
        (["news"]    if news_counts    else [])
    )

    by_ticker: dict[str, dict] = {}
    for t in tickers:
        p = ptt_counts.get(t, 0)
        y = youtube_counts.get(t, 0)
        n = news_counts.get(t, 0)
        total = p + y + n
        score = p * 1.5 + y * 3 + n * 2   # weights for TW context
        by_ticker[t] = {
            "display_name": ticker_labels.get(t, t.split(".")[0]),
            "ptt":     p,
            "youtube": y,
            "news":    n,
            "total":   total,
            "score":   round(score, 1),
        }

    top5 = sorted(by_ticker.items(), key=lambda x: x[1]["score"], reverse=True)[:5]
    top5_out = [{"ticker": k, **v} for k, v in top5 if v["total"] > 0]

    by_layer: dict[str, dict] = {}
    for t, buzz in by_ticker.items():
        lid = ticker_to_layer.get(t, "unknown")
        if lid not in by_layer:
            by_layer[lid] = {"total": 0, "score": 0.0, "top_ticker": "", "top_score": -1.0}
        by_layer[lid]["total"] += buzz["total"]
        by_layer[lid]["score"] += buzz["score"]
        if buzz["score"] > by_layer[lid]["top_score"]:
            by_layer[lid]["top_score"] = buzz["score"]
            by_layer[lid]["top_ticker"] = buzz["display_name"]

    logger.info("Social buzz done — sources: %s | top: %s",
                sources, top5_out[0]["display_name"] if top5_out else "—")
    return {
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "sources":    sources,
        "by_ticker":  by_ticker,
        "by_layer":   by_layer,
        "top5":       top5_out,
    }
