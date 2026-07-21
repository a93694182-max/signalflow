from sqlalchemy.orm import Session

from app.services.collector_service import collect_all_signals
from app.services.flow_service import create_flows_from_signals
from app.services.signal_filter_service import filter_signals
from app.services.flow_link_service import create_flow_links

def run_signal_engine(db: Session) -> dict:
    collected_signals = collect_all_signals()
    filtered_signals = filter_signals(collected_signals)

    if not filtered_signals:
        return {
            "collected_count": len(collected_signals),
            "filtered_count": 0,
            "flow_count": 0,
            "link_count": 0,
            "flows": [],
        }

    flows = create_flows_from_signals(
        db=db,
        signals=filtered_signals,
    )

    flow_links = create_flow_links(
        db=db,
        flows=flows,
    )

    return {
        "collected_count": len(collected_signals),
        "filtered_count": len(filtered_signals),
        "flow_count": len(flows),
        "link_count": len(flow_links),
        "flows": flows,
    }