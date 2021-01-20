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
    globalValues['msg'] = message
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
            dl_loc = os.path.join(Config.DOWN_PATH, os.path.basename(dl_loc))
            data = ffmpeg.probe(dl_loc)
            height = data['streams'][0]['height']
            width = data['streams'][0]['width']
            new_height = 0
            new_width = 0
            if height > width:
                new_width = 600
                new_height = -2
            else:
                new_height = 600
                new_width = -2
            tmp_name = os.path.basename(dl_loc).split('.')
            outputfile = os.path.join(
                Config.DOWN_PATH, tmp_name[0] + '-new.' + tmp_name[1])
            globalValues['output'] = outputfile
            optionsDict = {
                '-vf': f'scale={str(new_width)}:{str(new_height)}', '-c:a': 'copy'}
            setFF()
            ff2 = globalValues['ff'].input(dl_loc).option(
                'y').output(outputfile, optionsDict)
            await ff2.execute()
    else:
        await message.edit("Please read `.help whatsapp`", del_in=5)


def setFF():
    global ff
    ff = globalValues['ff']


@ff.on('start')
async def on_start(arguments):
    # print('Arguments:', arguments)
    msg = globalValues['msg']
    await msg.reply_text('Arguments: ' + str(arguments))
    pass


@ff.on('stderr')
async def on_stderr(line):
    # print('stderr:', line)
    msg = globalValues['msg']
    if 'error' in line.lower():
        await msg.reply_text(str(line))
    pass


@ff.on('progress')
async def on_progress(progress):
    msg = globalValues['msg']
    # total = globalValues['total']
    # currentTime = progress.time.split(':')
    # current = int(currentTime[0]) * 3600 + int(currentTime[1]
    #                                            ) * 60 + int(currentTime[2].split('.')[0])
    # size = progress.size
    # delay = 5
    # ud_type = 'Transcoding'
    # file_name = globalValues['file']
    # if msg.process_is_canceled:
    #     await msg.client.stop_transmission()
    # task_id = f"{msg.chat.id}.{msg.message_id}"
    # if current == total:
    #     if task_id in _TASKS:
    #         del _TASKS[task_id]
    #     try:
    #         await msg.try_to_edit("`finalizing process ...`")
    #     except FloodWait as f_e:
    #         time.sleep(f_e.x)
    #     return
    # now = time.time()
    # if task_id not in _TASKS:
    #     _TASKS[task_id] = (now, now)
    # start, last = _TASKS[task_id]
    # elapsed_time = now - start
    # if (now - last) >= delay:
    #     _TASKS[task_id] = (start, now)
    #     percentage = current * 100 / total
    #     transcode_speed = str(progress.speed) + 'x'
    #     speed = current / elapsed_time
    #     time_to_completion = time_formatter(int((total - current) / speed))
    #     progress_str = \
    #         "__{}__: `{}`\n" + \
    #         "```[{}{}]```\n" + \
    #         "**Progress**: `{}%`\n" + \
    #         "**Completed**: `{}`\n" + \
    #         "**Speed**: `{}`\n" + \
    #         "**ETA**: `{}`"
    #     progress_str = progress_str.format(
    #         ud_type,
    #         file_name,
    #         ''.join((Config.FINISHED_PROGRESS_STR
    #                  for i in range(floor(percentage / 5)))),
    #         ''.join((Config.UNFINISHED_PROGRESS_STR
    #                  for i in range(20 - floor(percentage / 5)))),
    #         round(percentage, 2),
    #         humanbytes(size),
    #         transcode_speed,
    #         time_to_completion if time_to_completion else "0 s")
    #     try:
    #         await msg.try_to_edit(progress_str)
    #     except FloodWait as f_e:
    #         time.sleep(f_e.x)


@ff.on('completed')
async def on_completed():
    # print('Completed')
    msg = globalValues['msg']
    await upload(msg, Path(globalValues['output']), upload_as_doc=False)
    del globalValues['ff']
    globalValues['ff'] = FFmpeg()
    pass


@ff.on('terminated')
def on_terminated():
    # print('Terminated')
    del globalValues['ff']
    globalValues['ff'] = FFmpeg()
    pass


@ff.on('error')
async def on_error(code):
    msg = globalValues['msg']
    await msg.edit(str(msg))
    del globalValues['ff']
    globalValues['ff'] = FFmpeg()
    pass
