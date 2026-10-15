from datetime import datetime, timezone
import uuid

def get_investigation_history(graph, hotspot_a_id, hotspot_b_id):
"""Read history using both legacy and current field names."""

result = graph.query(
    """
    MATCH (h:InvestigationHistory)
    WHERE (
        h.hotspot_a_id = $a AND h.hotspot_b_id = $b
    ) OR (
        h.hotspot_a_id = $b AND h.hotspot_b_id = $a
    )
    RETURN properties(h)
    ORDER BY h.investigation_id
    """,
    {"a": hotspot_a_id, "b": hotspot_b_id},
)

history = []

for row in result.result_set:
    props = dict(row[0])

    history.append({
        "investigation_id": props.get("investigation_id"),
        "hotspot_a_id": props.get("hotspot_a_id"),
        "hotspot_b_id": props.get("hotspot_b_id"),
        "status": props.get(
            "decision_status",
            props.get("status"),
        ),
        "winner": props.get("winner"),
        "created_at_utc": props.get("created_at_utc"),
        "summary": props.get(
            "summary",
            "; ".join(props.get("reasons", [])),
        ),
        "data_provenance": props.get("data_provenance"),
        "comparison_readiness": props.get("comparison_readiness"),
        "memory_type": props.get("memory_type"),
        "is_final_real_world_conclusion": props.get(
            "is_final_real_world_conclusion"
        ),
    })

history.sort(
    key=lambda item: item.get("created_at_utc") or "",
    reverse=True,
)

return history

def save_investigation_history(
graph,
hotspot_a_id,
hotspot_b_id,
decision,
):
"""Save an audit record; history never overrides current evidence."""

investigation_id = str(uuid.uuid4())
reasons = decision.get("reasons", [])

record = {
    "investigation_id": investigation_id,
    "hotspot_a_id": hotspot_a_id,
    "hotspot_b_id": hotspot_b_id,
    "decision_status": decision.get(
        "status", "INSUFFICIENT_EVIDENCE"
    ),
    "winner": decision.get("winner") or "",
    "created_at_utc": datetime.now(
        timezone.utc
    ).isoformat(),
    "reasons": reasons,
    "summary": "; ".join(reasons),
    "memory_type": "investigation_history",
    "data_provenance": "current_investigation",
    "record_purpose": "audit_trail",
    "is_final_real_world_conclusion": False,
}

graph.query(
    """
    CREATE (h:InvestigationHistory {
        investigation_id: $investigation_id,
        hotspot_a_id: $hotspot_a_id,
        hotspot_b_id: $hotspot_b_id,
        decision_status: $decision_status,
        winner: $winner,
        created_at_utc: $created_at_utc,
        reasons: $reasons,
        summary: $summary,
        memory_type: $memory_type,
        data_provenance: $data_provenance,
        record_purpose: $record_purpose,
        is_final_real_world_conclusion:
            $is_final_real_world_conclusion
    })
    """,
    record,
)

return record
