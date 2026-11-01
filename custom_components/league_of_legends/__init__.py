"""League of Legends last-match integration."""
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import RiotClient
from .coordinator import LeagueCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass, entry):
    client = RiotClient(async_get_clientsession(hass), entry.data["api_key"], entry.data["region"])
    coordinator = LeagueCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
