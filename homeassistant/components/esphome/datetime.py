"""Support for esphome datetimes."""
from __future__ import annotations

from aioesphomeapi import EntityInfo, DatetimeInfo, DatetimeState

from homeassistant.components.datetime import DateTimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import EsphomeEntity, esphome_state_property, platform_async_setup_entry
from datetime import UTC, datetime, timedelta


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up esphome datetime based on a config entry."""
    await platform_async_setup_entry(
        hass,
        entry,
        async_add_entities,
        info_type=DatetimeInfo,
        entity_type=DateTimeEntity,
        state_type=DatetimeState,
    )

class EsphomeDatetime(EsphomeEntity[DatetimeInfo, DatetimeState], DateTimeEntity):
    """A datetime implementation for esphome."""

    @callback
    def _on_static_info_update(self, static_info: EntityInfo) -> None:
        """Set attrs from static info."""
        super()._on_static_info_update(static_info)
        static_info = self._static_info
        self._attr_pattern = static_info.pattern

    @property
    @esphome_state_property
    def native_value(self) -> datetime | None:
        """Return the state of the entity."""
        state = self._state
        if state.missing_state:
            return None
        state = datetime.strptime(state._state, "%Y-%m-%d %H:%M:%S")

        return state

    async def async_set_value(self, value: datetime) -> None:
        """Update the current value."""
        await self._client.datetime_command(self._key, value.strftime("%Y-%m-%d %H:%M:%S"))
