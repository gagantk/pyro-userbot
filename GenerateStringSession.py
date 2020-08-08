#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from pyrogram import Client

try:
    from myrobot import API_ID, API_HASH
except ModuleNotFoundError:
    API_ID = int(input("Enter Telegram API ID: "))
    API_HASH = input("Enter Telegram API HASH: ")


async def main(api_id, api_hash):
    async with Client(":memory:", api_id=api_id, api_hash=api_hash) as app:
        print(app.export_string_session())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(API_ID, API_HASH))
