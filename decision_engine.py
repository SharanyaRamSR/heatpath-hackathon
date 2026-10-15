
from datetime import date


def compare_hotspots(report_a, report_b):
    """
    Compare two investigation reports conservatively.

    This initial decision policy refuses to rank hotspots
    when data is synthetic, evidence is unverified, or the
    prioritization policy has not been validated.
    """

    reports = [report_a, report_b]

    for report in reports:
        if report.get("status") != "FOUND":
            return {
                "status": "INSUFFICIENT_EVIDENCE",
                "winner": None,
                "reasons": [
                    "Both hotspot records must be found."
                ],
            }

    hotspot_a = report_a["hotspot"]
    hotspot_b = report_b["hotspot"]
    reasons = []

    if (
        hotspot_a.get("data_status") != "verified"
        or hotspot_b.get("data_status") != "verified"
    ):
        reasons.append(
            "One or both hotspot records are not verified."
        )

    date_a = hotspot_a.get("measurement_date")
    date_b = hotspot_b.get("measurement_date")

    if not date_a or not date_b:
        reasons.append(
            "A measurement date is missing."
        )
    elif date_a != date_b:
        reasons.append(
            "Measurement dates differ; observations may "
            "not be directly comparable."
        )
    else:
        try:
            date.fromisoformat(date_a)
        except (TypeError, ValueError):
            reasons.append(
                "Measurement dates must use YYYY-MM-DD format."
            )

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

    if reasons:
        return {
            "status": "INSUFFICIENT_EVIDENCE",
            "winner": None,
            "hotspots_compared": [
                hotspot_a.get("id"),
                hotspot_b.get("id"),
            ],
            "reasons": reasons,
        }

    return {
        "status": "INSUFFICIENT_EVIDENCE",
        "winner": None,
        "hotspots_compared": [
            hotspot_a.get("id"),
            hotspot_b.get("id"),
        ],
        "reasons": [
            "A validated prioritization policy is not yet "
            "configured. Temperature alone must not determine "
            "which hotspot receives priority."
        ],
    }
