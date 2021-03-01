import requests
import asyncio
import glob
import os
import wget
import numpy as np
import cv2
import socket
from time import time
from math import floor
from datetime import datetime
from pathlib import Path

from gaganrobot import gaganrobot, Message, Config
from gaganrobot.utils import humanbytes, time_formatter
from gaganrobot.plugins.misc.utube import _tubeDl
from ..misc.upload import upload
from youtube_dl import YoutubeDL

urls = []
ydl = YoutubeDL()
thumb_url = ''
title = ''
startdate = datetime(2021, 2, 28, 0, 0, 0, 0)
airtime = None


@gaganrobot.on_cmd('voot', about={'header': 'Download Voot contents'})
async def voot(message: Message):
    global thumb_url
    await message.edit('Processing...')
    if message.input_str:
        inputs = message.input_str.split()
        download_urls = get_urls(inputs[0])
        formats = get_formats(download_urls)
        if len(inputs) == 1:
            await message.reply_text(f'`{download_urls}`')
            text = '\n'.join(formats)
            generate_thumbs(thumb_url)
            await message.try_to_edit(f"`{text}`")
        elif len(inputs) == 2:
            await download_video(inputs[1], message)


def get_urls(mediaId):
    global thumb_url
    global title
    global airtime
    url = 'http://tvpapi.as.tvinci.com/v3_4/gateways/jsonpostgw.aspx?m=GetMediaInfo'
    jsonObj = {'initObj': {'Locale': {'LocaleLanguage': '', 'LocaleCountry': '', 'LocaleDevice': '', 'LocaleUserState': '0'}, 'Platform': '0',
                           'SiteGuid': '0', 'DomainID': 0, 'UDID': '', 'ApiUser': 'tvpapi_225', 'ApiPass': '11111'}, 'MediaID': '', 'mediaType': 0}
    jsonObj['MediaID'] = mediaId
    res = requests.post(url, json=jsonObj)
    data = res.json()
    medias = []
    for item in data['Metas']:
        if item['Key'] == 'EpisodeMainTitle':
            title = item['Value']
        if item['Key'] == 'Airtime':
            airtime = datetime.strptime(item['Value'], '%d/%m/%Y %H:%M:%S')
    for item in data['Pictures']:
        if item['PicSize'] == '1280X720':
            thumb_url = item['URL']
    hostname = socket.gethostname()
    for item in data['Files']:
        if hostname in ['gagan-arch', 'LIN35006419', 'ip-172-31-39-70']:
            if item['Format'] == 'HLSFPS_TV_PremiumHD' or item['Format'] == '360_Main':
                medias.append(item['URL'])
        else:
            if item['Format'] == '360_Main' or item['Format'] == 'TV Main':
                medias.append(item['URL'])
    return medias


def get_formats(media_urls):
    global urls
    for url in media_urls:
        print(url)
        formats = ydl.extract_info(url, download=False)
        for item in formats['formats']:
            if item['format'].split('x')[-1] in ['360', '480', '720', '1080']:
                urls.append(
                    {'format_id': item['format_id'], 'format': item['format'], 'url': item['url']})
    return [url['format'] for url in urls]


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
    quality = ''
    for item in urls:
        if item['format_id'] == format_id:
            url = item['url']
            quality = item['format'].split('x')[-1]
    retcode = await _tubeDl([url], __progress, startTime, None)
    if retcode == 0:
        _fpath = glob.glob(os.path.join(
            Config.DOWN_PATH, str(startTime), '*'))[0]
        await message.edit(f"**YTDL completed in {round(time() - startTime)} seconds**\n`{_fpath}`")
        thumb = get_biggboss_thumb(quality)
        caption = generate_caption(quality)
        await upload(message, Path(_fpath), thumb=thumb, caption=caption)
    else:
        await message.edit(str(retcode))


def generate_thumbs(url):
    wget.download(url, 'downloads/biggboss.jpg')
    for item in ['360.png', '480.png', '720.png', '1080.png']:
        background = cv2.imread(os.path.join(
            os.getcwd(), 'downloads', 'biggboss.jpg'), -1)
        overlay = cv2.imread(os.path.join(os.getcwd(), 'downloads', item), -1)
        h, w, depth = overlay.shape
        result = np.zeros((h, w, 3), np.uint8)
        for i in range(h):
            for j in range(w):
                color1 = background[i, j]
                color2 = overlay[i, j]
                alpha = color2[3] / 255.0
                new_color = [(1 - alpha) * color1[0] + alpha * color2[0],
                             (1 - alpha) * color1[1] + alpha * color2[1],
                             (1 - alpha) * color1[2] + alpha * color2[2]]
                result[i, j] = new_color
        cv2.imwrite(os.path.join(os.getcwd(), 'downloads',
                                 item.split('.')[0] + '-final.jpg'), result)


def get_biggboss_thumb(quality):
    return os.path.join(os.getcwd(), 'downloads', quality + '-final.jpg')


def generate_caption(quality):
    global airtime
    global startdate
    caption = f'<i>{title}</i>'
    epnum = (airtime - startdate).days
    caption += f'\nBigg Boss Kannada Season 08 - Episode {epnum}'
    caption += f'\n@Bigg_Boss_Kannada'
    return caption


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
