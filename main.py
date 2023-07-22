import config

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = config.TOKEN  # Токен вашего бота
volunteers = config.volunteers  # id волонтеров

updater = Updater(TOKEN, use_context=True)  # Вот здесь мы создаем экземпляр Updater
dispatcher = updater.dispatcher  # А теперь можем получить dispatcher

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

def request_dialog(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Ваш запрос на диалог принят, {user.mention_markdown_v2()}\. Ожидайте, пока волонтер примет приглашение.',
    )
    try:
        # Здесь можно добавить логику для выбора конкретного волонтера. Сейчас просто берем первого.
        context.bot.send_message(chat_id=volunteers[0], text=f"Пользователь {user.id} хочет начать диалог. Принимаете?")
    except Exception as e:
        print(f"Ошибка при отправке сообщения волонтеру: {e}")


def test(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    try:
        context.bot.send_message(chat_id=user.id, text=f"Это тестовое сообщение от бота.")
    except Exception as e:
        print(f"Ошибка при отправке тестового сообщения: {e}")

test_handler = CommandHandler("test", test)
dispatcher.add_handler(test_handler)


request_handler = CommandHandler("request", request_dialog)
dispatcher.add_handler(request_handler)

updater.start_polling()
