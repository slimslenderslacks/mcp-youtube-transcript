#  server.py
#
#  Copyright (c) 2025 Junpei Kawamoto
#
#  This software is released under the MIT License.
#
#  http://opensource.org/licenses/mit-license.php
from contextlib import asynccontextmanager
from dataclasses import dataclass
from functools import lru_cache, partial
from typing import AsyncIterator
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from mcp.server import FastMCP
from mcp.server.fastmcp import Context
from pydantic import Field
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig, GenericProxyConfig, ProxyConfig


@dataclass(frozen=True)
class AppContext:
    http_client: requests.Session
    ytt_api: YouTubeTranscriptApi


@asynccontextmanager
async def _app_lifespan(_server: FastMCP, proxy_config: ProxyConfig | None) -> AsyncIterator[AppContext]:
    with requests.Session() as http_client:
        ytt_api = YouTubeTranscriptApi(http_client=http_client, proxy_config=proxy_config)
        yield AppContext(http_client=http_client, ytt_api=ytt_api)


@lru_cache
def _get_transcript(ctx: AppContext, video_id: str, lang: str) -> str:
    if lang == "en":
        languages = ["en"]
    else:
        languages = [lang, "en"]

    page = ctx.http_client.get(
        f"https://www.youtube.com/watch?v={video_id}", headers={"Accept-Language": ",".join(languages)}
    )
    page.raise_for_status()
    soup = BeautifulSoup(page.text, "html.parser")
    title = soup.title.string if soup.title else "Transcript"

    transcripts = ctx.ytt_api.fetch(video_id, languages=languages)

    return f"# {title}\n" + "\n".join((item.text for item in transcripts))


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

    mcp = FastMCP("Youtube Transcript", lifespan=partial(_app_lifespan, proxy_config=proxy_config))

    @mcp.tool()
    async def get_transcript(
        ctx: Context,
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

        app_ctx: AppContext = ctx.request_context.lifespan_context  # type: ignore
        return _get_transcript(app_ctx, video_id, lang)

    return mcp
