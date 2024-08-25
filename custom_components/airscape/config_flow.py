"""Config flow for airscape integration."""

from __future__ import annotations

import logging
from typing import Any

import airscape as whf
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import selector
from homeassistant.helpers.device_registry import format_mac

from .const import CONF_MINIMUM_SPEED, DEFAULT_MINIMUM_SPEED, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    try:
        whfConnection = await hass.async_add_executor_job(whf.Fan, data[CONF_HOST])
    except (whf.exceptions.ConnectionError, whf.exceptions.Timeout) as err:
        raise CannotConnect from err
    else:
        data = await hass.async_add_executor_job(whfConnection.get_device_state)
        # Return info that you want to store in the config entry.
        return {
            "title": f"Airscape {data['model']}",
            "unique_id": f"{format_mac(data['macaddr'])}",
        }


class AirscapeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for airscape."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=info["title"], data=user_input, options={"minimum_speed": 1}
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(OptionsFlow):
    """Options flow handler."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_MINIMUM_SPEED,
                        default=self.config_entry.options.get(CONF_MINIMUM_SPEED, DEFAULT_MINIMUM_SPEED)
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1, max=10, mode=selector.NumberSelectorMode.BOX
                        )
                    )
                }
            ),
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
