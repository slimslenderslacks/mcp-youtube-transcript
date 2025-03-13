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
from youtube_transcript_api.proxies import WebshareProxyConfig, GenericProxyConfig, ProxyConfig


def server(
    webshare_proxy_username: str | None,
    webshare_proxy_password: str | None,
    http_proxy: str | None,
    https_proxy: str | None,
) -> FastMCP:
    """Initializes the MCP server."""

    proxy_config: ProxyConfig | None = None
    if webshare_proxy_username and webshare_proxy_password:
        proxy_config = WebshareProxyConfig(webshare_proxy_username, webshare_proxy_password)
    elif http_proxy or https_proxy:
        proxy_config = GenericProxyConfig(http_proxy, https_proxy)

    ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)

    mcp = FastMCP("Youtube Transcript")

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
@click.option(
    "--webshare-proxy-username",
    metavar="NAME",
    envvar="WEBSHARE_PROXY_USERNAME",
    help="Webshare proxy service username.",
)
@click.option(
    "--webshare-proxy-password",
    metavar="PASSWORD",
    envvar="WEBSHARE_PROXY_PASSWORD",
    help="Webshare proxy service password.",
)
@click.option("--http-proxy", metavar="URL", envvar="HTTP_PROXY", help="HTTP proxy server URL.")
@click.option("--https-proxy", metavar="URL", envvar="HTTPS_PROXY", help="HTTPS proxy server URL.")
@click.version_option()
def main(
    webshare_proxy_username: str | None,
    webshare_proxy_password: str | None,
    http_proxy: str | None,
    https_proxy: str | None,
) -> None:
    """YouTube Transcript MCP server."""

    logger: Final[Logger] = logging.get_logger(__name__)

    logger.info("starting Youtube Transcript MCP server")
    mcp = server(webshare_proxy_username, webshare_proxy_password, http_proxy, https_proxy)
    mcp.run()
    logger.info("closed Youtube Transcript MCP server")


__all__: Final = ["main"]
