#  __init__.py
#
#  Copyright (c) 2025 Junpei Kawamoto
#
#  This software is released under the MIT License.
#
#  http://opensource.org/licenses/mit-license.php

from logging import Logger
from typing import Final
from urllib.parse import urlparse, parse_qs

import click
from mcp.server import FastMCP
from mcp.server.fastmcp.utilities import logging
from pydantic import Field
from youtube_transcript_api import YouTubeTranscriptApi

logger: Final[Logger] = logging.get_logger(__name__)


def server() -> FastMCP:
    """Initializes the MCP server."""

    mcp = FastMCP("Youtube Transcript")
    ytt_api = YouTubeTranscriptApi()

    @mcp.tool()
    def get_transcript(
        url: str = Field(description="The URL of the YouTube video"),
        lang: str = Field(description="The preferred language for the transcript", default="en"),
    ) -> str:
        """Retrieves the transcript of a YouTube video."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        video_id = query_params.get("v", [None])[0]
        if video_id is None:
            raise ValueError(f"couldn't find a video ID from the provided URL: {url}.")

        if lang == "en":
            languages = ["en"]
        else:
            languages = [lang, "en"]
        transcripts = ytt_api.fetch(video_id, languages=languages)

        return "\n".join((item.text for item in transcripts))

    return mcp


@click.command()
@click.version_option()
def main() -> None:
    """YouTube Transcript MCP server."""

    logger.info("starting Youtube Transcript MCP server")
    mcp = server()
    mcp.run()
    logger.info("closed Youtube Transcript MCP server")


__all__: Final = ["main"]
