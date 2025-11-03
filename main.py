import os
import requests
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

STATSIG_API_KEY = os.getenv("STATSIG_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {STATSIG_API_KEY}"
}

# Tools for Statsig API

# 1. Get Feature Gate Value
def get_feature_gate_value(feature_gate_name: str) -> str:
    url = f"https://api.statsig.com/v1/feature-gates/{feature_gate_name}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# 2. List Feature Gates
def list_feature_gates() -> list[str]:
    url = "https://api.statsig.com/v1/feature-gates"
    response = requests.get(url, headers=HEADERS)
    return [gate["name"] for gate in response.json()]

@app.get("/")
def root():
    return {"message": "Statsig MCP Server is running"}