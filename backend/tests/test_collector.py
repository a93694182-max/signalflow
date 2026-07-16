from collections import Counter

from app.services.collector_service import collect_all_signals
from app.services.signal_filter_service import filter_signals


collected_signals = collect_all_signals()
filtered_signals = filter_signals(collected_signals)

print(f"전체 수집: {len(collected_signals)}")
print(f"필터 통과: {len(filtered_signals)}")

print("\n수집 타입:")
print(Counter(signal.signal_type for signal in collected_signals))

print("\n필터 통과 타입:")
print(Counter(signal.signal_type for signal in filtered_signals))

print("\n필터 통과 카테고리:")
print(Counter(signal.category for signal in filtered_signals))