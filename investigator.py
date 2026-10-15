
def _query_rows(graph, query, params=None):
    """Execute a FalkorDB query and return its rows."""
    result = graph.query(query, params or {})
    return result.result_set


def investigate_hotspot(graph, hotspot_id):
    """Retrieve a synthetic or real hotspot and connected records."""

    hotspot_rows = _query_rows(
        graph,
        """
        MATCH (h:HeatZone {id: $hotspot_id})
        RETURN h.id, h.name, h.temperature_c,
               h.measurement_date, h.data_status
        """,
        {"hotspot_id": hotspot_id},
    )

    if not hotspot_rows:
        return {
            "status": "NOT_FOUND",
            "hotspot_id": hotspot_id,
        }

    row = hotspot_rows[0]

    report = {
        "status": "FOUND",
        "hotspot": {
            "id": row[0],
            "name": row[1],
            "temperature_c": row[2],
            "measurement_date": row[3],
            "data_status": row[4],
        },
        "risks": [],
        "evidence": [],
        "nearby_facilities": [],
        "interventions": [],
        "warnings": [],
    }

    linked_queries = [
        (
            "risks",
            """
            MATCH (h:HeatZone {id: $hotspot_id})
                  -[:HAS_RISK]->(r:RiskFactor)
            RETURN r.id, r.name, r.severity, r.data_status
            """,
            ["id", "name", "severity", "data_status"],
        ),
        (
            "evidence",
            """
            MATCH (h:HeatZone {id: $hotspot_id})
                  -[:SUPPORTED_BY]->(e:Evidence)
            RETURN e.id, e.name, e.confidence,
                   e.source_type, e.data_status
            """,
            [
                "id",
                "name",
                "confidence",
                "source_type",
                "data_status",
            ],
        ),
        (
            "nearby_facilities",
            """
            MATCH (h:HeatZone {id: $hotspot_id})
                  -[:NEARBY_FACILITY]->(f:Facility)
            RETURN f.id, f.name, f.facility_type, f.data_status
            """,
            ["id", "name", "facility_type", "data_status"],
        ),
        (
            "interventions",
            """
            MATCH (h:HeatZone {id: $hotspot_id})
                  -[:HAS_INTERVENTION]->(i:Intervention)
            RETURN i.id, i.name, i.data_status
            """,
            ["id", "name", "data_status"],
        ),
    ]

    for section, query, fields in linked_queries:
        rows = _query_rows(
            graph,
            query,
            {"hotspot_id": hotspot_id},
        )
        report[section] = [
            dict(zip(fields, values))
            for values in rows
        ]

    if report["hotspot"]["data_status"] != "verified":
        report["warnings"].append(
            "Hotspot data is not verified; do not make "
            "a real-world prioritization decision."
        )

    if not report["evidence"]:
        report["warnings"].append(
            "No directly linked evidence was found."
        )

    verified_evidence = [
        evidence
        for evidence in report["evidence"]
        if evidence.get("data_status") == "verified"
    ]

    if report["risks"] and not verified_evidence:
        for risk in report["risks"]:
            report["warnings"].append(
                f"Risk '{risk.get('name', risk.get('id'))}' "
                "has no directly linked verified evidence."
            )

    return report
