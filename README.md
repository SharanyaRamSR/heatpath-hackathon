HeatPath — Graph-Powered Urban Heat Investigation Agent

HeatPath is an AI-agent project designed to compare urban heat hotspots by investigating connected risks, supporting evidence, and historical investigations using FalkorDB.

Rather than forcing a ranking from incomplete information, HeatPath aims to explain what the graph supports, identify missing evidence, and return an explicit insufficient-evidence result when a defensible decision cannot be made.

Problem

Urban heat prioritization requires more than comparing temperature values. Decision-makers also need supporting evidence, connected risks, relevant facilities, and an understanding of evidence quality and limitations.

Proposed Solution

HeatPath is being developed to:

- Traverse graph relationships to investigate connected risks and evidence.
- Explain findings using traceable graph records and relationships.
- Identify unsupported risk claims and missing evidence metadata.
- Use persistent investigation history as context without allowing it to override current verified evidence.
- Avoid unsupported hotspot rankings when the evidence is insufficient.

Technology

- Graph database: FalkorDB
- Language: Python
- Development environment: Google Colab
- Source control: GitHub

Data and Safety

Initial development and testing use synthetic hotspot records. Synthetic data is intended to validate application logic only; it does not support claims about actual locations or real-world heat risk.

HeatPath is designed to distinguish metadata validation from evidence verification. Missing dates indicate unknown freshness, not necessarily stale evidence.

Hackathon Scope

Primary focus: Agents That Act on Connected Data.

Additional focus, subject to implementation and testing: Agent Memory and Coordination.

The implementation, tests, and demonstration will be developed and documented during the permitted hackathon build window.

Project Status

In development. Graph-dependent reasoning, persistent memory behavior, automated tests, and the complete demonstration workflow must be verified before the project is considered submission-ready.

License

No open-source license has been selected yet.
