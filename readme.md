# Statsig MCP Server

A Model Context Protocol (MCP) server for integrating Statsig feature flags, experiments, and configurations.

**⚠️ Important**: This is an MCP server that communicates via **stdio** (not HTTP). It's designed to be used with Cursor or other MCP-compatible clients.

## Quick Start

### 1. Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
STATSIG_API_KEY=console-YOUR-API-KEY
STATSIG_BASE_URL=https://statsigapi.net/console/v1  # Optional, defaults to this
```

Get your API key from [Statsig Console](https://console.statsig.com/).

### 3. Test Server Locally

```bash
python main.py
```

The server will start and wait for stdio input (this is normal for MCP servers). Press Ctrl+C to stop.

## Usage

### Available MCP Tools

The server provides the following MCP tools:

1. **`list_feature_gates`** - List all available feature gates
2. **`get_feature_gate_value`** - Get the value of a specific feature gate
3. **`list_experiments`** - List all available experiments
4. **`get_experiment`** - Get details of a specific experiment

These tools are available in Cursor chat when the MCP server is properly configured.

## Adding to Cursor

**📖 See [MCP_SETUP_GUIDE.md](./MCP_SETUP_GUIDE.md) for detailed setup instructions and troubleshooting.**

### Quick Steps

1. **Open Cursor MCP Config**: `Settings` → `Tools & MCP` → `Edit Config`

2. **Add Your Server Configuration**:

```json
{
  "mcpServers": {
    "statsig": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/statsig-mcp",
      "env": {
        "STATSIG_API_KEY": "console-YOUR-API-KEY"
      }
    }
  }
}
```

**Important Notes:**
- ✅ Use `"python main.py"` (not `uvicorn`)
- ✅ Replace `/path/to/statsig-mcp` with your actual project path
- ✅ Replace `console-YOUR-API-KEY` with your Statsig API key
- ✅ If using virtual environment, use full path to venv's Python: `"/path/to/statsig-mcp/venv/bin/python"`

### Using .env File (Alternative)

If you prefer using the `.env` file, you can omit the `env` section:

```json
{
  "mcpServers": {
    "statsig": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/statsig-mcp"
    }
  }
}
```

The API key will be automatically loaded from your `.env` file in the project directory.

3. **Restart Cursor**:
   - Restart Cursor completely to load the new MCP server
   - Verify it appears in the MCP section (`Settings` → `Tools & MCP`)

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

### Verify MCP Server is Running

1. **Check Cursor MCP Status**:
   - Go to `Settings` → `Tools & MCP`
   - Verify "statsig" appears in the list
   - Status should show as "connected" or "running"

2. **Test Manually**:
   ```bash
   python main.py
   ```
   - Should start without errors
   - Will appear "hung" (waiting for stdio input) - this is normal!
   - Press Ctrl+C to stop

3. **Test in Cursor Chat**:
   - Open Cursor Chat (Cmd+L or Ctrl+L)
   - Ask: "List all my Statsig experiments"
   - Cursor should use the MCP tool and display results

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
├── main.py                  # MCP server implementation
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
├── manifest.json            # MCP server metadata (tools documentation)
├── MCP_SETUP_GUIDE.md       # Detailed setup guide and troubleshooting
└── readme.md               # This file
```

## Key Differences from Statsig Official Server

| Feature | Statsig Official (`statsig-local`) | Your Custom Server (`statsig`) |
|---------|-----------------------------------|--------------------------------|
| **Base URL** | `https://api.statsig.com/v1/mcp` | `https://statsigapi.net/console/v1` (configurable) |
| **Implementation** | Statsig's MCP endpoint | Your own implementation |
| **Control** | Limited | Full control |
| **Customization** | None | Full customization |

**Why use your own server?**
- Use different Statsig API endpoints
- Full control over implementation
- Customize tools and functionality
- Multi-product support (different servers for different products)
