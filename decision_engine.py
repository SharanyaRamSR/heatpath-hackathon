from datetime import date

GRAPH_SECTIONS = {
    "risks": "HAS_RISK",
    "evidence": "SUPPORTED_BY",
    "nearby_facilities": "NEARBY_FACILITY",
    "interventions": "HAS_INTERVENTION",
}


def _record_key(record):
    """Create a stable comparison key for a connected record."""
    return str(record.get("id") or record.get("name") or "unknown")


def compare_connected_records(report_a, report_b):
    """
    Compare graph-connected records without assigning priority.
    Findings describe retrieved records, not real-world truth.
    """
    comparison = {
        "hotspots": {},
        "differences": {},
        "interpretation": (
            "Differences describe connected graph records only. "
            "They do not establish real-world severity or priority."
        ),
    }

    for label, report in [("a", report_a), ("b", report_b)]:
        hotspot = report.get("hotspot", {})
        connected = {}

        for section, relationship in GRAPH_SECTIONS.items():
            connected[section] = [
                {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "data_status": item.get("data_status"),
                    "relationship": relationship,
                }
                for item in report.get(section, [])
            ]

        comparison["hotspots"][label] = {
            "hotspot_id": hotspot.get("id"),
            "connected_records": connected,
        }

    for section in GRAPH_SECTIONS:
        records_a = {
            _record_key(item): item
            for item in report_a.get(section, [])
        }
        records_b = {
            _record_key(item): item
            for item in report_b.get(section, [])
        }

        comparison["differences"][section] = {
            "only_in_a": [
                records_a[key]
                for key in sorted(records_a.keys() - records_b.keys())
            ],
            "only_in_b": [
                records_b[key]
                for key in sorted(records_b.keys() - records_a.keys())
            ],
            "shared": [
                records_a[key]
                for key in sorted(records_a.keys() & records_b.keys())
            ],
        }

    return comparison


def compare_hotspots(report_a, report_b):
    """
    Compare two investigation reports conservatively.
    No winner is selected without a validated prioritization policy.
    """
    reports = [report_a, report_b]

    for report in reports:
        if report.get("status") != "FOUND":
            return {
                "status": "INSUFFICIENT_EVIDENCE",
                "winner": None,
                "reasons": ["Both hotspot records must be found."],
            }

    hotspot_a = report_a["hotspot"]
    hotspot_b = report_b["hotspot"]
    reasons = []

    graph_comparison = compare_connected_records(report_a, report_b)

    if (
        hotspot_a.get("data_status") != "verified"
        or hotspot_b.get("data_status") != "verified"
    ):
        reasons.append("One or both hotspot records are not verified.")

    date_a = hotspot_a.get("measurement_date")
    date_b = hotspot_b.get("measurement_date")

    if not date_a or not date_b:
        reasons.append("A measurement date is missing.")
    elif date_a != date_b:
        reasons.append(
            "Measurement dates differ; observations may not be directly comparable."
        )
    else:
        try:
            date.fromisoformat(date_a)
        except (TypeError, ValueError):
            reasons.append("Measurement dates must use YYYY-MM-DD format.")

    for report in reports:
        verified_evidence = [
            evidence
            for evidence in report.get("evidence", [])
            if evidence.get("data_status") == "verified"
        ]

        if not verified_evidence:
            reasons.append(
                f"{report['hotspot'].get('name', 'A hotspot')} "
                "has no directly linked verified evidence."
            )

    result_base = {
        "winner": None,
        "hotspots_compared": [hotspot_a.get("id"), hotspot_b.get("id")],
        "graph_comparison": graph_comparison,
    }

    if reasons:
        return {
            **result_base,
            "status": "INSUFFICIENT_EVIDENCE",
            "reasons": reasons,
        }

    return {
        **result_base,
        "status": "INSUFFICIENT_EVIDENCE",
        "reasons": [
            "A validated prioritization policy is not yet configured. "
            "Temperature alone must not determine which hotspot receives priority."
        ],
    }
