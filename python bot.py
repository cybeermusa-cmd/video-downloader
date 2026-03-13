import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = os.environ.get("8277002073:AAFxPmOURBARjoEX1f-AFTeJM2YNAxghmDg")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 স্বাগতম!\n\n"
        "আমি Facebook, Instagram ও TikTok ভিডিও ডাউনলোড করতে পারি।\n\n"
        "📌 যেকোনো ভিডিও লিংক পাঠান, আমি ডাউনলোড করে দেব! ✅"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not any(domain in url for domain in [
        "facebook.com", "fb.watch",
        "instagram.com",
        "tiktok.com", "vm.tiktok.com"
    ]):
        await update.message.reply_text("❌ শুধু Facebook, Instagram বা TikTok লিংক পাঠান।")
        return

    msg = await update.message.reply_text("⏳ ডাউনলোড হচ্ছে... একটু অপেক্ষা করুন।")

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
    }

    os.makedirs("downloads", exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await msg.edit_text("✅ ডাউনলোড সম্পন্ন! পাঠাচ্ছি...")

        with open(file_path, "rb") as video_file:
            await update.message.reply_video(video=video_file)

        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ সমস্যা হয়েছে:\n{str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("🤖 বট চালু হয়েছে...")
    app.run_polling()

if __name__ == "__main__":
    main()
