
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = "HeatPath"
PROJECT_VERSION = "0.1.0"

FALKORDB_HOST = os.getenv("FALKORDB_HOST", "")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6379"))
FALKORDB_USERNAME = os.getenv("FALKORDB_USERNAME", "")
FALKORDB_PASSWORD = os.getenv("FALKORDB_PASSWORD", "")
FALKORDB_GRAPH_NAME = os.getenv(
    "FALKORDB_GRAPH_NAME",
    "heatpath_synthetic",
)

def validate_database_config():
    missing = []

    if not FALKORDB_HOST:
        missing.append("FALKORDB_HOST")

    if not FALKORDB_PASSWORD:
        missing.append("FALKORDB_PASSWORD")

    return missing
