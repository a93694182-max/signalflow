from app.core.flow_discovery import discover_flows
from app.services.news_service import generate_news_signals


signals = generate_news_signals(limit=3)
flows = discover_flows(signals)

print(f"Flow 개수: {len(flows)}")

for flow in flows:
    print("=" * 60)
    print(f"Flow 제목: {flow.title}")
    print(f"대상: {flow.target_asset}")
    print(f"노드 개수: {len(flow.nodes)}")

    for node in flow.nodes:
        print("-" * 40)
        print(f"Node: {node.title}")
        print(f"설명: {node.description}")
        print(f"Evidence URL: {node.evidences[0].url}")