import os
import sys
import logging
import requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Dict, List, Any

# Configure logging - but only log to stderr, not stdout
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stderr  # Important: log to stderr, not stdout
)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize FastMCP server FIRST, before any logging that might interfere
mcp = FastMCP("statsig-mcp")

# Get API key from environment
STATSIG_API_KEY = os.getenv("STATSIG_API_KEY")
STATSIG_BASE_URL = os.getenv("STATSIG_BASE_URL", "https://statsigapi.net/console/v1")

if not STATSIG_API_KEY:
    logger.error("✗ STATSIG_API_KEY environment variable is required")
    sys.exit(1)

# Statsig API uses statsig-api-key header
HEADERS = {
    "Content-Type": "application/json",
    "statsig-api-key": STATSIG_API_KEY
}

# Helper function to make Statsig API requests
def make_statsig_request(endpoint: str, method: str = "GET", data: Dict = None) -> Any:
    """Make a request to Statsig API with error handling"""
    url = f"{STATSIG_BASE_URL}/{endpoint}"
    logger.info(f"→ Making {method} request to: {url}")
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data)
        else:
            response = requests.request(method, url, headers=HEADERS, json=data)
        
        logger.info(f"✓ Response status: {response.status_code}")
        response.raise_for_status()
        result = response.json()
        logger.info(f"✓ Successfully received response from Statsig API")
        return result
    except requests.exceptions.HTTPError as e:
        error_detail = f"Statsig API error: {response.status_code}"
        try:
            error_body = response.json()
            error_detail = f"{error_detail} - {error_body}"
        except:
            error_detail = f"{error_detail} - {response.text}"
        
        logger.error(f"✗ {error_detail}")
        raise Exception(f"Statsig API error ({response.status_code}): {error_detail}")
    except requests.exceptions.RequestException as e:
        logger.error(f"✗ Statsig API request failed: {str(e)}")
        raise Exception(f"Statsig API request failed: {str(e)}")

# MCP Tools - define them
@mcp.tool()
def ping() -> str:
    """Simple ping tool for testing"""
    return "pong"

@mcp.tool()
def get_feature_gate_value(feature_gate_name: str) -> Dict[str, Any]:
    """Get the value of a specific feature gate"""
    logger.info(f"🔧 Tool called: get_feature_gate_value(feature_gate_name='{feature_gate_name}')")
    result = make_statsig_request(f"gates/{feature_gate_name}")
    logger.info(f"✓ Tool completed: get_feature_gate_value")
    return result

@mcp.tool()
def list_feature_gates() -> List[str]:
    """List all available feature gates"""
    logger.info(f"🔧 Tool called: list_feature_gates()")
    gates = make_statsig_request("gates")
    if isinstance(gates, list):
        result = [gate.get("name", "") for gate in gates if isinstance(gate, dict)]
        logger.info(f"✓ Tool completed: list_feature_gates (found {len(result)} gates)")
        return result
    logger.info(f"✓ Tool completed: list_feature_gates (empty result)")
    return []

@mcp.tool()
def list_experiments() -> List[Dict[str, Any]]:
    """List all available experiments"""
    logger.info(f"🔧 Tool called: list_experiments()")
    result = make_statsig_request("experiments")
    logger.info(f"✓ Tool completed: list_experiments (found {len(result) if isinstance(result, list) else 'N/A'} experiments)")
    return result

@mcp.tool()
def get_experiment(experiment_name: str) -> Dict[str, Any]:
    """Get details of a specific experiment"""
    logger.info(f"🔧 Tool called: get_experiment(experiment_name='{experiment_name}')")
    result = make_statsig_request(f"experiments/{experiment_name}")
    logger.info(f"✓ Tool completed: get_experiment")
    return result

# Run the MCP server via stdio
if __name__ == "__main__":
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("\n✓ Server stopped by user")
    except Exception as e:
        logger.error(f"✗ Server error: {str(e)}")
        raise