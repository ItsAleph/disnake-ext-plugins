import pytest

from disnake.ext import plugins

def test_basic():
    plugin = plugins.Plugin("test")

    assert plugin.name == "test"
    assert str(plugin) == plugin.name == "test"
    assert repr(plugin) == f"<Plugin name='{plugin.name}'>" == "<Plugin name='test'>"

    with pytest.raises(ValueError):
        plugin1 = plugins.Plugin("existing_plugin")
        plugin2 = plugins.Plugin("existing_plugin")

def test_state():
    empty_plugin = plugins.Plugin("empty_plugin")
    assert not empty_plugin.state
    assert empty_plugin.state == {}

    valid_plugin = plugins.Plugin("valid_plugin", state_key="state_value")
    assert valid_plugin.state
    assert valid_plugin.state.get("state_key")
    assert valid_plugin.state['state_key'] == "state_value"
