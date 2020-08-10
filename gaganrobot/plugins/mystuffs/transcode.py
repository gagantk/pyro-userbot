from gaganrobot import gaganrobot, Message

LOGGER = gaganrobot.getLogger(__name__)


@gaganrobot.on_cmd('transcode', about: {'header': 'Transcode media files using ffmpeg', 'description': 'Transcode media files using ffmpeg', 'examples': '{tr}transcode input_file opts output_file'})
async def transcode(message: Message):
    """ transcode media file """
