from youtube_dl import YoutubeDL
from webvtt import WebVTT
from html2text import HTML2Text
from pysrt.srtitem import SubRipItem
from pysrt.srttime import SubRipTime
import sys
import requests
import wget
import os
import html

from gaganrobot import gaganrobot, Config, Message

ydl = YoutubeDL()
name = ''
ext = ''
urls = []


@gaganrobot.on_cmd('zee5', about={'header': 'Download Zee5 contents'})
async def zee(message: Message):
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
            if inputs[1] == 'subs':
                if not download_subs(inputs[0]):
                    await message.try_to_edit('`Subtitles not available!`')
            else:
                pass


def get_url(movie_id):
    zee_api = f'https://gwapi.zee5.com/content/details/0-0-{movie_id}?translation=en&country=IN'
    res = requests.get(zee_api)
    data = res.json()
    hls_url = data['video_details']['hls_url'].replace('drm', 'hls')
    global name
    name = data['title']
    download_url = 'https://zee5vodnd.akamaized.net' + hls_url + get_token()
    return download_url


def get_token():
    token_url = 'https://useraction.zee5.com/tokennd/'
    return requests.get(token_url).json()['video_token']


def get_formats(url):
    global urls
    formats = ydl.extract_info(url, download=False)
    for item in formats['formats']:
        urls.append({'format_id': item['format_id'].replace(
            'ಕನ್ನಡ', 'kn'), 'format': item['format'].replace('ಕನ್ನಡ', 'kn'), 'url': item['url']})
        # urls[item['format'].replace('ಕನ್ನಡ', 'kn')] = item['url']
    return urls


def download_video(format_id):
    url = ''
    for item in urls:
        if item['format_id'] == format_id:
            url = item['url']
    ydl_opts = {
        'outtmpl': f'{name}-{format_id}.mp4',
        'noplaylist': True,
        'progress_hooks': [my_hook],
    }
    with YoutubeDL(ydl_opts) as ydl2:
        ydl2.download([url])


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_subs(movie_id):
    zee_api = f'https://gwapi.zee5.com/content/details/0-0-{movie_id}?translation=en&country=IN'
    res = requests.get(zee_api)
    data = res.json()
    if not data['subtitle_languages']:
        return False
    hls_url = data['video_details']['hls_url']
    url = 'https://zee5vod.akamaized.net'
    url += hls_url.replace('index.m3u8', 'manifest-en.vtt')
    wget.download(url, os.path.join(Config.DOWN_PATH, name + '-subs.vtt'))
    convert(os.path.join(Config.DOWN_PATH, name + '-subs.vtt'))
    return True


def convert(arg):
    file_name, file_extension = os.path.splitext(arg)
    index = 0

    if not file_extension.lower() == ".vtt":
        sys.stderr.write("Skipping %s.\n" % arg)
        return

    srt = open(file_name + ".srt", "w")

    for caption in WebVTT().read(arg):
        index += 1
        start = SubRipTime(0, 0, caption.start_in_seconds)
        end = SubRipTime(0, 0, caption.end_in_seconds)
        srt.write(SubRipItem(
            index, start, end, html.unescape(caption.text))
            .__str__()+"\n")
    os.remove(arg)


# download_url = get_url()
# get_formats(download_url)
# if len(sys.argv) == 3:
#     if sys.argv[2] == 'subs':
#         download_subs()
#     else:
#         download_video()
