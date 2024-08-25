"""Platform for AirScape Fan Sensors."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AirscapeDeviceEntity
from .const import SENSOR_ENTITY

_LOGGER = logging.getLogger(__name__)
PLATFORM = "sensor"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Handle creation of entity."""

    sensors = [
        AirscapeSensor(config_entry, SENSOR_ENTITY[sensor]) for sensor in SENSOR_ENTITY
    ]
    # for sensor in SENOR_ENTITY:
    #    sensors.append([AirscapeSensor(config_entry, SENOR_ENTITY[sensor])])
    async_add_entities(sensors, False)


class AirscapeSensor(SensorEntity, AirscapeDeviceEntity):
    """Implementation of Airscape Whole House Fan Sensor."""

    def __init__(
        self, entry: ConfigEntry, entity_description: SensorEntityDescription
    ) -> None:
        """Initilize an AirScape sensor."""
        super().__init__(entry, entity_description)

    @property
    def native_value(self) -> Any:
        """Return value of sensor."""
        return self._coordinator.data[self._type]
