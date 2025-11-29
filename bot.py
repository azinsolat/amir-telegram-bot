from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import os
import re
import tempfile
import shutil
from yt_dlp import YoutubeDL
import asyncio
import urllib.parse
import urllib.request
import requests


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🗨 شروع چت معمولی":
        context.user_data["chat_enabled"] = True
        await update.message.reply_text("چت فعال شد! 😊 هرچی دوست داری بنویس 🌸")
        return

    elif text == "📸 دانلود اینستاگرام":
        await update.message.reply_text("لینک پروفایل یا پست اینستاگرام رو بفرست 📎")
        return

    elif text == "⚙️ کمک و راهنما":
        await update.message.reply_text(
            "راهنما:\n\n"
            "🗨 شروع چت معمولی → فعال‌کردن گفتگو با ربات\n"
            "📸 دانلود اینستاگرام → دانلود عکس پروفایل/پست\n"
            "⚙️ کمک و راهنما → همین صفحه\n"
        )
        return


# ================== تنظیم توکن‌ها ==================

TOKEN = os.environ["TELEGRAM_TOKEN"]
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@amirbeautybot")

# توکن‌ها و شناسه‌ی Apify
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID")  


# ================== دستورات ساده ==================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or ""

    # کیبورد دکمه‌ها
    keyboard = [
        ["🗨 شروع چت معمولی"],
        ["📸 دانلود اینستاگرام"],
        ["⚙️ کمک و راهنما"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=False
    )

    # در شروع، چت معمولی قفل است
    context.user_data["chat_enabled"] = False

    await update.message.reply_text(
        f"💜 سلام {name} عزیز\n"
        "به ربات امیر خوش اومدی 😈\n\n"
        "یکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام کاربر عزیز من ربات امیر هستم.\n"
        "برای شروع می‌تونی روی دکمه «🗨 شروع چت معمولی» کلیک کنی تا باهم گپ بزنیم 😁\n"
        "وقتی روی دکمه «📸 دانلود اینستاگرام» کلیک کنی، من منتظر می‌مونم برام لینک ویدیویی "
        "یا لینک پست/پروفایل اینستاگرام رو بفرستی تا برات دانلود کنم."
    )


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("این یک دستور سفارشی هست")


async def amir_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "امیر صاحب این رباته 😎\n"
        "اهل مانگا و گیم و مسخره‌بازی با دوستاش 😂"
    )


# ================== چت معمولی ==================

def handle_response(text: str, last_reply=None):
    if not text:
        return "یه حرفی بزن یه چیزی بگوو😞"

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

    return random.choice([
        "داداش نمیفهمم چی میگی بدو برو به کارات برس وقت مام نگیر ",
        "کس نگو برو پی کارت",
        "متوجه نمیشم برو بعدا بیا که حال داشته باشم"
    ])


# ================== توابع اینستاگرام / Apify ==================

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


def fetch_instagram_profile_via_apify(profile_url: str) -> tuple[str, dict]:
    """
    پروفایل اینستاگرام را با استفاده از Apify می‌خواند
    و عکس پروفایل را دانلود می‌کند.
    """

    if not APIFY_TOKEN or not APIFY_ACTOR_ID:
        raise RuntimeError("APIFY_TOKEN یا APIFY_ACTOR_ID تنظیم نشده است.")

    api_url = (
        f"https://api.apify.com/v2/acts/{APIFY_ACTOR_ID}/run-sync-get-dataset-items"
        f"?token={APIFY_TOKEN}"
    )

    payload = {
        "directUrls": [profile_url],
        "resultsType": "details",
        "resultsLimit": 1,
        "scrapeProfilePicture": True,
        "downloadImages": True,
    }

    resp = requests.post(api_url, json=payload, timeout=60)
    resp.raise_for_status()

    items = resp.json()
    if not items:
        raise ValueError("Apify هیچ اطلاعاتی برنگرداند.")

    data = items[0]

    # ---- اطلاعات پروفایل ----
    username = data.get("username")
    full_name = data.get("fullName")
    biography = data.get("biography")
    followers = data.get("followersCount")
    following = data.get("followsCount")
    posts = data.get("postsCount")
    is_private = data.get("private")
    external_urls = data.get("externalUrls") or []
    website = external_urls[0] if external_urls else None

    # ---- عکس پروفایل ----
    profile_pic_url = data.get("profilePicUrlHD") or data.get("profilePicUrl")

    if not profile_pic_url:
        raise ValueError("لینک عکس پروفایل پیدا نشد.")

    # ---- دانلود عکس ----
    temp_dir = tempfile.mkdtemp(prefix="amirbot_igprofile_")

    parsed = urllib.parse.urlparse(profile_pic_url)
    ext = os.path.splitext(parsed.path)[1] or ".jpg"
    file_path = os.path.join(temp_dir, f"profile{ext}")

    with urllib.request.urlopen(profile_pic_url) as r, open(file_path, "wb") as out:
        out.write(r.read())

    meta = {
        "username": username,
        "full_name": full_name,
        "biography": biography,
        "followers": followers,
        "following": following,
        "posts": posts,
        "is_private": is_private,
        "website": website,
    }

    return file_path, meta


