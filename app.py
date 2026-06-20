from fastapi import FastAPI, Request, Response
import telebot
import os
import json

# توكن البوت من متغيرات البيئة
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = FastAPI()

# نقطة نهاية الويب هوك
@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])
        return Response(status_code=200)
    except Exception as e:
        return Response(status_code=500, content=str(e))

# نقطة نهاية للتحقق
@app.get("/")
async def home():
    return {"status": "Bot is running!"}

# أوامر البوت
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 مرحباً! أنا بوت بسيط.\n\nالأوامر:\n/start - ترحيب\n/help - مساعدة\n/time - الوقت\n/echo <نص> - تكرار النص")

@bot.message_handler(commands=['time'])
def send_time(message):
    from datetime import datetime
    bot.reply_to(message, f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@bot.message_handler(commands=['echo'])
def echo_message(message):
    text = message.text.replace('/echo', '').strip()
    if text:
        bot.reply_to(message, f"🔊 {text}")
    else:
        bot.reply_to(message, "⚠️ اكتب نصاً بعد /echo")

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    bot.reply_to(message, f"📩 رسالتك: {message.text}")