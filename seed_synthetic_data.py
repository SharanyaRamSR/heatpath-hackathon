
from graph_store import connect_graph


def seed_synthetic_data():
    """Create repeatable synthetic data for HeatPath testing."""
    client, graph = connect_graph()

    queries = [
        """
        MERGE (h:Hotspot {id: 'zone_a'})
        SET h.name = 'Synthetic Hotspot A',
            h.temperature_c = 40.1,
            h.measurement_date = '2026-10-10',
            h.data_status = 'synthetic'
        """,
        """
        MERGE (h:Hotspot {id: 'zone_b'})
        SET h.name = 'Synthetic Hotspot B',
            h.temperature_c = 39.5,
            h.measurement_date = '2026-10-10',
            h.data_status = 'synthetic'
        """,
        """
        MERGE (r:Risk {id: 'risk_a'})
        SET r.name = 'Low shade',
            r.severity = 0.8,
            r.data_status = 'synthetic'
        """,
        """
        MERGE (r:Risk {id: 'risk_b'})
        SET r.name = 'Very low vegetation',
            r.severity = 0.9,
            r.data_status = 'synthetic'
        """,
        """
        MERGE (e:Evidence {id: 'evidence_a'})
        SET e.name = 'Fictional thermal observation A',
            e.confidence = 0.9,
            e.source_type = 'synthetic_test',
            e.data_status = 'synthetic'
        """,
        """
        MERGE (e:Evidence {id: 'evidence_b'})
        SET e.name = 'Fictional thermal observation B',
            e.confidence = 0.9,
            e.source_type = 'synthetic_test',
            e.data_status = 'synthetic'
        """,
        """
        MERGE (f:Facility {id: 'facility_a'})
        SET f.name = 'Fictional Community Clinic A',
            f.facility_type = 'clinic',
            f.data_status = 'synthetic'
        """,
        """
        MERGE (i:Intervention {id: 'intervention_a'})
        SET i.name = 'Increase shade coverage',
            i.data_status = 'synthetic'
        """,
        """
        MATCH (h:Hotspot {id: 'zone_a'}),
              (r:Risk {id: 'risk_a'})
        MERGE (h)-[:HAS_RISK]->(r)
        """,
        """
        MATCH (h:Hotspot {id: 'zone_b'}),
              (r:Risk {id: 'risk_b'})
        MERGE (h)-[:HAS_RISK]->(r)
        """,
        """
        MATCH (h:Hotspot {id: 'zone_a'}),
              (e:Evidence {id: 'evidence_a'})
        MERGE (h)-[:SUPPORTED_BY]->(e)
        """,
        """
        MATCH (h:Hotspot {id: 'zone_b'}),
              (e:Evidence {id: 'evidence_b'})
        MERGE (h)-[:SUPPORTED_BY]->(e)
        """,
        """
        MATCH (h:Hotspot {id: 'zone_a'}),
              (f:Facility {id: 'facility_a'})
        MERGE (h)-[:NEARBY_FACILITY]->(f)
        """,
        """
        MATCH (h:Hotspot {id: 'zone_a'}),
              (i:Intervention {id: 'intervention_a'})
        MERGE (h)-[:HAS_INTERVENTION]->(i)
        """,
    ]

    for query in queries:
        graph.query(query)

    print("Synthetic HeatPath graph data seeded successfully.")
    print("Hotspots: zone_a, zone_b")
    print("All records are synthetic, not real-world findings.")

    return client


if __name__ == "__main__":
    seed_synthetic_data()
