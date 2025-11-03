# Statsig MCP Server

A Model Context Protocol (MCP) server for integrating Statsig feature flags, experiments, and configurations via FastAPI.

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
STATSIG_API_KEY=console-YOUR-API-KEY
```

Get your API key from [Statsig Console](https://console.statsig.com/).

### 3. Run Server

```bash
uvicorn main:app --reload
```

Server runs at: `http://127.0.0.1:8000`

## Usage

### Available Endpoints

- **Health Check**: `GET /health`
- **API Docs**: `http://127.0.0.1:8000/docs` (Interactive Swagger UI)

### Tools

#### List Feature Gates
```bash
curl http://127.0.0.1:8000/tools/list_feature_gates
```

#### Get Feature Gate Value
```bash
curl "http://127.0.0.1:8000/tools/get_feature_gate_value?feature_gate_name=YOUR_GATE_NAME"
```

#### List Experiments
```bash
curl http://127.0.0.1:8000/tools/list_experiments
```

#### Get Experiment Details
```bash
curl "http://127.0.0.1:8000/tools/get_experiment?experiment_name=YOUR_EXPERIMENT_NAME"
```

## Adding to Cursor

### Steps

1. **Open Cursor Settings**: `Settings` → `Tools & MCP` → `Edit Config`

2. **Copy Configuration**: Open `cursor-mcp-config.json` in this project and copy the entire JSON

3. **Update Path**: Replace `/YOUR/PATH/TO/statsig-mcp` with your actual project path

```json
{
  "mcpServers": {
    "statsig": {
      "command": "python",
      "args": [
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
      ],
      "cwd": "/path/to/statsig-mcp",
      "env": {
        "STATSIG_API_KEY": "console-YOUR-API-KEY"
      }
    }
  }
}
```

3. **Update Configuration**:
   - Replace `/path/to/statsig-mcp` with the actual path to this project directory
   - Replace `console-YOUR-API-KEY` with your Statsig API key (or remove `env` section if using `.env` file)
   - Ensure Python and uvicorn are available in your PATH

4. **Restart Cursor**:
   - Restart Cursor to load the new MCP server
   - Verify it appears in the MCP section

### Method 2: Using .env File

If you prefer using the `.env` file (already set up), you can omit the `env` section:

```json
{
  "mcpServers": {
    "statsig": {
      "command": "python",
      "args": [
        "-m",
        "uvicorn",
        "main:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
      ],
      "cwd": "/path/to/statsig-mcp"
    }
  }
}
```

The API key will be automatically loaded from your `.env` file in the project directory.

### Verify Integration

Once configured, you can use Statsig MCP tools directly in Cursor chat:
- List feature gates
- Get feature gate values
- List experiments
- Get experiment details

## Testing

### Test in Cursor Chat

1. **Open Cursor Chat** (Cmd+L or Ctrl+L)

2. **Test List Experiments** - Type one of these:
   - `List all experiments`
   - `Show me all my Statsig experiments`
   - `What experiments do I have?`

3. **Cursor will automatically**:
   - Use the `list_experiments` MCP tool
   - Display the results in chat

### Test via HTTP (Alternative Method)

If you want to test the HTTP endpoint directly:

```bash
# Make sure server is running first
uvicorn main:app --reload

# Then in another terminal:
curl http://127.0.0.1:8000/tools/list_experiments
```

### Verify MCP Server is Running

1. **Check Cursor MCP Status**:
   - Go to `Settings` → `Tools & MCP`
   - Verify "statsig" appears in the list
   - Status should show as "connected" or "running"

2. **Check Server Logs**:
   - When Cursor calls the MCP tool, you should see logs in the terminal where uvicorn is running
   - Look for incoming requests

3. **Health Check**:
   ```bash
   curl http://127.0.0.1:8000/health
   ```
   Should return: `{"status":"healthy","service":"statsig-mcp"}`

### Troubleshooting

**Issue: "MCP server not found"**
- Verify the `cwd` path in your Cursor config is correct
- Ensure Python virtual environment is activated where needed

**Issue: "Tool not available in chat"**
- Restart Cursor after adding MCP config
- Check that the server started successfully (check logs)

**Issue: "403 Forbidden" or "401 Unauthorized"**
- Verify `.env` file has correct `STATSIG_API_KEY`
- Check API key format (should start with `console-`)
- Verify API key has proper permissions in Statsig Console

## Requirements

- Python 3.10+
- Statsig Console API Key

## Project Structure

```
statsig-mcp/
├── main.py              # FastAPI server and MCP tools
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── manifest.json        # MCP server metadata
└── readme.md           # This file
```
