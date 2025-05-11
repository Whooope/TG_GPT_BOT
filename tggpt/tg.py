from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# 🔐 Вставь свои ключи прямо сюда (НЕ ДЕЛАЙ ТАК в публичном коде)


# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот ChatGPT. Напиши что-нибудь.")

# Ответ на сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}]
        )
        reply_text = response.choices[0].message.content.strip()
    except Exception as e:
        reply_text = f"Ошибка GPT: {e}"
    
    await update.message.reply_text(reply_text)

# Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
