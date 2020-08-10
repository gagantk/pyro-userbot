from pyrogram.errors.exceptions import FileIdInvalid, FileReferenceEmpty
from pyrogram.errors.exceptions.bad_request_400 import BadRequest, ChannelInvalid, MediaEmpty

from gaganrobot import gaganrobot, Message, Config, versions, get_version

LOGO_STICKER_ID, LOGO_STICKER_REF = None, None


@gaganrobot.on_cmd("alive", about={
    'header': "This command is just for fun"}, allow_channels=False)
async def alive(message: Message):
    await message.delete()
    await sendit(message)
    output = f"""
**GaganRobot is Up and Running**

       __Durable as a Serge__

• **uptime** : `{gaganrobot.uptime}`
• **python version** : `{versions.__python_version__}`
• **pyrogram version** : `{versions.__pyro_version__}`
• **gaganrobot version** : `{get_version()}`
• **unofficial enabled** : `{Config.LOAD_UNOFFICIAL_PLUGINS}`
• **repo** : [GaganRobot]({Config.UPSTREAM_REPO})
"""
    await message.client.send_message(message.chat.id, output, disable_web_page_preview=True)


async def refresh_id():
    global LOGO_STICKER_ID, LOGO_STICKER_REF  # pylint: disable=global-statement
    sticker = (await gaganrobot.get_messages('theUserge', 8)).sticker
    LOGO_STICKER_ID = sticker.file_id
    LOGO_STICKER_REF = sticker.file_ref


async def send_sticker(message):
    try:
        await message.client.send_sticker(
            message.chat.id, LOGO_STICKER_ID, file_ref=LOGO_STICKER_REF)
    except MediaEmpty:
        pass


async def sendit(message):
    if LOGO_STICKER_ID:
        try:
            await send_sticker(message)
        except (FileIdInvalid, FileReferenceEmpty, BadRequest):
            try:
                await refresh_id()
            except ChannelInvalid:
                pass
            else:
                await send_sticker(message)
    else:
        try:
            await refresh_id()
        except ChannelInvalid:
            pass
        else:
            await send_sticker(message)
