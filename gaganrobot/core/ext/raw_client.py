# pylint: disable=missing-module-docstring

__all__ = ['RawClient']

from typing import Optional

import nest_asyncio
from pyrogram import Client

from .. import types, client  # pylint: disable=unused-import


class RawClient(Client):
    """ gaganrobot raw client """
    DUAL_MODE = False

    def __init__(self, bot: Optional['client._GaganRobotBot'] = None, **kwargs) -> None:
        self._bot = bot
        super().__init__(**kwargs)
        self._channel = types.new.ChannelLogger(self, "CORE")
        types.new.Conversation.init(self)
        nest_asyncio.apply()
