import os
import json

import ffmpeg

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
        data = ffmpeg.probe(input_file)
        out_str = json.dumps(data, indent=2)
        await message.edit(f'`{out_str}`')
