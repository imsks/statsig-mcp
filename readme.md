# Statsig MCP

## Getting Started

1. Setting up a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the server
```bash
uvicorn main:app --reload
```