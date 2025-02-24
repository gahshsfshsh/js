from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json

# Токен вашего бота
TELEGRAM_BOT_TOKEN = "7365430251:AAHnzdIHU-9SwFChbQ2jzct2CjndpFxx2A0"

# ID администратора
ADMIN_CHAT_ID = 1094905671

# URL вашего Web App
WEB_APP_URL = "https://gahshsfshsh.github.io/js/"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Открыть магазин", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Добро пожаловать в наш элитный фермерский магазин!",
        reply_markup=reply_markup
    )

# Обработка данных от Web App
async def web_app_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.web_app_data:
        data = update.effective_message.web_app_data.data
        try:
            order_data = json.loads(data)

            # Формирование сообщения для администратора
            products = "\n".join([f"{name} x {info['quantity']} = {info['quantity'] * info['price']} руб."
                                  for name, info in order_data["products"].items()])
            total_price = order_data.get("total_price", 0)
            address = order_data.get("address", "Не указан")
            phone = order_data.get("phone", "Не указан")
            delivery_time = order_data.get("delivery_time", "Не указан")

            admin_message = (
                f"Новый заказ!\n\n"
                f"Товары:\n{products}\n\n"
                f"Итого: {total_price} руб.\n"
                f"Адрес: {address}\n"
                f"Телефон: {phone}\n"
                f"Время доставки: {delivery_time}\n"
                f"ID пользователя: {update.effective_user.id}"
            )

            # Отправка данных администратору
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)

            # Подтверждение пользователю
            await update.message.reply_text("Ваш заказ успешно оформлен!")
        except json.JSONDecodeError:
            await update.message.reply_text("Произошла ошибка при обработке данных.")
    else:
        await update.message.reply_text("Данные из Web App не были получены.")

# Основная функция
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data_handler))
    application.run_polling()

if __name__ == '__main__':
    main()