import os
import telebot
from google import genai
from PIL import Image

# Keys Setup
TELEGRAM_BOT_TOKEN = "9090861810:AAFIH4OOY7-KA2Z0de9riyS1CaDXuFEXy4s"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

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
    bot.reply_to(message, "नमस्ते! SSC का कोई भी सवाल (फोटो या टेक्स्ट) भेजो, मैं उसका सबसे छोटा और स्मार्ट तरीका निकाल कर दूँगा।")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    status_msg = bot.reply_to(message, "⚡ सवाल देख रहा हूँ, सबसे छोटा तरीका निकाल रहा हूँ...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("temp_q.jpg", 'wb') as f:
            f.write(downloaded_file)
        
        img = Image.open("temp_q.jpg")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[img, SYSTEM_PROMPT]
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"त्रुटि: {e}")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[message.text, SYSTEM_PROMPT]
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"त्रुटि: {e}")

bot.infinity_polling()
