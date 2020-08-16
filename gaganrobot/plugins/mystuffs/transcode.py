import os
import subprocess as sp
import re
import time
import sys
from math import floor
from pathlib import Path

import ffmpeg
from typing import Dict, Tuple
from pyrogram.errors.exceptions import FloodWait

from gaganrobot import gaganrobot, Message, Config
from gaganrobot.utils.tools import time_formatter, humanbytes, runcmd
from gaganrobot.utils.ffmpeg2.ffmpeg import FFmpeg
from ..misc.upload import upload

LOGGER = gaganrobot.getLogger(__name__)

_TASKS: Dict[str, Tuple[int, int]] = {}
globalValues = {'ff': FFmpeg(), 'msg': None, 'total': 0}
ff = globalValues['ff']


@gaganrobot.on_cmd('transcode', about={'header': 'Transcode media files using ffmpeg', 'description': 'Transcode media files using ffmpeg', 'usage': '{tr}transcode input_file | output_file | size | [scale] | [-s srt_file]', 'examples': ['{tr}transcode in.mp4 | In (2000) - HDRip | 400', '{tr}transcode in.mp4 | In (2001) - HDRip - ESubs | 900 | 1280:-1', '{tr}transcode in.mp4 in.srt | In (2003) - HDRip - ESubs | 700 | -s']})
async def transcode(message: Message):
    """ transcode media file """
    await message.edit('`Processing...`')
    global globalValues
    globalValues['msg'] = message
    if message.input_str:
        inputs = [word.strip() for word in message.input_str.split('|')]
        srt_file = ''
        if '-s' in message.input_str and len(inputs[0].split()) == 2:
            srt_file = os.path.join(
                Config.DOWN_PATH, inputs[0].split()[1].strip())
            input_file = os.path.join(
                Config.DOWN_PATH, inputs[0].split()[0].strip())
        else:
            input_file = os.path.join(Config.DOWN_PATH, inputs[0])
        file_name = inputs[1].split('-')
        target_size = inputs[2]
        globalValues['total'] = int(ffmpeg.probe(
            input_file)['format']['duration'].split('.')[0])
        try:
            data = ffmpeg.probe(input_file)
            video_codec = data['streams'][0]['codec_name']
            audio_codec = data['streams'][1]['codec_name']
            audio_bitrate = int(data['streams'][1]['bit_rate'])
        except KeyError:
            cmd = f"ffmpeg -i {input_file} -c:a copy {os.path.join(Config.DOWN_PATH, 'audio.' + audio_codec)} -y"
            await runcmd(cmd)
            audio_bitrate = int(ffmpeg.probe(os.path.join(
                Config.DOWN_PATH, f'audio.{audio_codec}'))['format']['bit_rate'])
        bitrate, size_name = calculate_bitrate(
            int(target_size), globalValues['total'], audio_bitrate)
        if len(file_name) == 2:
            globalValues['file'] = f"{file_name[0].strip()} - {file_name[1].strip()} - {size_name}.mkv"
            metadata_file_name = f"https://t.me/Kannada_Movies_HDs - {file_name[0].strip()} - {file_name[1].strip()} - {video_codec.replace('h', 'x')} - {audio_codec.upper()} - {size_name}"
        elif len(file_name) == 3 and file_name[2].strip() == 'ESubs':
            globalValues['file'] = f"{file_name[0].strip()} - {file_name[1].strip()} - {file_name[2].strip()} - {size_name}.mkv"
            metadata_file_name = f"https://t.me/Kannada_Movies_HDs - {file_name[0].strip()} - {file_name[1].strip()} - {video_codec.replace('h', 'x')} - {audio_codec.upper()} - {file_name[2].strip()} - {size_name}"
        elif len(file_name) == 3 and (file_name[2].strip() == '720p' or file_name[2].strip() == '1080p'):
            globalValues['file'] = f"{file_name[0].strip()} - {file_name[1].strip()} - {file_name[2].strip()} - {video_codec.replace('h', 'x')} - {size_name}.mkv"
            metadata_file_name = f"https://t.me/Kannada_Movies_HDs - {file_name[0].strip()} - {file_name[1].strip()} - {video_codec.replace('h', 'x')} - {audio_codec.upper()} - {file_name[2].strip()} - {size_name}"
        elif len(file_name) == 4 and (file_name[2].strip() == '720p' or file_name[2].strip() == '1080p'):
            globalValues['file'] = f"{file_name[0].strip()} - {file_name[1].strip()} - {file_name[2].strip()} - {video_codec.replace('h', 'x')} - {file_name[3].strip()} - {size_name}.mkv"
            metadata_file_name = f"https://t.me/Kannada_Movies_HDs - {file_name[0].strip()} - {file_name[1].strip()} - {video_codec.replace('h', 'x')} - {audio_codec.upper()} - {file_name[2].strip()} - {file_name[3].strip()} - {size_name}"
        if len(globalValues['file']) > 64:
            globalValues['file'] = globalValues['file'].replace('x264 - ', '')
            if len(globalValues['file']) > 64:
                globalValues['file'] = globalValues['file'].replace(
                    'ESubs - ', '')
        output_file = os.path.join(Config.DOWN_PATH, globalValues['file'])
        globalValues['output'] = output_file
        optionsDict = {'-b:v': bitrate + 'k', '-c:a': 'copy', '-metadata': f'title={metadata_file_name}',
                       '-metadata:s:v:0': 'language=kan', '-metadata:s:v:0': 'title="https://t.me/Kannada_Movies_HDs"',
                       '-metadata:s:a:0': 'language=kan', '-metadata:s:a:0': 'title = "https://t.me/Kannada_Movies_HDs"'}
        if len(inputs) == 4 and '-s' not in inputs[3]:
            optionsDict['-vf'] = f'scale={inputs[3]}'
        elif len(inputs) == 4 and '-s' in inputs[3]:
            optionsDict['-c:s'] = 'copy'
            optionsDict['-metadata:s:s:0'] = 'language=eng'
            optionsDict['-metadata:s:s:0'] = 'title="https://t.me/Kannada_Movies_HDs"'
            optionsDict['-disposition:s:0'] = 'default'
        elif len(inputs) == 5 and '-s' in inputs[4]:
            optionsDict['-vf'] = f'scale={inputs[3]}'
            optionsDict['-c:s'] = 'copy'
            optionsDict['-metadata:s:s:0'] = 'language=eng'
            optionsDict['-metadata:s:s:0'] = 'title="https://t.me/Kannada_Movies_HDs"'
            optionsDict['-disposition:s:0'] = 'default'
        setFF()
        if srt_file:
            ff2 = globalValues['ff'].input(input_file).input(srt_file).option(
                'y').output(output_file, optionsDict)
        else:
            ff2 = globalValues['ff'].input(input_file).option(
                'y').output(output_file, optionsDict)
        await ff2.execute()
    else:
        await message.edit("Please read `.help transcode`", del_in=5)


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
    total = globalValues['total']
    currentTime = progress.time.split(':')
    current = int(currentTime[0]) * 3600 + int(currentTime[1]
                                               ) * 60 + int(currentTime[2].split('.')[0])
    size = progress.size
    delay = 5
    ud_type = 'Transcoding'
    file_name = globalValues['file']
    if msg.process_is_canceled:
        await msg.client.stop_transmission()
    task_id = f"{msg.chat.id}.{msg.message_id}"
    if current == total:
        if task_id in _TASKS:
            del _TASKS[task_id]
        try:
            await msg.try_to_edit("`finalizing process ...`")
        except FloodWait as f_e:
            time.sleep(f_e.x)
        return
    now = time.time()
    if task_id not in _TASKS:
        _TASKS[task_id] = (now, now)
    start, last = _TASKS[task_id]
    elapsed_time = now - start
    if (now - last) >= delay:
        _TASKS[task_id] = (start, now)
        percentage = current * 100 / total
        transcode_speed = str(progress.speed) + 'x'
        speed = current / elapsed_time
        time_to_completion = time_formatter(int((total - current) / speed))
        progress_str = \
            "__{}__: `{}`\n" + \
            "```[{}{}]```\n" + \
            "**Progress**: `{}%`\n" + \
            "**Completed**: `{}`\n" + \
            "**Speed**: `{}`\n" + \
            "**ETA**: `{}`"
        progress_str = progress_str.format(
            ud_type,
            file_name,
            ''.join((Config.FINISHED_PROGRESS_STR
                     for i in range(floor(percentage / 5)))),
            ''.join((Config.UNFINISHED_PROGRESS_STR
                     for i in range(20 - floor(percentage / 5)))),
            round(percentage, 2),
            humanbytes(size),
            transcode_speed,
            time_to_completion if time_to_completion else "0 s")
        try:
            await msg.try_to_edit(progress_str)
        except FloodWait as f_e:
            time.sleep(f_e.x)


