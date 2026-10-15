
import argparse
import json

from graph_store import connect_graph
from investigator import investigate_hotspot
from decision_engine import compare_hotspots
from memory_store import (
    get_investigation_history,
    save_investigation_history,
)


def run_heatpath(hotspot_a_id, hotspot_b_id):
    client, graph = connect_graph()

    try:
        # Retrieve previous investigations for context.
        history = get_investigation_history(
            graph, hotspot_a_id, hotspot_b_id
        )

        # Investigate current graph records.
        report_a = investigate_hotspot(
            graph, hotspot_a_id
        )
        report_b = investigate_hotspot(
            graph, hotspot_b_id
        )

        # Make the decision from current evidence only.
        decision = compare_hotspots(
            report_a, report_b
        )

        # Save an audit record of this investigation.
        saved_record = save_investigation_history(
            graph,
            hotspot_a_id,
            hotspot_b_id,
            decision,
        )

        return {
            "project": "HeatPath",
            "hotspot_reports": [report_a, report_b],
            "previous_investigations": history,
            "decision": decision,
            "saved_investigation_id": (
                saved_record["investigation_id"]
            ),
            "memory_policy": {
                "history_is_context_only": True,
                "current_evidence_controls_decision": True,
                "history_can_override_current_evidence": False,
            },
        }
    finally:
        close = getattr(client, "close", None)
        if callable(close):
            close()


def main():
    parser = argparse.ArgumentParser(
        description="Investigate and compare two HeatPath hotspots."
    )
    parser.add_argument("--a", default="zone_a")
    parser.add_argument("--b", default="zone_b")
    args = parser.parse_args()

    result = run_heatpath(args.a, args.b)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
