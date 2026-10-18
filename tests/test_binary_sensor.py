"""Test Owlet Sensor."""
from __future__ import annotations

from homeassistant.core import HomeAssistant

from . import async_init_integration, get_state


async def test_sensors_asleep(hass: HomeAssistant) -> None:
    """Test sensor values."""
    await async_init_integration(
        hass, properties_fixture="update_properties_asleep.json"
    )

    assert len(hass.states.async_all("binary_sensor")) == 10

    assert get_state(hass, "binary_sensor", "charging").state == "off"
    assert (
        get_state(hass, "binary_sensor", "high_heart_rate_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "low_heart_rate_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "high_oxygen_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "low_oxygen_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "low_battery_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "lost_power_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "sock_disconnected_alert").state
        == "off"
    )
    assert get_state(hass, "binary_sensor", "sock_off").state == "off"
    assert get_state(hass, "binary_sensor", "awake").state == "off"


async def test_sensors_awake(hass: HomeAssistant) -> None:
    """Test sensor values."""
    await async_init_integration(
        hass, properties_fixture="update_properties_awake.json"
    )

    assert len(hass.states.async_all("binary_sensor")) == 10

    assert get_state(hass, "binary_sensor", "charging").state == "off"
    assert (
        get_state(hass, "binary_sensor", "high_heart_rate_alert").state
        == "on"
    )
    assert (
        get_state(hass, "binary_sensor", "low_heart_rate_alert").state
        == "on"
    )
    assert (
        get_state(hass, "binary_sensor", "high_oxygen_alert").state
        == "on"
    )
    assert (
        get_state(hass, "binary_sensor", "low_oxygen_alert").state
        == "on"
    )
    assert (
        get_state(hass, "binary_sensor", "low_battery_alert").state
        == "on"
    )
    assert (
        get_state(hass, "binary_sensor", "lost_power_alert").state
        == "on"
    )
    assert (
        get_state(hass, "binary_sensor", "sock_disconnected_alert").state
        == "off"
    )
    assert get_state(hass, "binary_sensor", "sock_off").state == "off"
    assert get_state(hass, "binary_sensor", "awake").state == "on"


async def test_sensors_charging(hass: HomeAssistant) -> None:
    """Test sensor values."""
    await async_init_integration(
        hass, properties_fixture="update_properties_charging.json"
    )

    assert len(hass.states.async_all("binary_sensor")) == 10

    assert get_state(hass, "binary_sensor", "charging").state == "on"
    assert (
        get_state(hass, "binary_sensor", "high_heart_rate_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "low_heart_rate_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "high_oxygen_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "low_oxygen_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "low_battery_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "lost_power_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "sock_disconnected_alert").state
        == "off"
    )
    assert get_state(hass, "binary_sensor", "sock_off").state == "off"
    assert (
        get_state(hass, "binary_sensor", "awake").state == "unavailable"
    )


async def test_sensors_v2(hass: HomeAssistant) -> None:
    """Test sensor values."""
    await async_init_integration(hass, properties_fixture="update_properties_v2.json")
    assert len(hass.states.async_all("binary_sensor")) == 9

    assert get_state(hass, "binary_sensor", "charging").state == "off"
    assert (
        get_state(hass, "binary_sensor", "high_heart_rate_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "low_heart_rate_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "low_oxygen_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "low_battery_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "critical_battery_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "critical_oxygen_alert").state
        == "off"
    )
    assert (
        get_state(hass, "binary_sensor", "sock_disconnected_alert").state
        == "off"
    )
    assert get_state(hass, "binary_sensor", "sock_off").state == "off"
