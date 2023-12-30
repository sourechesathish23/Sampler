import requests
from time import sleep
from configparser import ConfigParser
from os import system, name
from threading import Thread, active_count
from re import search, compile
from pyrogram import *
import time
import random
import asyncio
from aiohttp import web
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({"status": "running"})

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app


API_ID = int(15037283)
API_HASH = "7af9d761267bf6b81ed07f942d87127f"
BOT_TOKEN = "6334686364:AAFVuAT7Q5RtZwHu7ADAtPN15O4lQPEFVAU"
CHAT_ID = int(-1002101125659)

BOT_TOKEN_1 = "6146752046:AAF48W04fOJG_YP0jvhz8BSVjYcYMIOk-Tk"
BOT_TOKEN_2 = "6512487247:AAGQ9tRRxJOvxIHVbYeDKpVQVsSbEH1oPmY"
BOT_TOKEN_3 = "6363810728:AAFSeJvheOUFnK17b1KLVsocM_Xtr17NpUw"
BOT_TOKEN_4 = "6319165094:AAEmrS00GSq39Am61acXXhauL7CUefZcy9U"
BOT_TOKEN_5 = "6454637844:AAEFjOOuW9Hb5xgwIpmUyssqTkUhLEF1Y3o"


app = Client(name="STARK",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN,in_memory=False)
app.start()
print("APP Started")
app1 = Client(name="STARK1",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN_1,in_memory=False)
app1.start()
print("APP1 Started")
app2 = Client(name="STARK2",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN_2,in_memory=False)
app2.start()
print("APP2 Started")
app3 = Client(name="STARK3",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN_3,in_memory=False)
app3.start()
print("APP3 Started")
app4 = Client(name="STARK4",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN_4,in_memory=False)
app4.start()
print("APP4 Started")
app5 = Client(name="STARK5",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN_5,in_memory=False)
app5.start()
print("APP5 Started")

apps = [app,app1,app2,app3,app4,app5]

THREADS = 1000
PROXIES_TYPES = ('http', 'socks4', 'socks5')
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
REGEX = compile(r"(?:^|\D)?(("+ r"(?:[1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"\." + r"(?:\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])"
                + r"):" + (r"(?:\d|[1-9]\d{1,3}|[1-5]\d{4}|6[0-4]\d{3}"
                + r"|65[0-4]\d{2}|655[0-2]\d|6553[0-5])")
                + r")(?:\D|$)")

errors = open('errors.txt', 'a+')
cfg = ConfigParser(interpolation=None)
cfg.read("config.ini", encoding="utf-8")

http, socks4, socks5 = '', '', ''
try: http, socks4, socks5 = cfg["HTTP"], cfg["SOCKS4"], cfg["SOCKS5"]
except KeyError: print(' [ OUTPUT ] Error | config.ini not found!');sleep(3);exit()

http_proxies, socks4_proxies, socks5_proxies = [], [], []
proxy_errors, token_errors = 0, 0
channel, post, time_out, real_views = '', 0, 15, 0
channel = "marvelcloud"
post = "169"

def scrap(sources, _proxy_type):
    for source in sources:
        if source:
            try: response = requests.get(source, timeout=time_out)
            except Exception as e: errors.write(f'{e}\n')
            if tuple(REGEX.finditer(response.text)):
                for proxy in tuple(REGEX.finditer(response.text)):
                    if _proxy_type == 'http': http_proxies.append(proxy.group(1))
                    elif _proxy_type == 'socks4': socks4_proxies.append(proxy.group(1))
                    elif _proxy_type == 'socks5': socks5_proxies.append(proxy.group(1))


def start_scrap():
    threads = []
    for i in (http_proxies, socks4_proxies, socks5_proxies): i.clear()
    for i in ((http.get("Sources").splitlines(), 'http'), (socks4.get("Sources").splitlines(), 'socks4'), (socks5.get("Sources").splitlines(), 'socks5')):
        thread = Thread(target=scrap, args=(i[0], i[1]))
        threads.append(thread)
        thread.start()
    for t in threads: t.join()