# ================== دانلود ویدیو / پست ==================

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

    caption = info.get("description") or ""

    return file_path, caption


# ================== هندل پیام‌ها ==================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    message = update.message
    text = message.text
    chat_type = message.chat.type

    # اگر چت فعال نیست (و پیام، دکمه نیست) راهنما بده
    if not context.user_data.get("chat_enabled"):
        await message.reply_text(
            "برای شروع چت معمولی، دکمه 🗨 شروع چت معمولی رو بزن.\nیا /help"
        )
        return

    print(f"user: {message.chat.id}, chat type: {chat_type}, text: {text}")

    # --- چک کردن اینکه پیام لینک دارد یا نه ---
    url_match = re.search(r'(https?://\S+)', text)
    if url_match:
        url = url_match.group(1)

        # --- ۱) اگر لینکِ پروفایل اینستاگرام بود → Apify ---
        if is_instagram_profile_url(url):
            await message.reply_text("صبر کن دارم اطلاعات پیج رو از Apify می‌گیرم... ⏳")

            try:
                loop = asyncio.get_running_loop()
                file_path, meta = await loop.run_in_executor(
                    None, fetch_instagram_profile_via_apify, url
                )

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
                        await message.reply_photo(f, caption=caption)
                finally:
                    folder = os.path.dirname(file_path)
                    shutil.rmtree(folder, ignore_errors=True)

            except Exception as e:
                print("apify ig profile error:", e)
                await message.reply_text(
                    "نتونستم اطلاعات این پیج رو از Apify بگیرم 😕\n"
                    "ممکنه Actor درست تنظیم نشده باشه یا محدودیت درخواست خورده باشی."
                )

            return

        # --- ۲) اگر لینک پست ویدیو از IG/YT/TikTok و ... بود ---
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

                caption_parts: list[str] = []

                if remote_caption:
                    caption_parts.append(remote_caption.strip())

                if not caption_parts:
                    caption_parts.append("اینم فایل دانلود شده ✅")

                caption_parts.append(BOT_USERNAME)

                caption = "\n\n".join(caption_parts)

                if len(caption) > 1000:
                    caption = caption[:1000] + "…"

                try:
                    with open(file_path, "rb") as f:
                        await message.reply_document(f, caption=caption)
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

    # --- اگر لینک نبود، برگرد به رفتار چت معمولی قبلی ---

    if chat_type in ("group", "supergroup"):
        text_lower = text.lower()
        if BOT_USERNAME.lower() in text_lower:
            t = text_lower.replace(BOT_USERNAME.lower(), "").strip()
            response = handle_response(t)
        else:
            return
    else:
        last = context.user_data.get("last_reply")
        response = handle_response(text, last)

    context.user_data["last_reply"] = response
    await message.reply_text(response)


# ================== لاگ ارورها ==================

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update:{update} cause error:{context.error}')


# ================== اجرای برنامه ==================

if __name__ == "__main__":
    print("bot is starting")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("amir", amir_command))

    # هندل دکمه‌ها
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("^(🗨 شروع چت معمولی|📸 دانلود اینستاگرام|⚙️ کمک و راهنما)$"),
        handle_buttons
    ))

    # هندل پیام‌های متنی معمولی
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    print("polling")
    app.run_polling()


