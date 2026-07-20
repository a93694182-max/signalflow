from app.services.news_service import generate_news_signals


signals = generate_news_signals(limit=3)

print(f"뉴스 Signal 개수: {len(signals)}")

for signal in signals:
    print("=" * 60)
    print(f"type: {signal.signal_type}")
    print(f"category: {signal.category}")
    print(f"title: {signal.title}")
    print(f"source: {signal.source}")
    print(f"occurred_at: {signal.occurred_at}")
    print(f"url: {signal.url}")
    