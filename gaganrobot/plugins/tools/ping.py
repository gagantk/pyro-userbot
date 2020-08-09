from datetime import datetime
from gaganrobot import gaganrobot, Message


@gaganrobot.on_cmd(
    "ping", about={'header': "check how long it takes to ping your userbot"})
async def pingme(message: Message):
    start = datetime.now()
    await message.edit('`Pong!`')
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await message.edit(f"**Pong!**\n`{m_s} ms`")
