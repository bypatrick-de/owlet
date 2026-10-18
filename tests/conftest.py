"""Fixtures for testing the custom Owlet integration."""
import pytest

@pytest.fixture(autouse=True)
def enable_custom_integration(enable_custom_integrations):
    """Load the integration from custom_components."""
    yield
