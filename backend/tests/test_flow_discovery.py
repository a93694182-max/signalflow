from app.core.flow_discovery import discover_flows
from app.services.collector_service import collect_all_signals
from app.services.signal_filter_service import filter_signals

signals = collect_all_signals()
signals = filter_signals(signals)

flows = discover_flows(signals)

print(f"Flow 개수: {len(flows)}")

for flow in flows:
    print("=" * 60)
    print(flow.title)
    print(flow.target_asset)
    print(len(flow.nodes))