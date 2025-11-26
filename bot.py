from telegram import Update
from telegram.ext import Application,CommandHandler,MessageHandler,filters,ContextTypes
import random
import os

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

    return "داداش نمیفهمم چی میگی بدو برو به کارات برس وقت مام نگیر "





async def handle_massage(update:Update , context:ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
             return
        message = update.message
        text = message.text
        chat_type = message.chat.type


        print(f"user : {message.chat.id} , chat type:{chat_type},text :{text}")

        if chat_type in ("group" , "supergroup"):
             if(BOT_USERNAME in text.lower()):
                  t=text.replace(BOT_USERNAME , '').strip()
                  respose = handle_response(t)

             else:
               return

        else:
             last = context.user_data.get("last_reply")
             respose = handle_response(text, last)


        context.user_data["last_reply"] = respose


        await message.reply_text(respose)




async def error(update:Update , context:ContextTypes.DEFAULT_TYPE):
     print(f'update:{update} cause error:{context.error}')


if __name__ == "__main__":
     print("bot is starting")
     app= Application.builder().token(TOKEN).build()

     app.add_handler(CommandHandler("start",start_command))
     app.add_handler(CommandHandler("help",help_command))
     app.add_handler(CommandHandler("custom",custom_command))
     app.add_handler(CommandHandler("amir", amir_command))


     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND , handle_massage))
     app.add_error_handler(error)

     print("polling")

     app.run_polling(poll_interval=3)

