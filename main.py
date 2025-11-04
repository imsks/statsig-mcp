import os
import sys
import logging
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

load_dotenv()

logger.info("=" * 60)
logger.info("Starting Statsig MCP Server")
logger.info("=" * 60)

# Initialize FastMCP server
mcp = FastMCP("statsig-mcp")
logger.info("✓ FastMCP server initialized")

# Get API key from environment
STATSIG_API_KEY = os.getenv("STATSIG_API_KEY")

# Allow STATSIG_BASE_URL to be configurable via environment variable
STATSIG_BASE_URL = os.getenv("STATSIG_BASE_URL", "https://statsigapi.net/console/v1")

if not STATSIG_API_KEY:
    logger.error("✗ STATSIG_API_KEY environment variable is required")
    print("ERROR: STATSIG_API_KEY environment variable is required", file=sys.stderr)
    sys.exit(1)

logger.info(f"✓ STATSIG_API_KEY loaded (length: {len(STATSIG_API_KEY)})")
logger.info(f"✓ STATSIG_BASE_URL: {STATSIG_BASE_URL}")

# Statsig API uses statsig-api-key header (not Authorization Bearer)
HEADERS = {
    "Content-Type": "application/json",
    "statsig-api-key": STATSIG_API_KEY
}

# # Helper function to make Statsig API requests
# def make_statsig_request(endpoint: str, method: str = "GET", data: Dict = None) -> Any:
#     """Make a request to Statsig API with error handling"""
#     url = f"{STATSIG_BASE_URL}/{endpoint}"
#     logger.info(f"→ Making {method} request to: {url}")
#     try:
#         if method == "GET":
#             response = requests.get(url, headers=HEADERS)
#         elif method == "POST":
#             response = requests.post(url, headers=HEADERS, json=data)
#         else:
#             response = requests.request(method, url, headers=HEADERS, json=data)
        
#         logger.info(f"✓ Response status: {response.status_code}")
#         response.raise_for_status()
#         result = response.json()
#         logger.info(f"✓ Successfully received response from Statsig API")
#         return result
#     except requests.exceptions.HTTPError as e:
#         error_detail = f"Statsig API error: {response.status_code}"
#         try:
#             error_body = response.json()
#             error_detail = f"{error_detail} - {error_body}"
#         except:
#             error_detail = f"{error_detail} - {response.text}"
        
#         logger.error(f"✗ {error_detail}")
#         # For MCP, we raise exceptions that will be properly formatted
#         raise Exception(f"Statsig API error ({response.status_code}): {error_detail}")
#     except requests.exceptions.RequestException as e:
#         logger.error(f"✗ Statsig API request failed: {str(e)}")
#         raise Exception(f"Statsig API request failed: {str(e)}")

# MCP Tools for Statsig API

@mcp.tool()
def ping() -> str:
    return "pong"

# # 1. Get Feature Gate Value
# @mcp.tool()
# def get_feature_gate_value(feature_gate_name: str) -> Dict[str, Any]:
#     """Get the value of a specific feature gate"""
#     logger.info(f"🔧 Tool called: get_feature_gate_value(feature_gate_name='{feature_gate_name}')")
#     result = make_statsig_request(f"gates/{feature_gate_name}")
#     logger.info(f"✓ Tool completed: get_feature_gate_value")
#     return result

# # 2. List Feature Gates
# @mcp.tool()
# def list_feature_gates() -> List[str]:
#     """List all available feature gates"""
#     logger.info(f"🔧 Tool called: list_feature_gates()")
#     gates = make_statsig_request("gates")
#     if isinstance(gates, list):
#         result = [gate.get("name", "") for gate in gates if isinstance(gate, dict)]
#         logger.info(f"✓ Tool completed: list_feature_gates (found {len(result)} gates)")
#         return result
#     logger.info(f"✓ Tool completed: list_feature_gates (empty result)")
#     return []

# # 3. List Experiments
# @mcp.tool()
# def list_experiments() -> List[Dict[str, Any]]:
#     """List all available experiments"""
#     logger.info(f"🔧 Tool called: list_experiments()")
#     result = make_statsig_request("experiments")
#     logger.info(f"✓ Tool completed: list_experiments (found {len(result) if isinstance(result, list) else 'N/A'} experiments)")
#     return result

# # 4. Get Experiment
# @mcp.tool()
# def get_experiment(experiment_name: str) -> Dict[str, Any]:
#     """Get details of a specific experiment"""
#     logger.info(f"🔧 Tool called: get_experiment(experiment_name='{experiment_name}')")
#     result = make_statsig_request(f"experiments/{experiment_name}")
#     logger.info(f"✓ Tool completed: get_experiment")
#     return result

# Register tools with logging
logger.info("✓ Registering MCP tools:")
logger.info("  - list_feature_gates")
logger.info("  - get_feature_gate_value")
logger.info("  - list_experiments")
logger.info("  - get_experiment")
logger.info("=" * 60)
logger.info("MCP Server ready and waiting for stdio input...")
logger.info("=" * 60)

# Run the MCP server via stdio
# This is the entry point when run as an MCP server
if __name__ == "__main__":
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("\n✓ Server stopped by user")
    except Exception as e:
        logger.error(f"✗ Server error: {str(e)}")
        raise