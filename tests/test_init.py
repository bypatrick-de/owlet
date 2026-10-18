"""Test Owlet init."""
from __future__ import annotations

from unittest.mock import patch

from pyowletapi.exceptions import (
    OwletAuthenticationError,
    OwletConnectionError,
    OwletDevicesError,
    OwletError,
)

from custom_components.owlet.const import (
    CONF_OWLET_EXPIRY,
    CONF_OWLET_REFRESH,
    DOMAIN,
)
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_API_TOKEN, CONF_REGION, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from . import async_init_integration

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def test_async_setup_entry(hass: HomeAssistant) -> None:
    """Test setting up entry."""
    entry = await async_init_integration(hass)

    assert entry.state == ConfigEntryState.LOADED

    device_registry = dr.async_get(hass)

    device_entry = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id, identifiers={(DOMAIN, "SERIAL_NUMBER")}
    )

    assert device_entry.name == "Owlet Sock SERIAL_NUMBER"

    entity_registry = er.async_get(hass)

    entities = er.async_entries_for_device(entity_registry, device_entry.id)

    assert len(entities) == 19

    await hass.config_entries.async_unload(entry.entry_id)

    assert entry.state == ConfigEntryState.NOT_LOADED


async def test_async_setup_entry_new_tokens(hass: HomeAssistant) -> None:
    """Test setting up entry and getting new tokens."""
    entry = await async_init_integration(
        hass, devices_fixture="get_devices_with_tokens.json"
    )

    assert entry.data == {
        CONF_REGION: "europe",
        CONF_USERNAME: "sample@gmail.com",
        CONF_API_TOKEN: "new_api_token",
        CONF_OWLET_EXPIRY: 200,
        CONF_OWLET_REFRESH: "new_refresh_token",
    }

    assert entry.state == ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)

    assert entry.state == ConfigEntryState.NOT_LOADED


async def test_async_setup_entry_auth_error(hass: HomeAssistant) -> None:
    """Test setting up entry with auth error."""
    entry = await async_init_integration(hass, skip_setup=True)

    with patch(
        "custom_components.owlet.OwletAPI.authenticate",
        side_effect=OwletAuthenticationError(),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        assert entry.state == ConfigEntryState.SETUP_ERROR

        await hass.config_entries.async_unload(entry.entry_id)


async def test_async_setup_entry_connection_error(hass: HomeAssistant) -> None:
    """Test setting up entry with connection error."""
    entry = await async_init_integration(hass, skip_setup=True)

    with patch(
        "custom_components.owlet.OwletAPI.authenticate",
        side_effect=OwletConnectionError(),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        assert entry.state == ConfigEntryState.SETUP_RETRY

        await hass.config_entries.async_unload(entry.entry_id)


async def test_async_setup_entry_devices_error(hass: HomeAssistant) -> None:
    """Test setting up entry with device error."""
    entry = await async_init_integration(hass, skip_setup=True)

    with patch(
        "custom_components.owlet.OwletAPI.authenticate", return_value=None
    ), patch(
        "custom_components.owlet.OwletAPI.get_devices",
        side_effect=OwletDevicesError(),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        assert entry.state == ConfigEntryState.SETUP_ERROR
        await hass.config_entries.async_unload(entry.entry_id)


async def test_async_setup_entry_error(hass: HomeAssistant) -> None:
    """Test setting up entry with unknown error."""
    entry = await async_init_integration(hass, skip_setup=True)

    with patch(
        "custom_components.owlet.OwletAPI.authenticate",
        side_effect=OwletError(),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        assert entry.state == ConfigEntryState.SETUP_ERROR

        await hass.config_entries.async_unload(entry.entry_id)


async def test_options_apply_without_reload(hass: HomeAssistant) -> None:
    """A saved interval updates every coordinator without an API login."""
    from datetime import timedelta
    from homeassistant.const import CONF_SCAN_INTERVAL

    entry = await async_init_integration(hass)
    coordinators = hass.data[DOMAIN][entry.entry_id]
    with patch("custom_components.owlet.OwletAPI.authenticate") as authenticate:
        hass.config_entries.async_update_entry(
            entry, options={CONF_SCAN_INTERVAL: 30}
        )
        await hass.async_block_till_done()
        assert all(c.update_interval == timedelta(seconds=30)
                   for c in coordinators.values())
        authenticate.assert_not_called()
    await hass.config_entries.async_unload(entry.entry_id)


async def test_setup_without_interval(hass: HomeAssistant) -> None:
    """Older entries with no options still load with the default interval."""
    from datetime import timedelta
    from . import load_fixture
    from .const import AUTH_RETURN
    from custom_components.owlet.const import POLLING_INTERVAL
    import json

    entry = await async_init_integration(hass, skip_setup=True)
    hass.config_entries.async_update_entry(entry, options={})
    with patch("custom_components.owlet.OwletAPI.authenticate", return_value=AUTH_RETURN), patch(
        "custom_components.owlet.OwletAPI.get_devices",
        return_value=json.loads(load_fixture("get_devices.json")),
    ), patch("custom_components.owlet.OwletAPI.get_properties",
             return_value=json.loads(load_fixture("update_properties_charging.json"))):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    assert all(c.update_interval == timedelta(seconds=POLLING_INTERVAL)
               for c in hass.data[DOMAIN][entry.entry_id].values())
    await hass.config_entries.async_unload(entry.entry_id)
