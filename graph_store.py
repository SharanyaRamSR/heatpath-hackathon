
import os

from falkordb import FalkorDB

from config import (
    FALKORDB_HOST,
    FALKORDB_PORT,
    FALKORDB_USERNAME,
    FALKORDB_PASSWORD,
    FALKORDB_GRAPH_NAME,
    validate_database_config,
)


def connect_graph():
    """Connect to FalkorDB and select the HeatPath graph."""
    missing = validate_database_config()

    if missing:
        raise ValueError(
            "Missing database configuration: "
            + ", ".join(missing)
        )

    ssl_enabled = os.getenv(
        "FALKORDB_SSL", "true"
    ).strip().lower() in ("1", "true", "yes")

    client = FalkorDB(
        host=FALKORDB_HOST,
        port=FALKORDB_PORT,
        username=FALKORDB_USERNAME or None,
        password=FALKORDB_PASSWORD,
        ssl=ssl_enabled,
    )

    graph = client.select_graph(FALKORDB_GRAPH_NAME)

    return client, graph
