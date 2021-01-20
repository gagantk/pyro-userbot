from gaganrobot import gaganrobot, Message, Config
from gaganrobot.utils import progress
import ffmpeg
import os
from pathlib import Path

from gaganrobot.utils.ffmpeg2.ffmpeg import FFmpeg
from ..misc.upload import upload

LOGGER = gaganrobot.getLogger(__name__)
globalValues = {'ff': FFmpeg(), 'msg': None, 'total': 0}
ff = globalValues['ff']


@gaganrobot.on_cmd('whatsapp', about={'header': 'Compress your videos for WhatsApp', 'description': 'Compress your videos to fit for WhatsApp status/messages', 'usage': '{tr}whatsapp'})
async def whatsapp(message: Message):
    """ Convert to WhatsApp media """
    await message.edit('`Processing...`')
    global globalValues
    if message.reply_to_message and message.reply_to_message.video:
        dl_loc = await message.client.download_media(
            message=message.reply_to_message,
            file_name=Config.DOWN_PATH,
            progress=progress,
            progress_args=(message, 'Trying to download...')
        )
        if message.process_is_canceled:
            await message.edit("`Process Canceled!`", del_in=5)
        else:
            await message.delete()
            print(dl_loc)
            dl_loc = os.path.join(Config.DOWN_PATH, os.path.basename(dl_loc))
            print(dl_loc)
            data = ffmpeg.probe(dl_loc)
            height = data['streams'][0]['height']
            width = data['streams'][0]['width']
            new_height = 0
            new_width = 0
            if height > width:
                new_width = 600
                new_height = round(height / width * 600)
            else:
                new_height = 600
                new_width = round(width / height * 600)
            return
            outputfile = ''
            optionsDict = {}
            setFF()
            ff2 = globalValues['ff'].input(dl_loc).option(
                'y').output(outputfile, optionsDict)
            new_loc = os.path.join(
                Config.DOWN_PATH, message.filtered_input_str)
            os.rename(dl_loc, new_loc)
            await upload(message, Path(new_loc), True)
    else:
        await message.edit("Please read `.help rename`", del_in=5)


def setFF():
    global ff
    ff = globalValues['ff']
