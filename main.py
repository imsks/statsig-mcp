import os
import requests
from fastapi import FastAPI, HTTPException, Query
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from typing import Dict, List, Any

load_dotenv()

app = FastAPI(
    title="Statsig MCP Server",
    description="Model Context Protocol server for Statsig integration",
    version="1.0.0"
)
mcp = FastMCP("statsig-mcp")

STATSIG_API_KEY = os.getenv("STATSIG_API_KEY")

if not STATSIG_API_KEY:
    raise ValueError("STATSIG_API_KEY environment variable is required")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {STATSIG_API_KEY}",
    "statsig-api-key": STATSIG_API_KEY
}

# Base URL for Statsig API
STATSIG_BASE_URL = "https://api.statsig.com/v1"

# Helper function to make Statsig API requests
def make_statsig_request(endpoint: str, method: str = "GET", data: Dict = None) -> Any:
    """Make a request to Statsig API with error handling"""
    url = f"{STATSIG_BASE_URL}/{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data)
        else:
            response = requests.request(method, url, headers=HEADERS, json=data)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Resource not found: {endpoint}")
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid API key or unauthorized")
        else:
            raise HTTPException(status_code=response.status_code, detail=str(e))
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Statsig API error: {str(e)}")

# MCP Tools for Statsig API

# 1. Get Feature Gate Value
@mcp.tool()
def get_feature_gate_value(feature_gate_name: str) -> Dict[str, Any]:
    """Get the value of a specific feature gate"""
    return make_statsig_request(f"feature-gates/{feature_gate_name}")

# 2. List Feature Gates
@mcp.tool()
def list_feature_gates() -> List[str]:
    """List all available feature gates"""
    gates = make_statsig_request("feature-gates")
    if isinstance(gates, list):
        return [gate.get("name", "") for gate in gates if isinstance(gate, dict)]
    return []

# 3. List Experiments
@mcp.tool()
def list_experiments() -> List[Dict[str, Any]]:
    """List all available experiments"""
    return make_statsig_request("experiments")

# 4. Get Experiment
@mcp.tool()
def get_experiment(experiment_name: str) -> Dict[str, Any]:
    """Get details of a specific experiment"""
    return make_statsig_request(f"experiments/{experiment_name}")

# FastAPI HTTP Endpoints (expose MCP tools as HTTP)

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Statsig MCP Server is running",
        "endpoints": {
            "tools": {
                "list_feature_gates": "/tools/list_feature_gates",
                "get_feature_gate_value": "/tools/get_feature_gate_value?feature_gate_name=<name>",
                "list_experiments": "/tools/list_experiments",
                "get_experiment": "/tools/get_experiment?experiment_name=<name>",
                "list_dynamic_configs": "/tools/list_dynamic_configs",
                "get_dynamic_config": "/tools/get_dynamic_config?config_name=<name>"
            },
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "statsig-mcp"}

@app.get("/tools/list_feature_gates")
async def list_feature_gates_endpoint():
    """List all feature gates"""
    try:
        result = list_feature_gates()
        return {"success": True, "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools/get_feature_gate_value")
async def get_feature_gate_value_endpoint(
    feature_gate_name: str = Query(..., description="Name of the feature gate")
):
    """Get value of a specific feature gate"""
    try:
        result = get_feature_gate_value(feature_gate_name)
        return {"success": True, "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools/list_experiments")
async def list_experiments_endpoint():
    """List all experiments"""
    try:
        result = list_experiments()
        return {"success": True, "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools/get_experiment")
async def get_experiment_endpoint(
    experiment_name: str = Query(..., description="Name of the experiment")
):
    """Get details of a specific experiment"""
    try:
        result = get_experiment(experiment_name)
        return {"success": True, "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount MCP server to FastAPI (if FastMCP supports it)
try:
    # Try to integrate MCP server with FastAPI
    if hasattr(mcp, 'router'):
        app.include_router(mcp.router)
    elif hasattr(mcp, 'add_to_fastapi'):
        mcp.add_to_fastapi(app)
except Exception as e:
    # If integration fails, tools are still available via HTTP endpoints above
    print(f"Note: MCP server integration skipped: {e}")