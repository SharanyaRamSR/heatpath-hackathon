# HeatPath — Graph-Powered Urban Heat Investigation Agent

HeatPath is a graph-powered investigation agent built with Python and FalkorDB. It compares two urban heat hotspot records by traversing connected risks, supporting evidence, nearby facilities, interventions, and previous investigation records.

HeatPath is designed to avoid unsupported prioritization. When the available records do not justify a defensible decision, it returns `INSUFFICIENT_EVIDENCE` rather than forcing a winner.

## Problem

Urban heat prioritization cannot reliably depend on temperature alone. Investigators need to examine connected risk factors, supporting evidence, data provenance, verification status, and gaps in the available records.

## Solution

HeatPath uses graph relationships to:

- Retrieve hotspot records and their connected risks.
- Trace supporting evidence, nearby facilities, and interventions.
- Identify unverified hotspot records and unsupported risk claims.
- Compare two hotspots using explicit decision-safety checks.
- Return an insufficient-evidence result when required evidence is missing or unverified.
- Retrieve previous investigations and save a persistent audit record for each run.

Investigation history is currently used as context and is not allowed to override current evidence. Historical memory does not yet influence the decision engine.

## Graph Architecture

The synthetic graph uses the following node types:

- `HeatZone` — hotspot records and their metadata.
- `RiskFactor` — connected risk factors.
- `Evidence` — records intended to support an investigation.
- `Facility` — nearby facilities.
- `Intervention` — potential responses to identified risks.
- `InvestigationHistory` — persistent investigation audit records.

Key relationships include:

- `HAS_RISK`
- `SUPPORTED_BY`
- `NEARBY_FACILITY`
- `HAS_INTERVENTION`

Investigation history is stored separately from the hotspot evidence graph.

## Decision-Safety Behavior

HeatPath is designed to:

- Avoid selecting a winner when a hotspot is missing or unverified.
- Avoid treating synthetic data as verified real-world evidence.
- Identify missing or insufficient supporting evidence.
- Avoid using temperature alone as a basis for prioritization.
- Preserve the reasons behind a decision in an audit record.

The current decision engine conservatively returns `INSUFFICIENT_EVIDENCE` even when preliminary checks pass, because a validated prioritization policy has not yet been configured.

## Data and Limitations

Current testing uses synthetic records only. Names such as “Synthetic Hotspot A” and “Fictional thermal observation A” are test fixtures, not observations of actual locations.

A metadata check is not proof that evidence is authentic. Missing dates indicate unknown freshness, not automatically stale evidence.

HeatPath is a prototype. Its current automated tests cover five safety conditions: missing hotspots, synthetic data, unverified hotspots, differing measurement dates, and the absence of a validated prioritization policy. Broader testing, including evidence-quality edge cases and persistent-memory behavior, remains necessary before submission.

## Technology

- Python
- FalkorDB graph database
- `falkordb` Python client
- `python-dotenv`
- Google Colab
- GitHub

## Setup

1. Clone this repository.
2. Install the dependencies.
3. Configure the FalkorDB connection using environment variables.
4. Create or populate the expected synthetic graph before running the agent.

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the following environment variables for your FalkorDB instance:

- `FALKORDB_HOST`
- `FALKORDB_PORT`
- `FALKORDB_USERNAME`
- `FALKORDB_PASSWORD`
- `FALKORDB_GRAPH_NAME`
- `FALKORDB_SSL`

Do not commit passwords, access tokens, or other credentials to GitHub.

Run the agent:

```bash
python heatpath_agent.py --a zone_a --b zone_b
```

The command prints the hotspot investigation reports, previous investigations, decision result, and newly saved investigation ID. Each successful run writes a new `InvestigationHistory` record.

**Important:** The graph must already
