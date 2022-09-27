# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio

from typing import Callable, TYPE_CHECKING, Any, Dict, Optional, Union, Sequence, List

if TYPE_CHECKING:
    from disnake.ext.commands.bot import (
        AutoShardedBot,
        AutoShardedInteractionBot,
        Bot,
        InteractionBot,
    )

    from disnake.app_commands import Option
    from disnake.i18n import LocalizedOptional
    from disnake.permissions import Permissions
    from disnake.ext.commands.base_core import CommandCallback

    AnyBot = Union[Bot, AutoShardedBot, InteractionBot, AutoShardedInteractionBot]

from disnake.ext.commands.slash_core import InvokableSlashCommand

BOT: Optional[AnyBot] = None

__all__ = ("init", "Plugin")


def init(bot: AnyBot) -> None:
    """Initializes internal state to work with the passed bot instance.

    .. warning::

        This clears all previously registered plugins.

    Parameters
    ----------
    bot: Union[Bot, AutoShardedBot, InteractionBot, AutoShardedInteractionBot]
        Bot instance.
    """
    global BOT

    monkey(bot)

    BOT = bot


def monkey(bot: AnyBot) -> None:
    def load_plugin(self, plugin: Plugin) -> None:
        """Loads plugin and it's content.

        Parameters
        ----------
        plugin: :class:`Plugin`
            The plugin instance to load.
        """
        if plugin.name in self._plugins:
            raise ValueError(f"Plugin with name '{plugin.name}' already loaded")

        self._plugins[plugin.name] = plugin
    
    def unload_plugin(self, plugin_name: str) -> None:
        """Unloads plugin and it's content.

        Parameters
        ----------
        plugin_name: :class:`str`
            The name of the plugin to unload.
        """
        
        if not plugin_name in self._plugins:
            raise ValueError(f"Plugin with name '{plugin_name}' is not loaded")
        
        del self._plugins[plugin_name]


class Plugin:
    """Represents a specific group of related code.

    Parameters
    ----------
    name: :class:`str`
        The plugin's unique name.
    **kwargs: Dict[:class:`str`, Any]
        Data to initialize :attr:`.state` with.

    Attributes
    ----------
    name: :class:`str`
        The plugin's unique name.
    state: Dict[:class:`str`, Any]
        Plugin's state. Can be used for storing various data like category, required permissions etc.
    """

    __slots__ = (
        "name",
        "state",
        "_commands",
        "_groups",
        "_slash_commands",
        "_message_commands",
        "_user_commands",
    )

    def __init__(self, name: str, **kwargs: Dict[str, Any]) -> None:
        if not BOT:
            raise RuntimeError("init() was never called")

        self.name = name
        self.state = kwargs
        self._commands = {}
        self._groups = {}
        self._slash_commands = {}
        self._message_commands = {}
        self._user_commands = {}

        BOT.add_plugin(self)

    def __repr__(self) -> str:
        return f"<Plugin name='{self.name}'>"

    def __str__(self) -> str:
        return self.name

    def slash_command(
        self,
        *,
        name: LocalizedOptional = None,
        description: LocalizedOptional = None,
        dm_permission: Optional[bool] = None,
        default_member_permissions: Optional[Union[Permissions, int]] = None,
        options: Optional[List[Option]] = None,
        guild_ids: Optional[Sequence[int]] = None,
        connectors: Optional[Dict[str, str]] = None,
        auto_sync: Optional[bool] = None,
        extras: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Callable[[CommandCallback], InvokableSlashCommand]:
        """Registers a slash command for this plugin. Same as :func:`disnake.ext.commands.slash_command`."""
    
        def decorator(func: CommandCallback) -> InvokableSlashCommand:
            if not asyncio.iscoroutinefunction(func):
                raise TypeError(f"<{func.__qualname__}> must be a coroutine function")
            if hasattr(func, "__command_flag__"):
                raise TypeError("Callback is already a command.")
            if guild_ids and not all(isinstance(guild_id, int) for guild_id in guild_ids):
                raise ValueError("guild_ids must be a sequence of int.")
            slash = InvokableSlashCommand(
                func,
                name=name,
                description=description,
                options=options,
                dm_permission=dm_permission,
                default_member_permissions=default_member_permissions,
                guild_ids=guild_ids,
                connectors=connectors,
                auto_sync=auto_sync,
                extras=extras,
                **kwargs,
            )

            self._slash_commands[slash.qualified_name] = slash

            return slash

        return decorator
    
