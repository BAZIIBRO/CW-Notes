import json
import aria2p
import subprocess
from pyromod import listen
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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
       await update.reply_text("**HI I AM A POWER FULL BOT I CAN DOWNLOAD PDF/NOTES FROM CAREER WILL**\n\n"
                              "NOW:-"
                                       
                                       "**Press /login to continue**\n\n"
                                     "**Bot made by @MR_ALPHA_SIR1 **" )

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
        "Send **ID & Password** in this manner\notherwise bot will not respond.\n\n:- **ID*Password**:" 
    )
    input: Message = await bot.listen(editable.chat.id, timeout=600)   
    
    raw_text = input.text
    info["email"] = raw_text.split("*")[0]
    info["password"] = raw_text.split("*")[1]
    await input.delete(True)
    
    url="https://elearn.crwilladmin.com/api/v1/"
    login_response=requests.post(url+"login-other",info)

    token=login_response.json( )["data"]["token"]

    get_hdr={
     "token":token,
    }


    await m.reply_text("**login Successful 😝**")
    
    
    
    p=requests.get("https://elearn.crwilladmin.com/api/v1/comp/my-batch?&token="+token)
    topics = json.loads(p.text)
    await m.reply_text(topics)
    q = topics["data"]["batchData"]
    for data in q:    
        aaa=(data["id"])
        aa=("**YOU HAVE THESE BATCHES:-\n\nBatch id : Batch name**\n" + data["id"]) + " : " +str(data["batchName"])  
        await m.reply_text(aa)
    
    await m.reply_text("Now send **Batch id**\nfrom which you want to download **PDFs**")
    for data in q:
     req = requests.get("https://elearn.crwilladmin.com/api/v1/comp/batch-topic/" +str(data["id"]) +"?type=notes&token=" +token)
     resp=req.json()["data"]["batch_topic"]
     input2: Message = await bot.listen(editable.chat.id, timeout=600)   
     await m.reply_text(input2.text)
     raw_text2 = str(input2.text)
     await input2.delete(True)
    
     for dataa in resp:
      z="https://elearn.crwilladmin.com/api/v1/comp/batch-notes/"+str(data["id"])+"?topicid="+str(dataa["id"])+"&token="+token
      await m.reply_text(z)
      f=requests.get(z)
      await m.reply_text(f.text)
    
      try:
        videos = json.loads(f.text)
        x = videos["data"]["notesDetails"]
        await m.reply_text(x)
        tmp_directory_for_each_user = f"./DOWNLOADS/{m.from_user.id}.pdf"
        if not os.path.isdir(tmp_directory_for_each_user):
            os.makedirs(tmp_directory_for_each_user)
        careerewill_pdf = tmp_directory_for_each_user + "/%(title)s.%(ext)s"
        for data in x:
            name=(data["docTitle"])
            s=str(data["docUrl"])    
            await m.reply_text(s)
            
            cmd = ( f" -o './downloads/2110997301/%(id)s.%(ext)s' no-warning '{s}'" )


            Client.send_document(f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'")
            return 0
            
            
      except Exception as e:
        await m.reply_text(str(e))
        
    

bot.run()
