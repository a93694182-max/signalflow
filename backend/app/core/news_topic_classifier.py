from __future__ import annotations

import re


TOPIC_KEYWORDS = {
    "monetary_policy": {
        "fed",
        "federal reserve",
        "interest rate",
        "rate cut",
        "rate hike",
        "central bank",
        "monetary policy",
        "inflation",
    },
    "geopolitics": {
        "war",
        "missile",
        "military",
        "conflict",
        "sanction",
        "iran",
        "israel",
        "russia",
        "ukraine",
        "china",
        "tariff",
    },
    "commodity": {
        "oil",
        "crude",
        "gold",
        "gas",
        "opec",
        "commodity",
        "supply",
    },
    "crypto": {
        "bitcoin",
        "crypto",
        "ethereum",
        "blockchain",
        "digital asset",
    },
    "technology": {
        "ai",
        "artificial intelligence",
        "semiconductor",
        "chip",
        "nvidia",
        "microsoft",
        "apple",
        "google",
        "meta",
    },
    "corporate": {
        "earnings",
        "revenue",
        "profit",
        "company",
        "acquisition",
        "merger",
        "shares",
        "stock",
    },
    "economic": {
        "gdp",
        "employment",
        "unemployment",
        "consumer price",
        "cpi",
        "economy",
        "economic growth",
        "recession",
    },
    
}

IRRELEVANT_NEWS_KEYWORDS = {
    "world cup",
    "football",
    "soccer",
    "basketball",
    "baseball",
    "tennis",
    "formula 1",
    "nba",
    "nfl",
    "olympics",
}




def contains_keyword(
    text: str,
    keyword: str,
) -> bool:
    pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"

    return re.search(
        pattern,
        text,
        flags=re.IGNORECASE,
    ) is not None


def classify_news_topic(
    title: str,
    summary: str | None = None,
) -> str:
    text = f"{title} {summary or ''}"

    topic_scores = {
        topic: sum(
            1
            for keyword in keywords
            if contains_keyword(text, keyword)
        )
        for topic, keywords in TOPIC_KEYWORDS.items()
    }

    best_topic = max(
        topic_scores,
        key=topic_scores.get,
    )

    if topic_scores[best_topic] == 0:
        return "general"

    return best_topic


def is_relevant_news(
    title: str,
    summary: str | None = None,
) -> bool:
    text = f"{title} {summary or ''}"

    return not any(
        contains_keyword(text, keyword)
        for keyword in IRRELEVANT_NEWS_KEYWORDS
    )