# pylint: disable=missing-module-docstring

__all__ = ['RawClient']

import time
from typing import Optional

from pyrogram import Client

import gaganrobot


class RawClient(Client):
    """ gaganrobot raw client """
    DUAL_MODE = False
    LAST_OUTGOING_TIME = time.time()

    def __init__(self, bot: Optional['gaganrobot.core.client._GaganRobotBot'] = None, **kwargs) -> None:
        self._bot = bot
        super().__init__(**kwargs)
        self._channel = gaganrobot.core.types.new.ChannelLogger(self, "CORE")
        gaganrobot.types.new.Conversation.init(self)
