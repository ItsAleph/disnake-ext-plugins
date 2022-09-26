# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

if TYPE_CHECKING:
    from disnake.ext.commands import (
        AutoShardedBot,
        AutoShardedInteractionBot,
        Bot,
        InteractionBot,
    )

    AnyBot = Union[Bot, AutoShardedBot, InteractionBot, AutoShardedInteractionBot]

BOT: Optional[AnyBot] = None
PLUGINS: Dict[str, Any] = {}

__all__ = ("init", "Plugin")


def init(bot: AnyBot) -> None:
    global PLUGINS, BOT

    PLUGINS.clear()
    BOT = bot


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

    __slots__ = ("name", "state")

    def __init__(self, name: str, **kwargs: Dict[str, Any]) -> None:
        if name in PLUGINS:
            raise ValueError(f"Plugin with name '{name}' already exists")

        self.name = name
        self.state = kwargs

        PLUGINS[name] = self

    def __repr__(self) -> str:
        return f"<Plugin name='{self.name}'>"

    def __str__(self) -> str:
        return self.name
