import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Клавиатура с кнопками
keyboard = [
    ["🎲 Кинуть D5"],
    ["🎲 Кинуть D12"],
    ["🎲 Кинуть 2D12"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎲 Привет! Я бот для бросков кубиков.\n"
        "Нажимай на кнопки внизу или пиши команду, например: 2d12\n",
        reply_markup=reply_markup
    )

# ========== ГЛАВНЫЙ ОБРАБОТЧИК С ЛОГАМИ ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ===== ВРЕМЕННЫЙ ЛОГ =====
    if update.message:
        logging.info(f"🔍 ПОЛУЧЕНО: {update.message.text} | из чата ID: {update.message.chat_id} | тип: {update.message.chat.type}")
    else:
        logging.info("🔍 Получен апдейт без сообщения")
    # ===== КОНЕЦ ЛОГА =====
    
    if not update.message:
        return
    
    text = update.message.text
    chat_id = update.message.chat_id

    try:
        # 1. Кнопки
        if text == "🎲 Кинуть D5":
            result = random.randint(1, 5)
            await context.bot.send_message(chat_id=chat_id, text=f"🎲 **D5:** {result}", parse_mode='Markdown')
            
        elif text == "🎲 Кинуть D12":
            result = random.randint(1, 12)
            await context.bot.send_message(chat_id=chat_id, text=f"🎲 **D12:** {result}", parse_mode='Markdown')
            
        elif text == "🎲 Кинуть 2D12":
            results = [random.randint(1, 12) for _ in range(2)]
            total = sum(results)
            await context.bot.send_message(chat_id=chat_id, text=f"🎲 **2D12:** {results}\nСумма: {total}", parse_mode='Markdown')

        # 2. Команды с d
        elif "d" in text.lower():
            try:
                clean_text = text.lower().replace("/roll", "").strip()
                count, sides = map(int, clean_text.split('d'))
                
                if count > 10:
                    await context.bot.send_message(chat_id=chat_id, text="❌ Нельзя кидать больше 10 кубиков за раз!")
                    return
                    
                results = [random.randint(1, sides) for _ in range(count)]
                total = sum(results)
                await context.bot.send_message(chat_id=chat_id, text=f"🎲 Результат ({count}d{sides}): {results}\nСумма: {total}")
                
            except:
                await context.bot.send_message(chat_id=chat_id, text="❌ Не понял. Напиши, например: 2d12 или нажми кнопку.")

        else:
            await context.bot.send_message(chat_id=chat_id, text="Я понимаю только кнопки или команды с d (например, 2d6). Нажми /start чтобы посмотреть меню.")
            
    except Exception as e:
        logging.error(f"❌ Ошибка отправки в чат {chat_id}: {e}")
        await context.bot.send_message(chat_id=chat_id, text="❌ Ошибка! Проверьте, есть ли у бота права администратора в этом чате.")

# Обработчик команды /roll
async def roll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_message(update, context)

# ========== ЗАПУСК ==========
if __name__ == '__main__':
    # ⚠️ ВСТАВЬТЕ СВОЙ ТОКЕН
    TOKEN = '8681984974:AAEB8qh_zXRS3aQ9roH1bFyojzvITWXzHUw'
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('roll', roll_command))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("✅ Бот запущен! Смотри логи в Render.")
    application.run_polling()