import os
import json

import ffmpeg
from ffmpeg import Error

from gaganrobot import gaganrobot, Message, Config

LOGGER = gaganrobot.getLogger(__name__)


@gaganrobot.on_cmd('ffprobe', about={'header': 'Metadata of media files',
                                     'description': 'Get metadata info of media files using ffprobe',
                                     'examples': '{tr}ffprobe input_file'})
async def ffprobe(message: Message):
    """ metadata of media files """
    await message.edit('`Gathering info...`')
    if message.input_str:
        input_file = os.path.join(Config.DOWN_PATH, message.input_str)
        try:
            data = ffmpeg.probe(input_file)
        except Error as e:
            await message.reply_text(e.stderr, del_in=60)
            return
        out_str = json.dumps(data, indent=2)
        if len(out_str) > Config.MAX_MESSAGE_LENGTH:
            with open(os.path.join(Config.DOWN_PATH, 'probe.txt'), 'w') as f:
                f.write(out_str)
            await message.reply_document(os.path.join(Config.DOWN_PATH, 'probe.txt'))
        else:
            await message.edit(f'`{out_str}`')
