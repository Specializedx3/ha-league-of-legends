"""Set up and reauthenticate via the Home Assistant UI."""
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import RiotAuthError, RiotClient, RiotError, RiotNotFound
from .const import DOMAIN, REGIONS

KEY_SELECTOR = selector.TextSelector(selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD))


class LeagueConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            data = {k: v.strip() for k, v in user_input.items()}
            if not all(data.values()):
                errors["base"] = "invalid_input"
            else:
                client = RiotClient(async_get_clientsession(self.hass), data["api_key"], data["region"])
                try:
                    account = await client.account(data["game_name"], data["tag_line"])
                except RiotAuthError:
                    errors["base"] = "invalid_auth"
                except RiotNotFound:
                    errors["base"] = "account_not_found"
                except RiotError:
                    errors["base"] = "cannot_connect"
                else:
                    await self.async_set_unique_id(account["puuid"])
                    self._abort_if_unique_id_configured()
                    data["puuid"] = account["puuid"]
                    return self.async_create_entry(title=f"{data['game_name']}#{data['tag_line']}", data=data)
        return self.async_show_form(step_id="user", data_schema=vol.Schema({
            vol.Required("game_name"): str,
            vol.Required("tag_line"): str,
            vol.Required("region", default="europe"): vol.In(REGIONS),
            vol.Required("api_key"): KEY_SELECTOR,
        }), errors=errors)

    async def async_step_reauth(self, entry_data):
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        errors = {}
        entry = self._get_reauth_entry()
        if user_input is not None:
            key = user_input["api_key"].strip()
            client = RiotClient(async_get_clientsession(self.hass), key, entry.data["region"])
            try:
                # Validate the key against the stable PUUID even after a Riot-ID rename.
                await client.get(f"/riot/account/v1/accounts/by-puuid/{entry.data['puuid']}")
            except RiotAuthError:
                errors["base"] = "invalid_auth"
            except RiotError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_update_reload_and_abort(entry, data_updates={"api_key": key})
        return self.async_show_form(step_id="reauth_confirm", data_schema=vol.Schema({
            vol.Required("api_key"): KEY_SELECTOR,
        }), errors=errors)
