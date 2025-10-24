import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- НАСТРОЙКИ ---
BOT_TOKEN = "7866911476:AAFK9gVdI_JAwCCMyzahh0kkWrtBbTxChEg"
CHANNEL_USERNAME = "@engsiderschool"

# --- ПРОВЕРКА ПОДПИСКИ ---
async def check_subscription(user_id: int, app: Application) -> bool:
    try:
        chat_member = await app.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False

# --- КОМАНДА /START ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id

    is_subscribed = await check_subscription(user_id, context.application)

    if is_subscribed:
        await update.message.reply_text(
            "🎉 Спасибо за подписку! Вот ваш бонус:\n\n"
            "🌟 Бесплатный урок английского\n"
            "Смотрите урок по ссылке: https://progressme.ru/sharing-material/a0a88b46-e78c-4e32-8d59-ded129ee5830\n\n"
            "Успехов в изучении английского! 📚"
        )
    else:
        keyboard = [
            [InlineKeyboardButton("✅ Подписаться на канал", url=f"https://t.me/engsiderschool")],
            [InlineKeyboardButton("🔁 Я подписался", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n"
            "Чтобы получить бесплатный урок английского, подпишитесь на наш канал.\n"
            "После подписки нажмите 'Я подписался'.",
            reply_markup=reply_markup
        )

# --- ПРОВЕРКА ПОДПИСКИ ПО КНОПКЕ ---
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    is_subscribed = await check_subscription(user_id, context.application)

    if is_subscribed:
        await query.edit_message_text(
            "🎉 Спасибо за подписку! Вот ваш бонус:\n\n"
            "🌟 Бесплатный урок английского\n"
            "Смотрите урок по ссылке: https://progressme.ru/sharing-material/a0a88b46-e78c-4e32-8d59-ded129ee5830\n\n"
            "Успехов в изучении английского! 📚"
        )
    else:
        await query.edit_message_text(
            "❌ Я не вижу вашу подписку. Убедитесь, что вы подписались на канал, и нажмите 'Я подписался' снова.\n\n"
            "Ссылка на канал: https://t.me/engsiderschool",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔁 Я подписался", callback_data="check_subscription")
            ]])
        )

# --- ЗАПУСК БОТА ---
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_callback, pattern="^check_subscription$"))
    
    print("Бот запущен! Нажмите Ctrl+C для остановки")
    application.run_polling()

if __name__ == '__main__':
    main()