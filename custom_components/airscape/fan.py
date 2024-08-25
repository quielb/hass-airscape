"""Platform for AirScape Fan Integration."""

import logging
import math
from typing import Any

from homeassistant.components.fan import (
    FanEntity,
    FanEntityDescription,
    FanEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.percentage import (
    int_states_in_range,
    percentage_to_ranged_value,
    ranged_value_to_percentage,
)

from . import AirscapeDeviceEntity
from .const import DEFAULT_MINIMUM_SPEED, CONF_MINIMUM_SPEED, SERVICES_FAN, FAN_ENTITY

_LOGGER = logging.getLogger(__name__)
PLATFORM = "fan"
SPEED_RANGE = (1, 10)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Handle creation of entity."""

    platform = entity_platform.async_get_current_platform()

    for k, v in SERVICES_FAN.items():
        platform.async_register_entity_service(k, {}, v)

    fans = [AirscapeFan(config_entry, FAN_ENTITY[fan]) for fan in FAN_ENTITY]

    async_add_entities(fans, False)


class AirscapeFan(FanEntity, AirscapeDeviceEntity):
    """Implementation of Airscape Whole House Fan."""

    _attr_supported_features = (
        FanEntityFeature.TURN_ON
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.SET_SPEED
    )

    def __init__(
        self,
        entry: ConfigEntry,
        entity_description: FanEntityDescription,
        enabled_default: bool = True,
    ) -> None:
        """Initilize a Fan."""
        _LOGGER.debug(
            "Starting async_setup_entry for FAN platform with config_entry:\n%s",
            entry.as_dict(),
        )
        super().__init__(entry, entity_description)
        self._max_speed = self._coordinator.fan_api.max_speed
        self._minimum_speed = entry.options.get(CONF_MINIMUM_SPEED, DEFAULT_MINIMUM_SPEED)

    @property
    def is_on(self) -> bool:
        """Return state of fan."""
        self._coordinator.data["fanspd"]
        return bool(self._coordinator.data["fanspd"])

    def turn_on(
        self,
        speed: str | None = None,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Instruct the fan to turn on."""
        if self.available:
            if percentage is not None:
                self._coordinator.fan_api.speed = math.ceil(
                    percentage_to_ranged_value((1, self._max_speed), percentage)
                )
            else:
                self._coordinator.fan_api.speed = 1

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the fan to turn off."""
        if self.available:
            self._coordinator.fan_api.is_on = False

    @property
    def speed_count(self) -> int:
        """Return the number of speeds the fan supports."""
        return int_states_in_range((1, self._max_speed))

    @property
    def percentage(self) -> int:
        """Return the current speed percentage."""
        return ranged_value_to_percentage(
            (1, self._max_speed), self._coordinator.data.get("fanspd")
        )

    def set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan."""
        if self.available:
            if not bool(percentage):
                self._coordinator.fan_api.is_on = False
            else:
                self._coordinator.fan_api.speed = math.ceil(
                    percentage_to_ranged_value((1, self._max_speed), percentage)
                )

    def speed_up(self) -> None:
        """Instruct fan to increment speed up by 1."""
        if self.available:
            self._coordinator.fan_api.speed_up()

    def slow_down(self) -> None:
        """Instruct fan to increment speed down by 1 to minimum speed."""
        if (
            self.available
            and self._coordinator.data.get("fanspd") > self._minimum_speed
        ):
            self._coordinator.fan_api.slow_down()

    def turn_on_to_minimum(self) -> None:
        """Turn fan on and set to minimum speed defined."""
        if self.available:
            self._coordinator.fan_api.speed = self._minimum_speed
