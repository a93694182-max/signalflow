from app.core.news_topic_classifier import (
    classify_news_topic,
    is_relevant_news,
)


test_cases = [
    (
        "Fed signals another interest rate cut",
        "monetary_policy",
    ),
    (
        "Oil prices rise after supply concerns",
        "commodity",
    ),
    (
        "Bitcoin climbs to a new record",
        "crypto",
    ),
    (
        "Nvidia unveils new AI semiconductor",
        "technology",
    ),
    (
        "Military conflict increases market uncertainty",
        "geopolitics",
    ),
    (
        "Company reports strong quarterly earnings",
        "corporate",
    ),
    (
        "Spain beat Argentina to win World Cup",
        "general",
    ),
    (
        "A completely unrelated headline",
        "general",
    ),
]


for title, expected_topic in test_cases:
    result = classify_news_topic(title)

    print("=" * 60)
    print(f"title: {title}")
    print(f"expected: {expected_topic}")
    print(f"result: {result}")

    assert result == expected_topic

assert not is_relevant_news(
    "Spain beat Argentina to win World Cup",
)

assert is_relevant_news(
    "Oil prices rise after supply concerns",
)


print("News Topic Classifier 테스트 통과")