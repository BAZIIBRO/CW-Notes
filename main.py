import json
import tgcrypto
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import User, Message
import os
import requests
bot = Client(
    "Careerwill",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

@bot.on_message(filters.command(["start"]))
async def start(bot, update):
       await update.reply_text("Hi i can download **PDFs/NOTEs** from **Careerwill.**\n\n"
                              "**NOW:-** "
                                       
                                       "Press **/login** to continue..\n\n"
                                     "Bot made by **Unknown ~ Kai84**" )

url="https://elearn.crwilladmin.com/api/v1/"

info= {
 "deviceType":"android",
    "password":"",
    "deviceModel":"Asus ASUS_X00TD",
    "deviceVersion":"Pie(Android 9.0)",
    "email":"",
}

@bot.on_message(filters.command(["login"])& ~filters.edited)
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "Send **ID & Password** in this manner otherwise bot will not respond.\n\nSend like this:-  **ID*Password**"
    )

    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text
    info["email"] = raw_text.split("*")[0]
    info["password"] = raw_text.split("*")[1]
    await input1.delete(True)

    login_response=requests.post(url+"login-other",info)
    token=login_response.json( )["data"]["token"]
    await editable.edit("**login Successful**")
    await editable.edit("**You have these Batches :-\n\nBatch ID : Batcch Name**")
    
    
    url1 = requests.get("https://elearn.crwilladmin.com/api/v1/comp/my-batch?&token="+token)
    b_data = url1.json()['data']['batchData']
    for data in b_data:
        aa=f"```{data['id']}```  :  **{data['batchName']}\n**"
        await m.reply_text(aa)
    editable1= await m.reply_text("**Now send the Batch ID to Download PDFs**")
    input2 = message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    
    await input2.delete(True)

    url2=requests.get("https://elearn.crwilladmin.com/api/v1/comp/batch-notes/"+raw_text2+"?topicid="+raw_text2+"&token="+token)
    k=url2.json()["data"]["notesDetails"]
    bb = len(url2.json()["data"]["notesDetails"])
    ss = f"Total PDFs Found in Batch id **{raw_text2}** is - **{bb}** "
    await editable1.edit (ss)
    k.reverse()
    for data in k:
        name=(data["docTitle"])
        s=str(data["docUrl"]) 
        ka = await download(s)
        await m.reply_document(ka, caption=s)
        
async def download(url):
    ka = url.split("/")[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(ka, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return ka
bot.run()
