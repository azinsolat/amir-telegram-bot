from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
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

# ================== تنظیمات عمومی ==================

TOKEN = os.environ["TELEGRAM_TOKEN"]
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@amirbeautybot")

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID")

MAX_TG_FILE_SIZE = 48 * 1024 * 1024  # حدوداً ۴۸ مگ، کمی کمتر از محدودیت تلگرام


# ================== دکمه‌های اصلی ==================

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🗨 شروع چت معمولی":
        context.user_data["chat_enabled"] = True
        await update.message.reply_text("چت فعال شد! 😊 هرچی دوست داری بنویس 🌸")
        return

    elif text == "📸 دانلود اینستاگرام":
        await update.message.reply_text("لینک پروفایل یا پست اینستاگرام/ویدیو رو بفرست 📎")
        return

    elif text == "⚙️ کمک و راهنما":
        await update.message.reply_text(
            "راهنما:\n\n"
            "🗨 شروع چت معمولی → فعال‌کردن گفتگو با ربات\n"
            "📸 دانلود اینستاگرام → دانلود عکس پروفایل/پست/ویدیو\n"
            "⚙️ کمک و راهنما → همین صفحه\n"
        )
        return


# ================== دستورات ساده ==================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or ""

    keyboard = [
        ["🗨 شروع چت معمولی"],
        ["📸 دانلود اینستاگرام"],
        ["⚙️ کمک و راهنما"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=False
    )

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
            "اوففف 😉",
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


# ================== اینستاگرام / Apify ==================

def is_instagram_profile_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()

    if "instagram.com" not in host:
        return False

    path = parsed.path.strip("/")

    if not path:
        return False

    first = path.split("/")[0]

    if first in ("p", "reel", "tv", "stories"):
        return False

    return True


def fetch_instagram_profile_via_apify(profile_url: str) -> tuple[str, dict]:
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

    username = data.get("username")
    full_name = data.get("fullName")
    biography = data.get("biography")
    followers = data.get("followersCount")
    following = data.get("followsCount")
    posts = data.get("postsCount")
    is_private = data.get("private")
    external_urls = data.get("externalUrls") or []
    website = external_urls[0] if external_urls else None

    profile_pic_url = data.get("profilePicUrlHD") or data.get("profilePicUrl")

    if not profile_pic_url:
        raise ValueError("لینک عکس پروفایل پیدا نشد.")

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


# ================== دانلود عمومی (IG / TikTok / ... ) ==================

def download_media(url: str) -> tuple[str, str | None]:
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


# ================== یوتیوب: گرفتن کیفیت‌ها و دانلود ==================

def get_youtube_quality_options(url: str):
    """
    کیفیت‌های مختلف را از یوتیوب می‌گیرد (چند تا mp3 و چند ارتفاع mp4).
    خروجی: title, options
    هر option: dict(id, label, filesize, is_audio, direct_url)
    """

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    title = info.get("title") or "video"
    formats = info.get("formats") or []

    options = []

    # --- فرمت‌های صوتی ---
    audio_formats = [
        f for f in formats
        if f.get("vcodec") == "none" and f.get("acodec") != "none"
    ]

    def pick_closest(target_kbps):
        best = None
        best_diff = None
        for f in audio_formats:
            abr = f.get("abr")
            if abr is None:
                continue
            diff = abs(abr - target_kbps)
            if best is None or diff < best_diff:
                best = f
                best_diff = diff
        return best

    a190 = pick_closest(190)
    a320 = pick_closest(320)

    for fmt, label_prefix in [(a190, "🎵 190k | mp3"), (a320, "🎵 320k | mp3")]:
        if fmt:
            size = fmt.get("filesize") or fmt.get("filesize_approx")
            size_mb = size / (1024 * 1024) if size else None
            label = label_prefix
            if size_mb:
                label += f", {size_mb:.1f} MB"

            options.append({
                "id": fmt["format_id"],
                "label": label,
                "filesize": size,
                "is_audio": True,
                "direct_url": fmt.get("url"),
            })

    # --- فرمت‌های ویدیویی mp4 با ارتفاع‌های مختلف ---
    target_heights = [144, 240, 360, 480, 720, 1080]

    for h in target_heights:
        best = None
        best_diff = None
        for f in formats:
            if f.get("vcodec") == "none":
                continue
            if f.get("ext") != "mp4":
                continue
            height = f.get("height")
            if not height:
                continue
            diff = abs(height - h)
            if best is None or diff < best_diff:
                best = f
                best_diff = diff

        if best:
            size = best.get("filesize") or best.get("filesize_approx")
            size_mb = size / (1024 * 1024) if size else None

            label = f"🎬 {h}p | mp4"
            if size_mb:
                label += f", {size_mb:.1f} MB"

            options.append({
                "id": best["format_id"],
                "label": label,
                "filesize": size,
                "is_audio": False,
                "direct_url": best.get("url"),
            })

    return title, options


def download_specific_format(url: str, format_id: str, is_audio: bool) -> tuple[str, str]:
    """
    یک format_id مشخص را دانلود می‌کند (همان کیفیت انتخاب‌شده).
    اگر is_audio=True باشد، فقط صدا است؛ ولی ما همان فرمت اصلی را نگه می‌داریم.
    """
    temp_dir = tempfile.mkdtemp(prefix="amirbot_dl_")

    ydl_opts = {
        "outtmpl": f"{temp_dir}/%(title)s.%(ext)s",
        "format": format_id,
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

    print(f"user: {message.chat.id}, chat type: {chat_type}, text: {text}")

    # --- اگر پیام لینک داشت ---
    url_match = re.search(r'(https?://\S+)', text)
    if url_match:
        url = url_match.group(1)

        # ۱) پروفایل اینستاگرام → Apify
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

        # ۲) لینک یوتیوب → نمایش گزینه‌های کیفیت
        if "youtube.com" in url or "youtu.be" in url:
            await message.reply_text("دارم کیفیت‌های موجود رو می‌گیرم... ⏳")
            loop = asyncio.get_running_loop()
            try:
                title, options = await loop.run_in_executor(
                    None, get_youtube_quality_options, url
                )
                if not options:
                    await message.reply_text("کیفیت مناسبی پیدا نکردم 😕")
                    return

                # ذخیره برای callback
                context.user_data["yt_url"] = url
                context.user_data["yt_options"] = {opt["id"]: opt for opt in options}

                buttons = []
                row = []
                for opt in options:
                    row.append(InlineKeyboardButton(
                        opt["label"],
                        callback_data=f"yt|{opt['id']}"
                    ))
                    if len(row) == 2:
                        buttons.append(row)
                        row = []
                if row:
                    buttons.append(row)

                reply_markup = InlineKeyboardMarkup(buttons)

                await message.reply_text(
                    f"🎥 {title}\n\nیکی از کیفیت‌ها رو انتخاب کن:",
                    reply_markup=reply_markup
                )
            except Exception as e:
                print("get_youtube_quality_options error:", e)
                await message.reply_text("نتونستم کیفیت‌ها رو بگیرم 😕")
            return

        # ۳) سایر لینک‌های ویدیو (IG پست، TikTok، X، …) → دانلود ساده
        if any(domain in url for domain in (
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

    # ----- از این‌جا به بعد، اگر لینک نبود → چت معمولی -----

    if not context.user_data.get("chat_enabled"):
        await message.reply_text(
            "برای شروع چت معمولی، دکمه 🗨 شروع چت معمولی رو بزن.\nیا /help"
        )
        return

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


# ================== Callback انتخاب کیفیت یوتیوب ==================
async def handle_youtube_quality_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    if not data.startswith("yt|"):
        return

    format_id = data.split("|", 1)[1]

    yt_url = context.user_data.get("yt_url")
    options_dict = context.user_data.get("yt_options") or {}
    opt = options_dict.get(format_id)

    if not yt_url or not opt:
        await query.edit_message_text("این انتخاب قدیمی شده، دوباره لینک رو بفرست 🙂")
        return

    filesize = opt.get("filesize")
    direct_url = opt.get("direct_url") or yt_url
    is_audio = opt.get("is_audio")

    # ⛔ چک اول: اگر از روی اطلاعات yt_dlp معلومه که خیلی بزرگه
    if filesize and filesize > MAX_TG_FILE_SIZE:
        size_mb = filesize / (1024 * 1024)
        text = (
            f"حجم این فایل حدود {size_mb:.1f} مگابایته و تلگرام اجازه نمی‌ده ربات‌ها همچین فایلی رو مستقیم بفرستن 😅\n\n"
            f"از این لینک می‌تونی مستقیم دانلودش کنی:\n{direct_url}"
        )
        await query.edit_message_text(text)
        return

    # اگر اینجا رسیدیم یعنی یا حجم کمتر از محدوده‌ست، یا حجم دقیق رو نمی‌دونیم
    await query.edit_message_text("دارم فایل رو دانلود می‌کنم... ⏳")

    loop = asyncio.get_running_loop()
    try:
        file_path, caption = await loop.run_in_executor(
            None, download_specific_format, yt_url, format_id, is_audio
        )

        # ✅ چک دوم: بعد از دانلود، حجم واقعی فایل رو هم چک کن
        try:
            real_size = os.path.getsize(file_path)
        except OSError:
            real_size = None

        if real_size and real_size > MAX_TG_FILE_SIZE:
            # فایل رو پاک کن، چون به درد ارسال نمی‌خوره
            folder = os.path.dirname(file_path)
            shutil.rmtree(folder, ignore_errors=True)

            size_mb = real_size / (1024 * 1024)
            text = (
                f"حجم نهایی این فایل حدود {size_mb:.1f} مگابایته و از محدودیت تلگرام بیشتره 😕\n\n"
                f"این لینک مستقیمشه، از اینجا می‌تونی دانلود کنی:\n{direct_url}"
            )
            await query.message.reply_text(text)
            return

        # اگر مشکلی نداشت، فایل رو بفرست
        caption = (caption or "اینم فایل دانلود شده ✅") + f"\n\n{BOT_USERNAME}"

        try:
            with open(file_path, "rb") as f:
                await query.message.reply_document(f, caption=caption)
        finally:
            folder = os.path.dirname(file_path)
            shutil.rmtree(folder, ignore_errors=True)

    except Exception as e:
        print("download_specific_format error:", e)
        await query.message.reply_text("در دانلود فایل مشکلی پیش اومد 😕")


    
       

# ================== لاگ ارورها ==================

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update:{update} cause error:{context.error}")


# ================== اجرای برنامه ==================

if __name__ == "__main__":
    print("bot is starting")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("amir", amir_command))

    # دکمه‌های اصلی
    app.add_handler(MessageHandler(
        filters.TEXT & filters.Regex("^(🗨 شروع چت معمولی|📸 دانلود اینستاگرام|⚙️ کمک و راهنما)$"),
        handle_buttons
    ))

    # Callback انتخاب کیفیت یوتیوب
    app.add_handler(CallbackQueryHandler(handle_youtube_quality_callback))

    # پیام‌های متنی (لینک‌ها + چت معمولی)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    print("polling")
    app.run_polling()

