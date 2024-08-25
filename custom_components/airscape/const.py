"""Constants for the airscape integration."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.components.button import ButtonEntityDescription
from homeassistant.components.fan import FanEntityDescription
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower, UnitOfTemperature, UnitOfTime

DOMAIN = "airscape"

# Default Values
DEFAULT_MINIMUM_SPEED = 1
DEFAULT_TIMEOUT = 5

# Configuration Constants
CONF_MINIMUM_SPEED = "minimum_speed"


# Services
SERVICES_FAN: dict[str, str] = {
    "speed_up": "speed_up",
    "slow_down": "slow_down",
    "turn_on_to_minimum": "turn_on_to_minimum",
}

BINARYSENSOR_ENTITY: dict[str, BinarySensorEntityDescription] = {
    "door": BinarySensorEntityDescription(
        key="doorinprocess",
        name="Door Moving",
        device_class=BinarySensorDeviceClass.MOVING,
        icon="mdi:hvac",
        entity_registry_enabled_default=False,
    )
}

BUTTON_ENTITY: dict[str, ButtonEntityDescription] = {
    "add_time": ButtonEntityDescription(
        key="add_time",
        name="Add Time",
        icon="mdi:timer-plus-outline",
    )
}

FAN_ENTITY: dict[str, FanEntityDescription] = {
    "fan": FanEntityDescription(
        key="fan",
        name=f"Fan",
    )
}

SENSOR_ENTITY: dict[str, SensorEntityDescription] = {
    "attic": SensorEntityDescription(
        key="attic",
        name="Attic Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "cfm": SensorEntityDescription(
        key="cfm",
        name="CFM",
        device_class=None,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fan",
    ),
    "power": SensorEntityDescription(
        key="power",
        name="Power Usage",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    "timeremaining": SensorEntityDescription(
        key="timeremaining",
        name="Timer",
        device_class=None,
        native_unit_of_measurement=UnitOfTime.MINUTES,
        icon="mdi:fan-clock",
    ),
    "inside": SensorEntityDescription(
        key="inside",
        name="Inside Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    "outside": SensorEntityDescription(
        key="oa",
        name="Outside Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
}
