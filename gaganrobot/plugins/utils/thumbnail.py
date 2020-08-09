import os
from datetime import datetime
from gaganrobot import gaganrobot, Config, Message
from gaganrobot.utils import progress

THUMB_PATH = Config.DOWN_PATH + "thumb_image.jpg"
CHANNEL = gaganrobot.getCLogger(__name__)


@gaganrobot.on_cmd('sthumb', about={
    'header': "Save thumbnail",
    'usage': "{tr}sthumb [reply to any photo]"})
async def save_thumb_nail(message: Message):
    """ setup thumbnail """
    await message.edit("processing ...")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                 or (replied.document and "image" in replied.document.mime_type))):
        start_t = datetime.now()
        if os.path.exists(THUMB_PATH):
            os.remove(THUMB_PATH)
        await message.client.download_media(message=replied,
                                            file_name=THUMB_PATH,
                                            progress=progress,
                                            progress_args=(message, "trying to download"))
        end_t = datetime.now()
        m_s = (end_t - start_t).seconds
        await message.edit(f"thumbnail saved in {m_s} seconds.", del_in=3)
    else:
        await message.edit("Reply to a photo to save custom thumbnail", del_in=3)


@gaganrobot.on_cmd('dthumb', about={'header': "Delete thumbnail"}, allow_channels=False)
async def clear_thumb_nail(message: Message):
    """ delete thumbnail """
    await message.edit("`processing ...`")
    if os.path.exists(THUMB_PATH):
        os.remove(THUMB_PATH)
        await message.edit("✅ Custom thumbnail deleted succesfully.", del_in=3)
    elif os.path.exists('resources/gaganrobot.png'):
        os.remove('resources/gaganrobot.png')
        await message.edit("✅ Default thumbnail deleted succesfully.", del_in=3)
    else:
        await message.delete()


@gaganrobot.on_cmd('vthumb', about={'header': "View thumbnail"}, allow_channels=False)
async def get_thumb_nail(message: Message):
    """ view current thumbnail """
    await message.edit("processing ...")
    if os.path.exists(THUMB_PATH):
        msg = await message.client.send_document(chat_id=message.chat.id,
                                                 document=THUMB_PATH,
                                                 disable_notification=True,
                                                 reply_to_message_id=message.message_id)
        await CHANNEL.fwd_msg(msg)
        await message.delete()
    else:
        await message.err("Custom Thumbnail Not Found!")
