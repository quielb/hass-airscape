"""Platform for Airscape fan integration."""
import logging, math
import airscape
import voluptuous as vol

import homeassistant.helpers.config_validation as cv

# Import the device class from the component that you want to support
from homeassistant.components.fan import (
    SUPPORT_SET_SPEED,
    PLATFORM_SCHEMA,
    FanEntity,
    DOMAIN,
)

from homeassistant.const import CONF_HOST, CONF_NAME, CONF_TIMEOUT, CONF_MINIMUM, CONF_MAXIMUM

from homeassistant.util.percentage import (
    int_states_in_range,
    ranged_value_to_percentage,
    percentage_to_ranged_value,
)

from . import AIRSCAPE_DOMAIN
from .const import fan_to_hass_attr, DEFAULT_TIMEOUT, DEFAULT_MINIMUM


_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
        vol.Optional(CONF_MINIMUM, default=DEFAULT_MINIMUM): cv.positive_int,
        vol.Optional(CONF_MAXIMUM): cv.positive_int,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Airscape Fan platform."""
    # Setup connection to the fan
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    minimum = config.get(CONF_MINIMUM)    
    maximum = config.get(CONF_MAXIMUM)
    timeout = config.get(CONF_TIMEOUT)

    try:
        device = airscape.Fan(host, timeout)
        # use maximum reported by the airscape library is none specifed in the config
        maximum = maximum or device.max_speed
    except (airscape.exceptions.Timeout, airscape.exceptions.ConnectionError):
        _LOGGER.error(
            "Cannot connect to %s.  " "Device did not respond to API request", host
        )
    else:
        # Add devices
        add_entities([AirscapeWHF(device, name, minimum, maximum)], True)

    def service_speed_up(call):
        """Handle speed_up service call."""
        entity_id = call.data.get("entity_id")
        _LOGGER.debug("Calling speed_up for %s", entity_id)

        entity = hass.data[DOMAIN].get_entity(entity_id)
        entity.speed_up()

    def service_slow_down(call):
        """Handle slow_down service call."""
        entity_id = call.data.get("entity_id")
        _LOGGER.debug("Calling slow_down for %s", entity_id)

        entity = hass.data[DOMAIN].get_entity(entity_id)
        entity.slow_down()

    def service_add_time(call):
        """Handle slow_down service call."""
        entity_id = call.data.get("entity_id")
        _LOGGER.debug("Calling add_time for %s", entity_id)

        entity = hass.data[DOMAIN].get_entity(entity_id)
        entity.add_time()

    hass.services.register(AIRSCAPE_DOMAIN, "speed_up", service_speed_up)
    hass.services.register(AIRSCAPE_DOMAIN, "slow_down", service_slow_down)
    hass.services.register(AIRSCAPE_DOMAIN, "add_time", service_add_time)

    return True


class AirscapeWHF(FanEntity):
    """Representation of an Airscape Fan."""

    def __init__(self, device, name, minimum, maximum):
        """Initialize a AirscapeFan."""
        self._fan = device
        self._name = name
        self._state = None
        self._speed = None
        self._available = True
        self._minimum_speed = minimum
        self._maximum_speed = maximum
        self._attr = {}

    @property
    def name(self):
        """Return the display name of this fan."""
        return self._name

    @property
    def available(self):
        """Return if device is available."""
        return self._available

    @property
    def should_poll(self):
        """Instruct HA this device should be polled."""
        return True

    @property
    def supported_features(self):
        """Return supported features of fan."""
        return SUPPORT_SET_SPEED

    @property
    def device_state_attributes(self):
        return self._attr

    @property
    def is_on(self):
        """Return state of fan."""
        return self._state

    def turn_on(
        self,
        speed: str = None,
        percentage: int = None,
        preset_mode: str = None,
        **kwargs,
    ) -> None:
        """Instruct the fan to turn on."""
        try:
            if percentage is not None:
                self._fan.speed = math.ceil(
                    percentage_to_ranged_value(
                        (self._minimum_speed, self._maximum_speed), percentage
                    )
                )
            else:
                self._fan.speed = self._minimum_speed
        except (airscape.exceptions.ConnectionError, airscape.exceptions.Timeout):
            self._available = False

    def turn_off(self, **kwargs):
        """Instruct the fan to turn off."""
        try:
            self._fan.is_on = False
        except (airscape.exceptions.ConnectionError, airscape.exceptions.Timeout):
            self._available = False

    def add_time(self):
        """Add an hour to the shutoff timer."""
        try:
            self._fan.add_time()
        except (airscape.exceptions.ConnectionError, airscape.exceptions.Timeout):
            self._available = False

    @property
    def speed_count(self):
        """Return the number of speeds the fan supports."""
        return int_states_in_range((self._minimum_speed, self._maximum_speed))

    @property
    def percentage(self):
        """Return the current speed percentage"""
        return ranged_value_to_percentage(
            (self._minimum_speed, self._maximum_speed), self._speed
        )

    def set_percentage(self, percentage: int):
        """Set the speed of the fan."""
        if not bool(percentage):
            self._fan.is_on = False
        try:
            self._fan.speed = math.ceil(
                percentage_to_ranged_value(
                    (self._minimum_speed, self._maximum_speed), percentage
                )
            )
        except (airscape.exceptions.ConnectionError, airscape.exceptions.Timeout):
            self._available = False

    def speed_up(self):
        """Instruct fan to increment speed up by 1."""
        try:
            if self._speed < self._maximum_speed:
                self._fan.speed_up()
        except (airscape.exceptions.ConnectionError, airscape.exceptions.Timeout):
            self._available = False

    def slow_down(self):
        """Instruct fan to increment speed down by 1."""
        try:
            if self._speed > self._minimum_speed:
                self._fan.slow_down()
        except (airscape.exceptions.ConnectionError, airscape.exceptions.Timeout):
            self._available = False

    def update(self):
        """Fetch new state data for this fan.

        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            fan_data = self._fan.get_device_state()
        except (airscape.exceptions.ConnectionError, airscape.exceptions.Timeout):
            self._available = False
        else:
            self._state = bool(fan_data["fanspd"])
            self._speed = fan_data["fanspd"]
            self._available = True
            # self._attr = fan_data
            for k, v in fan_to_hass_attr.items():
                self._attr[v] = fan_data[k]
