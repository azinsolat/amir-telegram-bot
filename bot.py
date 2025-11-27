from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
import random
import os
import re
import tempfile
import shutil
from yt_dlp import YoutubeDL
import asyncio
import urllib.parse
import urllib.request




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

    # 👇 اول منطق «لب و رد کن بیاد» رو چک کن
    if last_reply and "لب و رد کن بیاد" in last_reply:
        if "باشه" in user_text:
            return "👌🏻👈🏻"

    # بقیه‌ی جواب‌ها
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







def is_instagram_profile_url(url: str) -> bool:
    """
    بررسی می‌کند که آیا لینک، لینک پروفایل اینستاگرام است (نه پست/ریل/استوری).
    مثال: https://www.instagram.com/username/
    """
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()

    if "instagram.com" not in host:
        return False

    path = parsed.path.strip("/")

    if not path:
        return False

    # اولین بخش مسیر
    first = path.split("/")[0]

    # اگر /p/ یا /reel/ یا /stories/ بود یعنی پست/استوری است، نه پروفایل
    if first in ("p", "reel", "tv", "stories"):
        return False

    return True







def fetch_instagram_profile(url: str) -> tuple[str, dict]:
    """
    اطلاعات پروفایل اینستاگرام را می‌گیرد و عکس پروفایل را دانلود می‌کند.

    خروجی:
    - مسیر فایل عکس پروفایل
    - دیکشنری اطلاعات پروفایل (پرایوت بودن، تعداد پست، فالوور، فالوینگ، بیو، وبسایت)
    """
    temp_dir = tempfile.mkdtemp(prefix="amirbot_igprofile_")

    ydl_opts = {
        "skip_download": True,   # هیچ پستی را دانلود نکن، فقط اطلاعات را بگیر
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # --- عکس پروفایل ---

    thumb_url = None
    if "thumbnail" in info:
        thumb_url = info["thumbnail"]
    elif "thumbnails" in info and info["thumbnails"]:
        thumb_url = info["thumbnails"][-1].get("url")

    if not thumb_url:
        raise ValueError("نتوانستم عکس پروفایل را پیدا کنم.")

    parsed_thumb = urllib.parse.urlparse(thumb_url)
    ext = os.path.splitext(parsed_thumb.path)[1] or ".jpg"
    file_path = os.path.join(temp_dir, f"profile{ext}")

    with urllib.request.urlopen(thumb_url) as resp, open(file_path, "wb") as out:
        out.write(resp.read())

    # --- اطلاعات پروفایل ---

    meta: dict = {}

    # خیلی از این فیلدها ممکن است وجود نداشته باشند؛ برای همین .get استفاده می‌کنیم
    meta["is_private"] = info.get("is_private")
    meta["posts"] = info.get("n_entries") or info.get("playlist_count")
    meta["followers"] = (
        info.get("channel_follower_count")
        or info.get("followers")
        or info.get("like_count")
    )
    meta["following"] = info.get("following_count")
    meta["biography"] = info.get("description")
    meta["website"] = info.get("channel_url") or info.get("uploader_url")

    return file_path, meta












def download_media(url: str) -> tuple[str, str | None]:
    """
    ویدیو/عکس را دانلود می‌کند و:
    - مسیر فایل
    - کپشن/توضیحات پست (در صورت وجود) را برمی‌گرداند
    """
    temp_dir = tempfile.mkdtemp(prefix="amirbot_")

    ydl_opts = {
        "outtmpl": f"{temp_dir}/%(title)s.%(ext)s",
        "format": "mp4/bestaudio/best",
        "noplaylist": True,
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    # کپشن پست (برای اینستا، تیک‌تاک، یوتیوب و … معمولا این فیلد هست)
    caption = info.get("description") or ""

    return file_path, caption




async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    message = update.message
    text = message.text
    chat_type = message.chat.type

    print(f"user: {message.chat.id}, chat type: {chat_type}, text: {text}")

    # --- چک کردن اینکه پیام لینک دارد یا نه ---
    url_match = re.search(r'(https?://\S+)', text)
    if url_match:
        url = url_match.group(1)

        # --- ۱) اگر لینکِ پروفایل اینستاگرام بود ---
        if is_instagram_profile_url(url):
            await message.reply_text("صبر کن دارم اطلاعات پیج رو می‌گیرم... ⏳")

            try:
                loop = asyncio.get_running_loop()
                file_path, meta = await loop.run_in_executor(
                    None, fetch_instagram_profile, url
                )

                # ساختن متن کپشن
                is_private = meta.get("is_private")
                if is_private is True:
                    priv_text = "🔐 پیج خصوصی"
                elif is_private is False:
                    priv_text = "🔓 پیج عمومی"
                else:
                    priv_text = "ℹ️ وضعیت حریم خصوصی نامشخص"

                def fmt_num(n):
                    if n is None:
                        return "نامشخص"
                    try:
                        return f"{int(n):,}"
                    except Exception:
                        return str(n)

                posts = fmt_num(meta.get("posts"))
                followers = fmt_num(meta.get("followers"))
                following = fmt_num(meta.get("following"))

                bio = meta.get("biography") or "ندارد"
                website = meta.get("website") or "ندارد"

                caption = (
                    f"{priv_text}\n\n"
                    f"🌄 پست ها : {posts}\n"
                    f"👥 فالوور ها : {followers}\n"
                    f"👤 فالوینگ ها : {following}\n"
                    f"📝 بیوگرافی:\n{bio}\n"
                    f"🔗 وبسایت: {website}\n\n"
                    f"{BOT_USERNAME}"
                )

                try:
                    with open(file_path, "rb") as f:
                        # 👇 به صورت photo، نه document
                        await message.reply_photo(
                            f,
                            caption=caption
                        )
                finally:
                    folder = os.path.dirname(file_path)
                    shutil.rmtree(folder, ignore_errors=True)

            except Exception as e:
                print("ig profile error:", e)
                await message.reply_text(
                    "نتونستم اطلاعات این پیج رو بگیرم 😕\n"
                    "ممکنه پیج محدودیت داشته باشه یا اینستاگرام اجازه نده."
                )

            return  # دیگه ادامه نده، چون همین پیام هندل شد

        # --- ۲) اگر لینک پست ویدیو از IG/YT/TikTok و ... بود (همون قبلی) ---
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
                file_path, remote_caption = await loop.run_in_executor(
                    None, download_media, url
                )

            


                # --- ساختن کپشن نهایی ---
                caption_parts: list[str] = []

                # ۱) کپشن خود پست (اینستا/تیک‌تاک/یوتیوب)
                if remote_caption:
                    caption_parts.append(remote_caption.strip())

                # ۲) اگر هیچ کپشنی نبود، یه متن پیش‌فرض بذار
                if not caption_parts:
                    caption_parts.append("اینم فایل دانلود شده ✅")

                # ۳) در انتها آیدی ربات
                caption_parts.append(BOT_USERNAME)

                # چسبوندن همه بخش‌ها با دو خط فاصله
                caption = "\n\n".join(caption_parts)

                # اگر خیلی طولانی شد، یه مقدار کوتاهش کن که از لیمیت تلگرام نزنه بیرون
                if len(caption) > 1000:
                    caption = caption[:1000] + "…"

                # --- ارسال فایل به صورت document ---
                try:
                    with open(file_path, "rb") as f:
                        await message.reply_document(
                            f,
                            caption=caption
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

            return  # چون لینک هندل شد، دیگه لازم نیست ادامه بدیم

    # --- اگر لینک نبود، برگرد به رفتار چت معمولی قبلی ---

    if chat_type in ("group", "supergroup"):
        text_lower = text.lower()
        if BOT_USERNAME in text_lower:
            t = text_lower.replace(BOT_USERNAME, "").strip()
            response = handle_response(t)
        else:
            return
    else:
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


