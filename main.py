import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai
from PIL import Image

TELEGRAM_BOT_TOKEN = "9090861810:AAFIH4OOY7-KA2Z0de9riyS1CaDXuFEXy4s"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

SYSTEM_PROMPT = """
You are an elite SSC CGL Quant & Reasoning mentor.
For every question given:
1. Highlight the fastest exam-hall approach first (Ratio method, Value-putting, Digital Sum, Option-Elimination, or Deviation). Target: Under 30 seconds.
2. Give a clean, step-by-step breakdown in easy Hindi-English (Hinglish).
3. If applicable, mention the conventional concept briefly so fundamentals stay clear.
Do not waste words with generic greetings; go straight to the solution.
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "नमस्ते! SSC का कोई भी सवाल (फोटो या टेक्स्ट) भेजो, मैं उसका सबसे छोटा तरीका निकाल कर दूँगा।")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "⚡ सवाल प्रोसेस हो रहा है, सबसे छोटा तरीका निकाल रहा हूँ...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("temp_q.jpg", 'wb') as f:
            f.write(downloaded_file)
        
        img = Image.open("temp_q.jpg")
        response = ai_model.generate_content([SYSTEM_PROMPT, img])
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"त्रुटि: {e}")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        response = ai_model.generate_content(f"{SYSTEM_PROMPT}\n\nQuestion: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"त्रुटि: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    bot.infinity_polling()
    
