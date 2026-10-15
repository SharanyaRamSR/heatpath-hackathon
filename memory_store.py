
from datetime import datetime, timezone
import uuid


def get_investigation_history(graph, hotspot_a_id, hotspot_b_id):
    """Retrieve history for this hotspot pair, in either order."""

    result = graph.query(
        """
        MATCH (h:InvestigationHistory)
        WHERE (
            h.hotspot_a_id = $a AND h.hotspot_b_id = $b
        ) OR (
            h.hotspot_a_id = $b AND h.hotspot_b_id = $a
        )
        RETURN h.investigation_id, h.hotspot_a_id,
               h.hotspot_b_id, h.status, h.winner,
               h.created_at_utc, h.summary
        ORDER BY h.created_at_utc DESC
        """,
        {"a": hotspot_a_id, "b": hotspot_b_id},
    )

    fields = [
        "investigation_id",
        "hotspot_a_id",
        "hotspot_b_id",
        "status",
        "winner",
        "created_at_utc",
        "summary",
    ]

    return [
        dict(zip(fields, row))
        for row in result.result_set
    ]


def save_investigation_history(
    graph,
    hotspot_a_id,
    hotspot_b_id,
    decision,
):
    """
    Save an audit record of a comparison.

    Historical records provide context only. They are not
    evidence that a past decision was correct.
    """

    investigation_id = str(uuid.uuid4())

    record = {
        "investigation_id": investigation_id,
        "hotspot_a_id": hotspot_a_id,
        "hotspot_b_id": hotspot_b_id,
        "status": decision.get(
            "status", "INSUFFICIENT_EVIDENCE"
        ),
        "winner": decision.get("winner") or "",
        "created_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "summary": "; ".join(
            decision.get("reasons", [])
        ),
        "record_purpose": "audit_trail",
        "is_final_real_world_conclusion": False,
    }

    graph.query(
        """
        CREATE (h:InvestigationHistory {
            investigation_id: $investigation_id,
            hotspot_a_id: $hotspot_a_id,
            hotspot_b_id: $hotspot_b_id,
            status: $status,
            winner: $winner,
            created_at_utc: $created_at_utc,
            summary: $summary,
            record_purpose: $record_purpose,
            is_final_real_world_conclusion:
                $is_final_real_world_conclusion
        })
        """,
        record,
    )

    return record
