from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
import random
import os
import re
import tempfile
import shutil
from yt_dlp import YoutubeDL
import asyncio



TOKEN = os.environ["TELEGRAM_TOKEN"]
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@amirbeautybot")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or ""
    await update.message.reply_text(
        f"💜 سلام {name} عزیز\n"
        "به ربات امیر خوش اومدی 😈"
    )



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "من یک ربات ساده برای شروع هستم.\n\n"
        "دستورات من:\n"
        "/start - شروع ربات\n"
        "/help - راهنما\n"
        "/custom - دستور سفارشی\n\n"
        "همین‌طور به بعضی از نوشته‌های شما هم پاسخ می‌دم 😉"
    )

    
async def custom_command(update:Update , context:ContextTypes.DEFAULT_TYPE):
       await update.message.reply_text("این یک دستور سفارشی هست")



async def amir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "امیر صاحب این رباته 😎\n"
        "اهل مانگا و گیم و مسخره‌بازی با دوستاش 😂"
    )



def handle_response(text: str, last_reply=None):
    if not text:
        return "یه حرفی بزنن یه چیزی بگوو😞"

    user_text = text.lower()

   
    if last_reply and "لب و رد کن بیاد" in last_reply:
        if "باشه" in user_text:
            return "👌🏻👈🏻"

    
    if "hi" in user_text or "سلام" in user_text or "سلام خوشگله" in user_text:
        return random.choice([
            "سلام عزیزم",
            "سلام عشق داداش",
            "سلام زیبای من",
            "سلام دوست داشتنی",
        ])

    if "how are you" in user_text or "چطوری" in user_text or "خوبی" in user_text:
        return random.choice([
            "خوبم خوشگلم تو چطوری؟",
            "میزونه میزونم",
            "قربون داداش تو چطوریی",
        ])

    if (
        "منم خوبم مرسی" in user_text
        or "مرسی" in user_text
        or "قربونت" in user_text
        or "عشق منی" in user_text
        or "خوبم مرسی" in user_text
    ):
        return random.choice([
            "امیر دلش میخواد در این لحظه بگه سیشدییییییر",
            "خوبه خوبه",
            "شکرش",
            "🙄🙄",
            "😙😚",
        ])

    if (
        "دوست دارم داداش" in user_text
        or "عاشقتم" in user_text
        or "میمیرم برات" in user_text
        or "بیا بهت بدم" in user_text
        or "چقد خوشگلی" in user_text
    ):
        return random.choice([
            "لب و رد کن بیاد 🫦😈",
            "جووون منی",
            "اوفففف 😉",
        ])

    if "باشه" in user_text:
        return "اوکییی"

    if "خوشگله پسر" in user_text:
        return "یری سیشدیر"

    if "چخبر" in user_text:
        return "هیچی والا"

    if "چیکارا میکنی" in user_text or "چیکار میکنی" in user_text:
        return "داشتم مانگا میخوندم که مزاحمم شدی😔"

    return random.choice(["داداش نمیفهمم چی میگی بدو برو به کارات برس وقت مام نگیر ","کس نگو برو پی کارت","متوحه نمیشم برو بعدا بیا که حال داشته باشم"]) 





def download_media(url: str) -> str:
    """
    لینک رو می‌گیره، ویدیو/عکس رو دانلود می‌کنه
    و آدرس فایل نهایی رو برمی‌گردونه.
    """
    temp_dir = tempfile.mkdtemp(prefix="amirbot_")

    ydl_opts = {
        "outtmpl": f"{temp_dir}/%(id)s.%(ext)s",
        "format": "mp4/bestaudio/best",
        "noplaylist": True,
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

  
    return file_path





async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message = update.message
    text = message.text
    chat_type = message.chat.type

    print(f"user: {message.chat.id}, chat type: {chat_type}, text: {text}")

 
    url_match = re.search(r'(https?://\S+)', text)

    if url_match:
        url = url_match.group(1)

        if any(domain in url for domain in (
            "youtube.com",
            "youtu.be",
            "instagram.com",
            "tiktok.com",
            "x.com",
            "twitter.com",
        )):
            await message.reply_text("صبر کن دارم لینک رو دانلود می‌کنم... ⏳")

            try:
               
                loop = asyncio.get_running_loop()
                file_path = await loop.run_in_executor(
                    None, download_media, url
                )

                
                try:
                    with open(file_path, "rb") as f:
                        await message.reply_document(
                            f,
                            caption="اینم فایل دانلود شده ✅"
                        )
                finally:
                    folder = os.path.dirname(file_path)
                    shutil.rmtree(folder, ignore_errors=True)

            except Exception as e:
                print("download error:", e)
                await message.reply_text(
                    "نتونستم دانلود کنم 😕\n"
                    "ممکنه لینک مشکل داشته باشه، یا سایت اجازه دانلود نده."
                )

            return

   
        
        
    # گروه / سوپرگروه
    if chat_type in ("group", "supergroup"):
        text_lower = text.lower()
        if BOT_USERNAME in text_lower:
            t = text_lower.replace(BOT_USERNAME, "").strip()
            response = handle_response(t)
        else:
            return
    else:
        # پی‌وی
        last = context.user_data.get("last_reply")
        response = handle_response(text, last)

    context.user_data["last_reply"] = response
    await message.reply_text(response)












async def error(update:Update , context:ContextTypes.DEFAULT_TYPE):
     print(f'update:{update} cause error:{context.error}')


if __name__ == "__main__":
     print("bot is starting")
     app= Application.builder().token(TOKEN).build()

     app.add_handler(CommandHandler("start",start_command))
     app.add_handler(CommandHandler("help",help_command))
     app.add_handler(CommandHandler("custom",custom_command))
     app.add_handler(CommandHandler("amir", amir_command))


     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND , handle_message))
     app.add_error_handler(error)

     print("polling")
     app.run_polling()



