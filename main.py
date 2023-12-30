import asyncio
import time
import importlib
from pyrogram import *
from pyrogram.types import *
from pyrogram.errors import *
import pyromod
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aiohttp import web
routes = web.RouteTableDef()

API_ID = "15037283"
API_HASH = "7af9d761267bf6b81ed07f942d87127f"
BOT_TOKEN = "5170036823:AAFBCCvPBUAnI0EnNDlbrLMtSb2sxJtijPg"

smtp_server = "smtp-relay.sendinblue.com"
smtp_port = 587
smtp_username = "starkpentester@outlook.com"
smtp_password = "TSrsabGHXhv5npwK"

bot = Client("Stark",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)

def extract_domain(email):
    parts = email.split('@')
    if len(parts) == 2:
        return parts[1]
    else:
        return None

def send_email(frommail,tomail,subject,body):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = frommail
        msg["To"] = tomail
        msg["Subject"] = subject
        bodys = MIMEText(body)
        msg.attach(bodys)
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(frommail, tomail, msg.as_string())
        return True
    except Exception as e:
        print(e)
        return False


@bot.on_message(filters.command(["start","new"]) & filters.private)
async def new(client,message):
    POLICY = """
TOS & PP

This Bot is just for educational Purpose only.
We are not responsible for any illegal Usage or damage by using this bot.
By using this bot you are agreeing to these terms.
"""
    await message.reply(POLICY)
    email = await message.chat.ask('**Send me your anonymous email name:**', parse_mode=enums.ParseMode.MARKDOWN)
    data = extract_domain(email.text)
    if data is not None:
        await email.request.edit_text(f"**Email received!**\n`{email.text}`")
    else:
        return await message.reply("Invalid Email Recived\nPlease try again by /new")
    frommail = email.text
    toemail = await message.chat.ask('**Send me your reciver email name:**', parse_mode=enums.ParseMode.MARKDOWN)
    data = extract_domain(toemail.text)
    if data is not None:
        await toemail.request.edit_text(f"**Email received!**\n`{toemail.text}`")
    else:
        return await message.reply("Invalid Email Recived\nPlease try again by /new")
    toemail = toemail.text
    subject = await message.chat.ask('**Send me the subject of your email:**', parse_mode=enums.ParseMode.MARKDOWN)
    await subject.request.edit_text(f"**Subject Recived**\n`{subject.text}`")
    subject = subject.text
    body = await message.chat.ask("Please send me the body of the email", parse_mode=enums.ParseMode.MARKDOWN)
    await body.request.edit_text("Body Recived Successfully")
    text = await message.reply("Sending Data Packs to SMTP Server...")
    body = body.text
    is_sent = send_email(frommail,toemail,subject,body)
    await asyncio.sleep(2)
    if is_sent==True:
        TEXT = f"""
Email Sent Successfully!
Preview of the Email
From Email: {frommail}
To Email: {toemail}
Subject: {subject}
Body: {body}
"""
        await text.edit(TEXT)
    else:
        await text.edit("Unknown Error Occured!")


@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({"status": "running"})

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app



async def start_bot():
    wapp = web.AppRunner(await web_server())
    await wapp.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(wapp, "0.0.0.0", 5000).start()
    await bot.start()
    print("System Started!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
