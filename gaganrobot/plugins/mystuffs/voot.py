import requests
import asyncio
import glob
import os
from time import time
from math import floor

from gaganrobot import gaganrobot, Message, Config
from gaganrobot.utils import humanbytes, time_formatter
from gaganrobot.plugins.misc.utube import _tubeDl
from youtube_dl import YoutubeDL

urls = []
ydl = YoutubeDL()


@gaganrobot.on_cmd('voot', about={'header': 'Download Voot contents'})
async def voot(message: Message):
    await message.edit('Processing...')
    if message.input_str:
        inputs = message.input_str.split()
        download_url = get_url(inputs[0])
        formats = get_formats(download_url)
        if len(inputs) == 1:
            await message.reply_text(f'`{download_url}`')
            text = '\n'.join(formats)
            await message.try_to_edit(f"`{text}`")
        elif len(inputs) == 2:
            await download_video(inputs[1], message)


def get_url(mediaId):
    url = 'http://tvpapi.as.tvinci.com/v3_4/gateways/jsonpostgw.aspx?m=GetMediaInfo'
    jsonObj = {'initObj': {'Locale': {'LocaleLanguage': '', 'LocaleCountry': '', 'LocaleDevice': '', 'LocaleUserState': '0'}, 'Platform': '0',
                           'SiteGuid': '0', 'DomainID': 0, 'UDID': '', 'ApiUser': 'tvpapi_225', 'ApiPass': '11111'}, 'MediaID': '', 'mediaType': 0}
    jsonObj['MediaID'] = mediaId
    res = requests.post(url, json=jsonObj)
    data = res.json()
    for item in data['Files']:
        if item['Format'] == 'TV Main':
            return item['URL']


def get_formats(url):
    global urls
    formats = ydl.extract_info(url, download=False)
    for item in formats['formats']:
        urls.append(
            {'format_id': item['format_id'], 'format': item['format'], 'url': item['url']})
    return urls


async def download_video(format_id: str, message: Message):
    def __progress(data: dict):
        if ((time() - startTime) % 4) > 3.9:
            if data['status'] == 'downloading':
                eta = data.get('eta')
                speed = data.get('speed')
                if not (eta and speed):
                    return
                current = data.get('downloaded_bytes')
                total = data.get("total_bytes")
                progress_str = f"**FILENAME**: `{data['filename']}`\n" + \
                    f"**Speed**: `{humanbytes(speed)}`\n" + \
                    f"**ETA**: `{time_formatter(eta)}`"
                if current and total:
                    percentage = int(current) * 100 / int(total)
                    fin = ''.join((Config.FINISHED_PROGRESS_STR
                                   for i in range(floor(percentage / 5))))
                    unfin = ''.join((Config.UNFINISHED_PROGRESS_STR
                                     for i in range(20 - floor(percentage / 5))))
                    progress_str = f"__Downloading__\n" + \
                        f"```[{fin}{unfin}]```\n" + \
                        f"**Progress**: `{round(percentage, 2)}%`\n" + \
                        f"**Completed**: `{humanbytes(current)}`\n" + \
                        f"**Total**: `{humanbytes(total)}`\n" + progress_str
                if message.text != progress_str:
                    asyncio.get_event_loop().run_until_complete(message.edit(progress_str))
    url = ''
    startTime = time()
    for item in urls:
        if item['format_id'] == format_id:
            url = item['url']
    retcode = await _tubeDl([url], __progress, startTime, None)
    if retcode == 0:
        _fpath = glob.glob(os.path.join(
            Config.DOWN_PATH, str(startTime), '*'))[0]
        await message.edit(f"**YTDL completed in {round(time() - startTime)} seconds**\n`{_fpath}`")
    else:
        await message.edit(str(retcode))


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
