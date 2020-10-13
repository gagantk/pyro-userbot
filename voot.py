import requests, sys, json, youtube_dl.utils
from youtube_dl import YoutubeDL

ydl = YoutubeDL()
urls = []
youtube_dl.utils.std_headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'

def get_url():
    url = 'http://tvpapi.as.tvinci.com/v3_4/gateways/jsonpostgw.aspx?m=GetMediaInfo'
    jsonObj = {'initObj': {'Locale': {'LocaleLanguage': '', 'LocaleCountry': '', 'LocaleDevice': '', 'LocaleUserState': '0'}, 'Platform': '0', 'SiteGuid': '0', 'DomainID': 0, 'UDID': '', 'ApiUser': 'tvpapi_225', 'ApiPass': '11111'}, 'MediaID': '', 'mediaType': 0}
    jsonObj['MediaID'] = sys.argv[1]
    res = requests.post(url, json=jsonObj)
    data = res.json()
    for item in data['Files']:
        if item['Format'] == 'TV Main':
            print(item['URL'])
            return item['URL']
        
def download_video():
    url = ''
    for item in urls:
        if item['format_id'] == sys.argv[2]:
            url = item['url']
    ydl_opts = {
        'outtmpl': f'{name}-{sys.argv[2]}.mp4',    
        'noplaylist' : True,
        'progress_hooks': [my_hook],
    }
    with YoutubeDL(ydl_opts) as ydl2:
        ydl2.download([url])
        
def get_formats(url):
    global urls
    formats = ydl.extract_info(url, download=False)
    for item in formats['formats']:
        urls.append({'format_id': item['format_id'], 'format': item['format'], 'url': item['url']})
    for url in urls:
        print(url['format'])
        
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

download_url = get_url()
get_formats(download_url)
if len(sys.args) == 3:
    download_video()
