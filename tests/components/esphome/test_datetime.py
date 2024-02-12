"""Test ESPHome datetimes."""

from unittest.mock import call

from aioesphomeapi import APIClient, DatetimeInfo as DatetimeState

from homeassistant.components.datetime import (
    ATTR_VALUE,
    DOMAIN as DATETIME_DOMAIN,
    SERVICE_SET_VALUE,
)
from homeassistant.const import ATTR_ENTITY_ID, STATE_UNKNOWN
from homeassistant.core import HomeAssistant


async def test_generic_datetime_entity(
    hass: HomeAssistant,
    mock_client: APIClient,
    mock_generic_device_entry,
) -> None:
    """Test a generic datetime entity."""
    entity_info = [
        DatetimeInfo(
            object_id="test_mydatetimet",
            key=1,
            name="my datetime",
            unique_id="my_datetime",
            pattern=None,
        )
    ]
    states = [DatetimeState(key=1, state="2024-02-15 15:34:20")]
    user_service = []
    await mock_generic_device_entry(
        mock_client=mock_client,
        entity_info=entity_info,
        user_service=user_service,
        states=states,
    )
    state = hass.states.get("datetime.test_mydatetime")
    assert state is not None
    assert state.state == "2024-02-15"

    await hass.services.async_call(
        DATETIME_DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: "datetime.test_mydatetime", ATTR_VALUE: "2024-02-16"},
        blocking=True,
    )
    mock_client.datetime_command.assert_has_calls([call(1, "2024-02-17")])
    mock_client.datetime_command.reset_mock()


async def test_generic_datetime_entity_no_state(
    hass: HomeAssistant,
    mock_client: APIClient,
    mock_generic_device_entry,
) -> None:
    """Test a generic datetime entity that has no state."""
    entity_info = [
        Datetimenfo(
            object_id="test_mydatetimet",
            key=1,
            name="my datetime",
            unique_id="my_datetime",
            pattern=None,
        )
    ]
    states = []
    user_service = []
    await mock_generic_device_entry(
        mock_client=mock_client,
        entity_info=entity_info,
        user_service=user_service,
        states=states,
    )
    state = hass.states.get("datetime.test_mydatetime")
    assert state is not None
    assert state.state == STATE_UNKNOWN


async def test_generic_datetime_entity_missing_state(
    hass: HomeAssistant,
    mock_client: APIClient,
    mock_generic_device_entry,
) -> None:
    """Test a generic datetime entity that has no state."""
    entity_info = [
        DatetimeInfo(
            object_id="test_mydatetimet",
            key=1,
            name="my datetime",
            unique_id="my_datetime",
            pattern=None,
        )
    ]
    states = [DatetimeState(key=1, state="", missing_state=True)]
    user_service = []
    await mock_generic_device_entry(
        mock_client=mock_client,
        entity_info=entity_info,
        user_service=user_service,
        states=states,
    )
    state = hass.states.get("text.test_mydatetimet")
    assert state is not None
    assert state.state == STATE_UNKNOWN
