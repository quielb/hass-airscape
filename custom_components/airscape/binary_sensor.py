"""Platform for AirScpae Fan Binary Sensor."""

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AirscapeDeviceEntity
from .const import BINARYSENSOR_ENTITY

_LOGGER = logging.getLogger(__name__)
PLATFORM = "binary_sensor"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Handle creation of entity."""

    buttons = [
        AirscapeBinarySensor(config_entry, BINARYSENSOR_ENTITY[binary_sensor])
        for binary_sensor in BINARYSENSOR_ENTITY
    ]
    async_add_entities(buttons, False)


class AirscapeBinarySensor(BinarySensorEntity, AirscapeDeviceEntity):
    """Implementation of Airscape Whole House Fan Sensor."""

    def __init__(
        self, entry: ConfigEntry, entity_description: BinarySensorEntityDescription
    ) -> None:
        """Initilize an AirScape Binary Sensor."""
        super().__init__(entry, entity_description)

    @property
    def is_on(self) -> bool:
        """Return the statof of the Damper Doors."""
        return bool(self._coordinator.data["doorinprocess"])
