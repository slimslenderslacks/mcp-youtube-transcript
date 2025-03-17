#  server.py
#
#  Copyright (c) 2025 Junpei Kawamoto
#
#  This software is released under the MIT License.
#
#  http://opensource.org/licenses/mit-license.php

from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from mcp.server import FastMCP
from pydantic import Field
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig, GenericProxyConfig, ProxyConfig


def new_server(
    webshare_proxy_username: str | None = None,
    webshare_proxy_password: str | None = None,
    http_proxy: str | None = None,
    https_proxy: str | None = None,
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

        if parsed_url.hostname == "youtu.be":
            video_id = parsed_url.path.lstrip("/")
        else:
            q = parse_qs(parsed_url.query).get("v")
            if q is None:
                raise ValueError(f"couldn't find a video ID from the provided URL: {url}.")
            video_id = q[0]

        if lang == "en":
            languages = ["en"]
        else:
            languages = [lang, "en"]

        page = requests.get(
            f"https://www.youtube.com/watch?v={video_id}", headers={"Accept-Language": ",".join(languages)}
        )
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "html.parser")
        title = soup.title.string if soup.title else ""

        transcripts = ytt_api.fetch(video_id, languages=languages)

        return f"# {title}\n" + "\n".join((item.text for item in transcripts))

    return mcp