def get_token(proxy, proxy_type):
    try:
        session = requests.session()
        response = session.get(f'https://t.me/{channel}/{post}', params={'embed': '1', 'mode': 'tme'},
                    headers={'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT},
                    proxies={'http': f'{proxy_type}://{proxy}', 'https': f'{proxy_type}://{proxy}'},
                    timeout=time_out)
        return search('data-view="([^"]+)', response.text).group(1), session
    except AttributeError: return 2
    except requests.exceptions.RequestException: 1
    except Exception as e: return errors.write(f'{e}\n')

def send_view(token, session, proxy, proxy_type):
    try:
        cookies_dict = session.cookies.get_dict()
        response = session.get('https://t.me/v/', params={'views': str(token)}, cookies={
            'stel_dt': '-240', 'stel_web_auth': 'https%3A%2F%2Fweb.telegram.org%2Fz%2F',
            'stel_ssid': cookies_dict.get('stel_ssid', None), 'stel_on': cookies_dict.get('stel_on', None)},
                            headers={'referer': f'https://t.me/{channel}/{post}?embed=1&mode=tme',
                                'user-agent': USER_AGENT, 'x-requested-with': 'XMLHttpRequest'},
                            proxies={'http': f'{proxy_type}://{proxy}', 'https': f'{proxy_type}://{proxy}'},
                            timeout=time_out)
        return True if (response.status_code == 200 and response.text == 'true') else False
    except requests.exceptions.RequestException: 1
    except Exception: pass

def control(proxy, proxy_type):
    global proxy_errors, token_errors
    token_data = get_token(proxy, proxy_type)
    if token_data == 2: token_errors += 1
    elif token_data == 1: proxy_errors += 1
    elif token_data:
        send_data = send_view(token_data[0], token_data[1], proxy, proxy_type)
        if send_data == 1: proxy_errors += 1


def start_view():
    c, threads = 0, []
    start_scrap()
    for i in [http_proxies, socks4_proxies, socks5_proxies]:
        for j in i:
            thread = Thread(target=control, args=(j, PROXIES_TYPES[c]))
            threads.append(thread)
            while active_count() > THREADS: sleep(0.05)
            thread.start()
        c += 1
        sleep(2)
    for t in threads:
        t.join()
        start_view()


def check_views():
    global real_views
    while True:
        try:
            telegram_request = requests.get(f'https://t.me/{channel}/{post}', params={'embed': '1', 'mode': 'tme'},
                                headers={'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT})
            real_views = search('<span class="tgme_widget_message_views">([^<]+)', telegram_request.text).group(1)
            sleep(2)
        except: pass

def tui():
    while True:
        print(logo)
        print(f'''{B}[ ᴅᴀᴛᴀ ]: {G}{channel.capitalize()}/{post}
{B}[ ʟɪᴠᴇ ᴠɪᴇᴡs ]: {G}{real_views} ✅
 
{S}[ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇʀʀᴏʀs ]: {E}{proxy_errors} 🚫
{S}[ ᴛᴏᴋᴇɴ ᴇʀʀᴏʀs ]: {E}{token_errors} ❌
 
{G}[ ᴛʜʀᴇᴀᴅs ]: {B}{active_count()} ⇝⇝⇝⇝ ''')
        sleep(2);system('cls' if name == 'nt' else 'clear')


def bot_start():
    print("Starting To Check")
    while True:
        seconds = time.time()
        local_time = time.ctime(seconds)
        try:
            CHAT_IDS = int(-1001629184686)
            message = app.get_messages(int(CHAT_IDS),int(169))
            view = message.views
            TEXT = f'''ᴅᴀᴛᴀ :{channel.capitalize()}/{post}
ʟɪᴠᴇ ᴠɪᴇᴡs: {real_views} // {view}✅
 
ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴇʀʀᴏʀs : {proxy_errors} 🚫
ᴛᴏᴋᴇɴ ᴇʀʀᴏʀs : {token_errors} ❌
 
ᴛʜʀᴇᴀᴅs : {active_count()} ⇝⇝⇝⇝ 
Time : {local_time}'''
            appr = random.choice(apps)
            try:
                appr.edit_message_text(chat_id=int(CHAT_ID),message_id=int(6),text=TEXT)
                sleep(7)
            except Exception as e:
                e = f"{e}\n{local_time}"
                appr.edit_message_text(chat_id=int(CHAT_ID),message_id=int(6),text=e)
                sleep(15)
                print(e)
        except Exception as e:
            e = f"{e}\n{local_time}"
            try:
                appr.edit_message_text(chat_id=int(CHAT_ID),message_id=int(6),text=e)
            except Exception as e:
                print(e)
            sleep(5)



async def fuck():
    try:
        search('<span class="tgme_widget_message_views">([^<]+)', requests.get(f'https://t.me/{channel}/{post}',
        params={'embed': '1', 'mode': 'tme'}, headers={'referer': f'https://t.me/{channel}/{post}', 'user-agent': USER_AGENT}).text).group(1)
    except: print(f'{E}[×] Error | Channel Or Post Not Found!');sleep(3);exit()
    else:
        print(f'[√]sᴛᴀʀᴛᴇᴅ | ᴡᴀɪᴛ ғᴇᴡ sᴇᴄᴏɴᴅs ᴛᴏ ʀᴜɴ ᴛʜʀᴇᴀᴅs')
        Thread(target=start_view).start()
        Thread(target=check_views).start()
        print("Application Started")
    wapp = web.AppRunner(await web_server())
    await wapp.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(wapp, "0.0.0.0", 5000).start()
    await idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fuck())
    loop.run_until_complete(bot_start())
