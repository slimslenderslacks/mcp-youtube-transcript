# Youtube Transcript MCP Server
[![Python Application](https://github.com/jkawamoto/mcp-youtube-transcript/actions/workflows/python-app.yaml/badge.svg)](https://github.com/jkawamoto/mcp-youtube-transcript/actions/workflows/python-app.yaml)
[![GitHub License](https://img.shields.io/github/license/jkawamoto/mcp-youtube-transcript)](https://github.com/jkawamoto/mcp-youtube-transcript/blob/main/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![smithery badge](https://smithery.ai/badge/@jkawamoto/mcp-youtube-transcript)](https://smithery.ai/server/@jkawamoto/mcp-youtube-transcript)

This MCP server retrieves transcripts for given YouTube video URLs.

<a href="https://glama.ai/mcp/servers/of3kwtmlqp"><img width="380" height="200" src="https://glama.ai/mcp/servers/of3kwtmlqp/badge" alt="YouTube Transcript Server MCP server" /></a>

## Installation

### For Goose CLI
To enable the YouTube Transcript extension in Goose CLI,
edit the configuration file `~/.config/goose/config.yaml` to include the following entry:

```yaml
extensions:
  youtube-transcript:
    name: Youtube Transcript
    cmd: uvx
    args: [--from, git+https://github.com/jkawamoto/mcp-youtube-transcript, mcp-youtube-transcript]
    enabled: true
    type: stdio
```

### For Goose Desktop
Add a new extension with the following settings:

- **Type**: Standard IO
- **ID**: youtube-transcript
- **Name**: Youtube Transcript
- **Description**: Retrieve transcripts of YouTube videos
- **Command**: `uvx --from git+https://github.com/jkawamoto/mcp-youtube-transcript mcp-youtube-transcript`

For more details on configuring MCP servers in Goose Desktop,
refer to the documentation:
[Using Extensions - MCP Servers](https://block.github.io/goose/docs/getting-started/using-extensions#mcp-servers).

### For Claude Desktop
To configure this server for Claude Desktop, edit the `claude_desktop_config.json` file with the following entry under
`mcpServers`:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/jkawamoto/mcp-youtube-transcript",
        "mcp-youtube-transcript"
      ]
    }
  }
}
```
After editing, restart the application.
For more information,
see: [For Claude Desktop Users - Model Context Protocol](https://modelcontextprotocol.io/quickstart/user).

### Installing via Smithery
To install Youtube Transcript for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@jkawamoto/mcp-youtube-transcript):

```bash
npx -y @smithery/cli install @jkawamoto/mcp-youtube-transcript --client claude
```

## Tools
This MCP server provides the following tools:

### `get_transcript`
Fetches the transcript of a specified YouTube video.

#### Parameters
- **url** *(string)*: The full URL of the YouTube video. This field is required.
- **lang** *(string, optional)*: The desired language for the transcript. Defaults to `en` if not specified.

## License

This application is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
