
import os
import openai
import signal
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": update.message.text}]
        )
        await update.message.reply_text(response['choices'][0]['message']['content'])
    except Exception as e:
        await update.message.reply_text(f"⚠️ حدث خطأ: {str(e)}")

async def main():
    app = None
    try:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        print("🟢 البوت يعمل...")
        await app.run_polling(stop_signals=[signal.SIGINT, signal.SIGTERM])
    except asyncio.CancelledError:
        print("⏹️ تم إيقاف البوت بطلب من المستخدم")
    except Exception as e:
        print(f"🔴 خطأ غير متوقع: {e}")
    finally:
        if app:
            try:
                await app.shutdown()
                await app.updater.stop()
            except Exception as e:
                print(f"⚠️ خطأ أثناء الإغلاق: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⏹️ تم إيقاف البرنامج بواسطة المستخدم")
