import os  # مهم جداً تستورد os

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # يجيب التوكن من متغير البيئة

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
from bs4 import BeautifulSoup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط ريلز إنستقرام 🎬")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com/reel" not in url:
        await update.message.reply_text("❌ هذا مو رابط ريلز إنستقرام")
        return

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        session = requests.Session()
        page = session.post("https://igram.io/i/", data={"url": url}, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        video_tag = soup.find("a", attrs={"class": "btn-download"})

        if video_tag:
            video_url = video_tag["href"]
            await update.message.reply_video(video=video_url)
        else:
            await update.message.reply_text("❌ ما قدرت أجيب الفيديو، يمكن الرابط خاص.")
    except Exception:
        await update.message.reply_text("📛 صار خطأ أثناء التحميل")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 البوت شغّال...")
    app.run_polling()

if __name__ == "__main__":
    main()
