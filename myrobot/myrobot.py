#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyrogram import Client, __version__
from pyrogram.api.all import layer

from myrobot import (API_ID, API_HASH, HU_STRING_SESSION,
                     TMP_DOWNLOAD_DIRECTORY, LOGGER)


class MyRobot(Client):

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(HU_STRING_SESSION, plugins=dict(
            root=f'{name}/plugins'), workdir=TMP_DOWNLOAD_DIRECTORY, api_id=API_ID, api_hash=API_HASH)

    async def start(self):
        await super().start()

        user_bot_me = await self.get_me()
        self.set_parse_mode('html')
        LOGGER.info(f'User bot based on Pyrogram v{__version__}'
                    f'(Layer {layer}) started on @{user_bot_me.username}.'
                    'Hi.'
                    )

    async def stop(self, *args):
        await super().stop()
        LOGGER.info('Userbot stopped. Bye.')