@ff.on('completed')
async def on_completed():
    # print('Completed')
    msg = globalValues['msg']
    caption = f"<b>{globalValues['file'].replace('.mkv', '')}</b>\n\n@Kannada_Movies_HDs\nhttps://t.me/Kannada_Movies_HDs"
    await upload(msg, Path(globalValues['output']), upload_as_doc=True, caption=caption)
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


def calculate_bitrate(size, total, audio_bitrate):
    audio_bitrate = round(audio_bitrate / 1000)
    if size == 400:
        bitrate = round(size * 8 * 1024 / total - audio_bitrate + 10)
        mod = bitrate % 5
        if mod != 0:
            bitrate = bitrate + 5 - mod
    elif size == 700:
        bitrate = round(size * 8 * 1024 / total - audio_bitrate + 15)
        mod = bitrate % 5
        if mod != 0:
            bitrate = bitrate + 5 - mod
    elif size == 900:
        bitrate = round(size * 8 * 1024 / total - audio_bitrate + 20)
        mod = bitrate % 5
        if mod != 0:
            bitrate = bitrate + 5 - mod
    elif size > 1100 and size < 1500:
        bitrate = round(size * 8 * 1024 / total - audio_bitrate + 40)
        mod = bitrate % 5
        if mod != 0:
            bitrate = bitrate + 5 - mod
    elif size > 1500:
        bitrate = round(size * 8 * 1024 / total - audio_bitrate + 60)
        mod = bitrate % 5
        if mod != 0:
            bitrate = bitrate + 5 - mod
    if size > 1000:
        out = str(round(size / 1000, 1)) + 'GB'
    else:
        out = str(size) + 'MB'
    return (str(bitrate), out)
