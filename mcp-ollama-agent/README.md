# MCP Ollama Agent

# Background
## MCP
MCP (Connector between local agent and external tools) basically offers the following:
1. `@mcp.resource()` - Similar to GET request and is used to provide information to the model
2. `@mcp.tool()` - Similar to POST request, and specifies available tools availale for the model to use
3. `@mcp.prompt()` - Used to templatize prompts

There is not a need for frameworks like Agent2Agent (A2A) and Model Context Protocol (MCP) in a use case where the local LLM is not interacting with external agents and tools respectively. 

In the MCP intialization step the MCP client tells the server what all features it can handle, whereas the server provides the information about tools, resources and prompts it has to offer. Once the initialization is done, all the message exchanges are done via the JSON-RPC format (structured text message), and these messages are travelling through stdio for local MCP server and via Streamable HTTP (using Server Side Events) for external MCP servers.     


## Ollama
Ollama is an open source platform allowing users to run, create and share their LLMs locally.

To install Ollama refer to their [official installation page](https://ollama.com/download/windows). 

Ollama is a CLI based service, so after the setup and installation is complete, we can start the ollama using `ollama serve`. 

**NOTE: Restart your VS Code after installation of Ollama**

You can check out different models it has to offer [here](https://ollama.com/search) (remember to filter the models that support tools in order to make this work correctly), and run any of them using the following command:
```python
ollama run <model-name>
```

Few useful commands:
1. `ollama` -> lists all the possible commands
2. `ollama list` -> gives a list of all the downloaded models
3. `ollama pull <model-name>` -> install the model
4. `ollama run <model-name>` -> runs the model locally (if the model is not installed, then the pull command is run automatically) 


Sometimes Ollama works fine with cmd, but has some issues with VS Code -> it is because the PATH variables are not set correctly. We can resolve this by executing the following steps: 
1. Open Command Prompt
2. `where ollama` -> checks the position where ollama is installed. Copy the full installation path to the ollama executable
3. Open VS Code
4. `echo %PATH%` - Check if the Ollama path is present here or not. 
5. If the ollama is present there, then try restarting the VS Code/ all the terminals open
6. Incase ollama is not present, then we need to add it to the PATH via the Environment Variables in both User and System variables. Now restat your VS Code.

Confirm that Ollama is running by visiting `http://localhost:11434/` -> should show `Ollama is running`. 

## `uv` Crash Course
uv is a Python package manager that promises to replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more.

`uv` is - *An extremely fast Python package and project manager, written in Rust.*

**Installation** <br>
`pip install uv`

**Initializing a new project** <br>
`uv init <project-name>`


```
$ cd <project-name>
$ tree -a
.
├── .gitignore
├── .python-version
├── README.md
├── hello.py
└── pyproject.toml
```

**Adding dependencies** <br>
`uv add scikit-learn xgboost`

**Remove dependencies** <br>
`uv remove scikit-learn`

**Running Python scripts in uv** <br>
`uv run hello.py`

**Create a virtual environment** <br>
`uv venv`

A more detailed explanation of uv can be found [here](https://www.datacamp.com/tutorial/python-uv).

# Prereuisites
In order to connect our local LLMs (from Ollama) to external tools/agents we need to install [mcphost](https://github.com/mark3labs/mcphost). 

We need `uvx` to launch Python based MCP servers locally.

## MCP Host
To successfully install mcphost on the system follow the below steps
1. Install [Go](https://go.dev/doc/install)
2. Open Command Prompt and run `go install github.com/mark3labs/mcphost@latest`

## Setup
After installing `mcphost`, `ollama` and `uv` on your system we can start with the project setup.

1. `uv init mcp-ollama-agent`
2. `cd mcp-ollama-agent`
3. `uv venv`
4. `source .venv/Scripts/activate`
5. `uv add mcp[cli] httpx`
 
# Ollama + MCPHost Config Setup
By default `mcphost` uses `anthropic:claude-3-5-sonnet-latest` as the default model and therefore it expects an Anthropic API Key to be specified in the environment variables or in the flags. 

Use Ollama with Qwen model - `mcphost -m ollama:qwen2.5:3b`

There are a ton of flag options available but the main ones relevant for us are:
1. `--config` string: Config file location (default is $HOME/.mcp.json)
2. `--system-prompt` string: system-prompt file location
3. `--debug`: Enable debug logging
4. `--message-window` int: Number of messages to keep in context (default: 10)
5. `-m`, `--model` string: Model to use (format: provider:model). For Ollama use `ollama:<model-name>`


While chatting, you can use:
1. `/help`: Show available commands
2. `/tools`: List all available tools
3. `/servers`: List configured MCP servers
4. `/history`: Display conversation history
5. `/quit`: Exit the application
6. Ctrl+C: Exit at any time


## MCP Servers
MCPHost will automatically create a configuration file at ~/.mcp.json if it doesn't exist. You can also specify a custom location using the --config flag:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": [
        "mcp-server-sqlite",
        "--db-path",
        "/tmp/foo.db"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/tmp"
      ]
    }
  }
}
```

Each MCP server entry requires:
1. `command`: The command to run (e.g., `uvx`, `npx`)
2. `args`: Array of arguments for the command:
    - For SQLite server: mcp-server-sqlite with database path
    - For filesystem server: @modelcontextprotocol/server-filesystem with directory path

**NOTE: In Windows all the paths should have double backward slash (\\\\).** 

## System Prompt
You can specify a custom system prompt using the `--system-prompt` flag. The system prompt should be a JSON file containing the instructions and context you want to provide to the model. For example:
```json
{
    "systemPrompt": "You're a cat. Name is Neko"
}
```

Usage:
`mcphost --system-prompt ./my-system-prompt.json`



## Weather Server Setup 
We will now create a server that offers 2 tools -> `get_forecast` and `get_alerts`. We can see the implementation in `weaher.py`, they are basically getting data from a weather API and then just formatting it. 

Once we are done with this, we need to add this to the MCP Sevrer config `mcp.json`. 

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
We have already explained about the JSON file before.

NOTE: Before we use mcphost, be sure to have pulled the ollama model that you want to use. 

Now let's see the magic by running: <br> 
`mcphost -m ollama:qwen2.5:3b --config mcp.json`

## MCP Inspector
MCP Inspector is the tool that is used during debuging to check whether our MCP server are working fine.

TO open the inspector, just execute the followin command in the terminal: <br>
`mcp dev <path-to-server-file>`

In our case it is <br>
`mcp dev weather.py`

This command will ask you to install MCP Inspector package if it is not already installed. Once you install it, then open the link displayed on your screen. 

At the start the server is not connector with the inspector and you will see below the `Connect` button, in grey it says Disconnected. So in order to conenct to the server, click on this button. 

On the top navigation bar, you will see a lot of options such as resources, tools, etc. Lets click on tools and then press on List tools, to get the list of available tools in the server. 

There you can choose any of the tools, and once you fill in the required parameters present on the right, and click on `Run Tool`, you will see the results. 

You should always test the MCP Server before you push it to PyPI or any other package manager. 