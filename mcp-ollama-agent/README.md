# 🧠 MCP Ollama Agent

A local AI agent that connects Ollama LLMs with external tools using [MCP (Model Context Protocol)](https://github.com/mark3labs/mcphost) and serves them via custom MCP servers.

---

## 📚 Table of Contents

- [🧠 MCP Ollama Agent](#-mcp-ollama-agent)
  - [📚 Table of Contents](#-table-of-contents)
  - [📘 Background](#-background)
    - [MCP Overview](#mcp-overview)
    - [Ollama Overview](#ollama-overview)
    - [`uv` Python Package Manager](#uv-python-package-manager)
      - [Installation:](#installation)
      - [Quick Usage:](#quick-usage)
  - [🛠 Prerequisites](#-prerequisites)
    - [Install MCPHost](#install-mcphost)
  - [⚙️ Project Setup](#️-project-setup)
  - [🧩 Ollama + MCPHost Configuration](#-ollama--mcphost-configuration)
    - [Common Flags](#common-flags)
    - [In-Chat Commands](#in-chat-commands)
    - [MCP Servers Configuration](#mcp-servers-configuration)
      - [Example (`mcp.json`):](#example-mcpjson)
    - [System Prompt Configuration](#system-prompt-configuration)
  - [🌦️ Weather Server Setup (Example)](#️-weather-server-setup-example)
  - [🔍 MCP Inspector (Debugging Tool)](#-mcp-inspector-debugging-tool)

---

## 📘 Background

### MCP Overview

**Model Context Protocol (MCP)** connects local LLMs with external tools and resources:

* `@mcp.resource()`: Used like a GET request; provides information to the model.
* `@mcp.tool()`: Similar to a POST request; defines callable tools.
* `@mcp.prompt()`: Used to templatize prompts.

**Communication Architecture:**

* MCP initialization: Client and server exchange capabilities.
* Data exchange uses **JSON-RPC** over:

  * `stdio` for local servers
  * `Streamable HTTP` (Server-Sent Events) for external servers

No need for frameworks like Agent2Agent (A2A) or MCP if the local model doesn’t interact with external tools/agents.

---

### Ollama Overview

**Ollama** is a CLI tool to run, create, and share LLMs locally.

* Install: [Ollama Installation](https://ollama.com/download/windows)
* Start server:

  ```bash
  ollama serve
  ```
* Browse models: [Ollama Models](https://ollama.com/search) (Filter for tool support)
* Run a model:

  ```bash
  ollama run <model-name>
  ```

**Useful Commands:**

```bash
ollama             # List all commands
ollama list        # Show downloaded models
ollama pull <model-name>  # Download a model
ollama run <model-name>   # Run a model
```

**Tip (Windows + VS Code):**

1. Use `where ollama` in CMD to locate installation path.
2. Ensure the path is in the system `%PATH%`.
3. Restart VS Code if necessary.

Visit `http://localhost:11434/` to confirm Ollama is running.

---

### `uv` Python Package Manager

[`uv`](https://www.datacamp.com/tutorial/python-uv) is a fast Python package and project manager written in Rust.

#### Installation:

```bash
pip install uv
```

#### Quick Usage:

```bash
uv init <project-name>
cd <project-name>
uv venv
uv add scikit-learn xgboost
uv remove scikit-learn
uv run hello.py
```

---

## 🛠 Prerequisites

To enable local LLM interaction with external tools via MCP, install the following:

### Install MCPHost

1. Install Go: [https://go.dev/doc/install](https://go.dev/doc/install)
2. Run:

   ```bash
   go install github.com/mark3labs/mcphost@latest
   ```

---

## ⚙️ Project Setup

```bash
uv init mcp-ollama-agent
cd mcp-ollama-agent
uv venv
source .venv/Scripts/activate
uv add mcp[cli] httpx
```

---

## 🧩 Ollama + MCPHost Configuration

By default, `mcphost` uses Anthropic’s Claude model. Use Ollama with:

```bash
mcphost -m ollama:qwen2.5:3b
```

### Common Flags

* `--config <file>`: Custom config file (default: `~/.mcp.json`)
* `--system-prompt <file>`: Path to system prompt JSON file
* `--debug`: Enable debug logging
* `--message-window <int>`: Messages in memory (default: 10)
* `-m` or `--model`: Specify model (`ollama:<model-name>`)

### In-Chat Commands

* `/help`: List commands
* `/tools`: Show available tools
* `/servers`: Show configured servers
* `/history`: Show conversation history
* `/quit`: Exit
* `Ctrl + C`: Force quit

---

### MCP Servers Configuration

If `~/.mcp.json` doesn’t exist, `mcphost` generates it.

#### Example (`mcp.json`):

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "/tmp/foo.db"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    }
  }
}
```

**Windows Note:** Use double backslashes (`\\`) in paths.

---

### System Prompt Configuration

Example JSON:

```json
{
  "systemPrompt": "You're a cat. Name is Neko"
}
```

Run with:

```bash
mcphost --system-prompt ./my-system-prompt.json
```

---

## 🌦️ Weather Server Setup (Example)

Create a weather server (`weather.py`) that exposes:

* `get_forecast`
* `get_alerts`

Update `mcp.json` to include:

```json
{
  "mcpServers": {
    "weather": {
      "command": "C:\\Users\\User\\anaconda3\\Scripts\\uv.exe",
      "args": [
        "--directory",
        "C:/Users/User/Downloads/mcp-ollama/mcp-ollama-agent",
        "run",
        "weather.py"
      ]
    }
  }
}
```

**Reminder:** Ensure the model is pulled via:

```bash
ollama pull qwen2.5:3b
```

Launch:

```bash
mcphost -m ollama:qwen2.5:3b --config mcp.json
```

---

## 🔍 MCP Inspector (Debugging Tool)

To verify MCP server functionality:

```bash
mcp dev weather.py
```

1. Accept prompt to install Inspector (if needed)
2. Open the browser URL provided
3. Click **Connect**
4. Explore tabs: **Tools**, **Resources**, etc.
5. Test each tool with input parameters and click `Run Tool`

Use this to validate the server before publishing to PyPI or elsewhere.