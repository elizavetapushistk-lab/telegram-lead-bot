import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# --- НАСТРОЙКИ ---
BOT_TOKEN = "7866911476:AAFK9gVdI_JAwCCMyzahh0kkWrtBbTxChEg"
CHANNEL_USERNAME = "@engsiderschool"

# --- ПРОВЕРКА ПОДПИСКИ ---
def check_subscription(update: Update, context: CallbackContext) -> bool:
    try:
        user_id = update.effective_user.id
        chat_member = context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Ошибка проверки подписки: {e}")
        return False

# --- КОМАНДА /START ---
def start_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    if check_subscription(update, context):
        update.message.reply_text(
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

        update.message.reply_text(
            f"Привет, {user.first_name}! 👋\n"
            "Чтобы получить бесплатный урок английского, подпишитесь на наш канал.\n"
            "После подписки нажмите 'Я подписался'.",
            reply_markup=reply_markup
        )

# --- ПРОВЕРКА ПОДПИСКИ ПО КНОПКЕ ---
def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    
    try:
        chat_member = context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        is_subscribed = chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        is_subscribed = False

    if is_subscribed:
        query.edit_message_text(
            "🎉 Спасибо за подписку! Вот ваш бонус:\n\n"
            "🌟 Бесплатный урок английского\n"
            "Смотрите урок по ссылке: https://progressme.ru/sharing-material/a0a88b46-e78c-4e32-8d59-ded129ee5830\n\n"
            "Успехов в изучении английского! 📚"
        )
    else:
        query.edit_message_text(
            "❌ Я не вижу вашу подписку. Убедитесь, что вы подписались на канал, и нажмите 'Я подписался' снова.\n\n"
            "Ссылка на канал: https://t.me/engsiderschool",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔁 Я подписался", callback_data="check_subscription")
            ]])
        )

# --- ЗАПУСК БОТА ---
def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CallbackQueryHandler(button_callback, pattern="^check_subscription$"))
    
    print("Бот запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()