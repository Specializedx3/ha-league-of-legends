"""Small asynchronous Riot API client."""
import asyncio
from urllib.parse import quote

import aiohttp


class RiotError(Exception):
    """Riot API request failed."""


class RiotAuthError(RiotError):
    """API key is invalid or expired."""


class RiotNotFound(RiotError):
    """Account or match was not found."""


class RiotClient:
    def __init__(self, session, api_key, region):
        self.session = session
        self.api_key = api_key
        self.region = region
        self.retry_at = 0.0

    async def get(self, path, params=None):
        loop = asyncio.get_running_loop()
        if loop.time() < self.retry_at:
            raise RiotError("Riot rate limit: waiting for Retry-After")
        try:
            async with self.session.get(
                f"https://{self.region}.api.riotgames.com{path}",
                params=params,
                headers={"X-Riot-Token": self.api_key},
                timeout=aiohttp.ClientTimeout(total=20),
            ) as response:
                if response.status in (401, 403):
                    raise RiotAuthError("API key rejected")
                if response.status == 404:
                    raise RiotNotFound("Account or match not found")
                if response.status == 429:
                    try:
                        delay = max(1, float(response.headers.get("Retry-After", "120")))
                    except ValueError:
                        delay = 120
                    self.retry_at = loop.time() + delay
                    raise RiotError("Riot rate limit reached")
                if response.status != 200:
                    raise RiotError(f"Riot returned HTTP {response.status}")
                return await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            raise RiotError("Cannot connect to Riot API") from err

    async def account(self, game_name, tag_line):
        return await self.get(
            f"/riot/account/v1/accounts/by-riot-id/{quote(game_name, safe='')}/{quote(tag_line, safe='')}"
        )

    async def latest_match_id(self, puuid):
        matches = await self.get(
            f"/lol/match/v5/matches/by-puuid/{quote(puuid, safe='')}/ids",
            {"start": 0, "count": 1},
        )
        return matches[0] if matches else None

    async def match(self, match_id):
        return await self.get(f"/lol/match/v5/matches/{quote(match_id, safe='')}")
