"""Platform for AirScape Fan Button."""

import logging

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AirscapeDeviceEntity
from .const import BUTTON_ENTITY

_LOGGER = logging.getLogger(__name__)
PLATFORM = "button"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Handle creation of entity."""

    buttons = [
        AirscapeButton(config_entry, BUTTON_ENTITY[button]) for button in BUTTON_ENTITY
    ]
    async_add_entities(buttons, False)


class AirscapeButton(ButtonEntity, AirscapeDeviceEntity):
    """Implementation of Airscape Whole House Fan Sensor."""

    def __init__(
        self, entry: ConfigEntry, entity_description: ButtonEntityDescription
    ) -> None:
        """Initilize an AirScape button."""
        super().__init__(entry, entity_description)

    def press(self) -> None:
        """Press the button."""
        if bool(self._coordinator.data["fanspd"]):
            self._coordinator.fan_api.add_time()
