"""The airscape integration."""

from __future__ import annotations

from dataclasses import dataclass
import logging

import airscape as whf

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.device_registry import DeviceInfo, format_mac
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AirscapeCoordinator

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.FAN,
    Platform.SENSOR,
]


@dataclass
class AirscapeData:
    """AirScape Data Class."""

type AirscapeConfigEntry = ConfigEntry[AirscapeData]  # noqa: F821


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: AirscapeConfigEntry) -> bool:
    """Set up airscape from a config entry."""
    try:
        device = await hass.async_add_executor_job(whf.Fan, entry.data[CONF_HOST])
    except (whf.exceptions.ConnectionError, whf.exceptions.Timeout) as err:
        raise ConfigEntryNotReady from err
    dataCoordinator = AirscapeCoordinator(hass, device)
    await dataCoordinator.async_config_entry_first_refresh()
    entry.runtime_data = dataCoordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: AirscapeConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: AirscapeConfigEntry) -> None:
    """Handle an options update."""
    await hass.config_entries.async_reload(entry.entry_id)


class AirscapeDeviceEntity(CoordinatorEntity[AirscapeCoordinator]):
    """Define an Airscape device entity."""

    _attr_has_entity_name = True

    def __init__(
        self, entry: ConfigEntry, entity_description, enabled_default: bool = True
    ) -> None:
        """Initialize the Airscape Entity."""
        self._entry_id = entry.entry_id
        self._attr_enabled_default = enabled_default
        self._coordinator = entry.runtime_data
        self._attr_device_info = DeviceInfo(
            configuration_url=f"http://{self._coordinator.data.get('ipaddr')}",
            identifiers={(DOMAIN, format_mac(self._coordinator.data.get("macaddr")))},
            name=f"AirScape {self._coordinator.data['model']}",
            manufacturer="AirScape",
            model=self._coordinator.data["model"],
            sw_version=self._coordinator.data["softver"],
            connections={(DOMAIN, entry.entry_id)},
        )
        self.entity_description = entity_description
        self._name = entity_description.name
        self._type = entity_description.key
        self._attr_unique_id = (
            f"{format_mac(entry.runtime_data.data.get("macaddr"))}_{self._type}"
        )
        super().__init__(self._coordinator)

    @property
    def device_info(self) -> DeviceInfo:
        """Retrun device information."""
        return self._attr_device_info
