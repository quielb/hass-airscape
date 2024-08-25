"""DataCoordinator for the Airscape integration."""

from __future__ import annotations

from datetime import timedelta
import logging

import airscape as whf

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


class AirscapeCoordinator(DataUpdateCoordinator):
    """Airscape Update Coordinator."""

    fan_api = None

    def __init__(self, hass: HomeAssistant, fan_api) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Airscpae API",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=5),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True,
        )
        self.fan_api = fan_api

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            # async with async_timeout.timeout(10):
            # Grab active context variables to limit data requir
            # ed to be fetched from API
            # Note: using context is not required if there is no need or ability to limit
            # data retrieved from API.
            #    listening_idx = set(self.async_contexts())
            return await self.hass.async_add_executor_job(self.fan_api.get_device_state)
        except (whf.exceptions.ConnectionError, whf.exceptions.Timeout) as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
