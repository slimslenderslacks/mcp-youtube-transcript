# Youtube Transcript MCP Server
[![Python Application](https://github.com/jkawamoto/mcp-youtube-transcript/actions/workflows/python-app.yaml/badge.svg)](https://github.com/jkawamoto/mcp-youtube-transcript/actions/workflows/python-app.yaml)
[![GitHub License](https://img.shields.io/github/license/jkawamoto/mcp-youtube-transcript)](https://github.com/jkawamoto/mcp-youtube-transcript/blob/main/LICENSE)

This MCP server retrieves transcripts for given YouTube video URLs.

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

## License

This application is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
