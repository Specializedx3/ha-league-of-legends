"""Sensors describing the latest completed match."""
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

DESCRIPTIONS = (
    SensorEntityDescription(key="result", translation_key="result", device_class=SensorDeviceClass.ENUM, options=["win", "loss"], icon="mdi:trophy"),
    SensorEntityDescription(key="champion", name="Champion", icon="mdi:account"),
    SensorEntityDescription(key="kills", name="Kills", icon="mdi:sword"),
    SensorEntityDescription(key="deaths", name="Deaths", icon="mdi:skull"),
    SensorEntityDescription(key="assists", name="Assists", icon="mdi:handshake"),
    SensorEntityDescription(key="kda", name="KDA", icon="mdi:chart-line"),
    SensorEntityDescription(key="cs", name="CS", icon="mdi:counter"),
    SensorEntityDescription(key="gold", name="Gold", icon="mdi:gold"),
    SensorEntityDescription(key="damage", name="Champion damage", icon="mdi:sword-cross"),
    SensorEntityDescription(key="vision_score", name="Vision score", icon="mdi:eye"),
    SensorEntityDescription(key="duration", name="Game duration", device_class=SensorDeviceClass.DURATION, native_unit_of_measurement="s"),
    SensorEntityDescription(key="ended_at", name="Game ended", device_class=SensorDeviceClass.TIMESTAMP),
)


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities(LeagueSensor(entry.runtime_data, entry, description) for description in DESCRIPTIONS)


class LeagueSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, description):
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.data['puuid']}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data["puuid"])},
            name=entry.title, manufacturer="Riot Games", model="League of Legends",
        )

    @property
    def native_value(self):
        return (self.coordinator.data or {}).get(self.entity_description.key)

    @property
    def extra_state_attributes(self):
        if self.entity_description.key != "result":
            return None
        data = self.coordinator.data or {}
        return {key: data.get(key) for key in ("match_id", "queue_id", "game_mode", "position")}
