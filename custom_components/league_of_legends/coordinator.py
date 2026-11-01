"""Fetch one match history for all sensors."""
from datetime import timedelta
import logging

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RiotAuthError, RiotError
from .model import parse_match


class LeagueCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry, client):
        super().__init__(
            hass, logging.getLogger(__name__), name=f"League of Legends {entry.title}",
            config_entry=entry, update_interval=timedelta(minutes=5),
        )
        self.client = client
        self.puuid = entry.data["puuid"]

    async def _async_update_data(self):
        try:
            match_id = await self.client.latest_match_id(self.puuid)
            if match_id is None:
                return {}
            if self.data and self.data.get("match_id") == match_id:
                return self.data
            return parse_match(await self.client.match(match_id), self.puuid)
        except RiotAuthError as err:
            raise ConfigEntryAuthFailed("Riot API key rejected") from err
        except (RiotError, KeyError, ValueError, TypeError, StopIteration) as err:
            raise UpdateFailed("Cannot retrieve latest Riot match") from err
