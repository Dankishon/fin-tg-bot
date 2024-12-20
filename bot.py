import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta
from config import BOT_TOKEN, ADMIN_ID
from utils.user_data import get_user_data, save_user_data

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    await update.message.reply_text(
        f'Добро пожаловать! Ваш баланс: {user_data["balance"]} монет.'
    )

# Команда /roulette
async def roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    await update.message.reply_text('Игра началась! Делайте ставки!')

# Команда /log
async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    if not user_data['log']:
        await update.message.reply_text('Нет предыдущих игр.')
    else:
        log_text = "\n".join(user_data['log'][-12:])
        await update.message.reply_text(f'Последние 12 игр:\n{log_text}')

# Команда /bet
async def bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)

    if user_data['balance'] < 1000:
        await update.message.reply_text('Недостаточно средств для минимальной ставки в 1000!')
        return

    try:
        amount = int(context.args[0])
        bet_choice = context.args[1]

        if amount < 1000:
            await update.message.reply_text('Минимальная ставка 1000!')
            return

        if amount > user_data['balance']:
            await update.message.reply_text('Недостаточно средств!')
            return

        user_data['balance'] -= amount
        save_user_data(user_id, user_data)
        await update.message.reply_text(f'Вы поставили {amount} на {bet_choice}. Удачи!')
    except (IndexError, ValueError):
        await update.message.reply_text('Неверный формат ставки. Используйте: /bet <сумма> <ставка>.')

# Команда /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_list = """
📜 Список доступных команд:
- /start: Начать взаимодействие с ботом
- /roulette: Запустить игру
- /log: Просмотреть последние игры
- /bet <сумма> <ставка>: Сделать ставку
- /menu: Показать это меню
    """
    await update.message.reply_text(commands_list)

# Основная функция
def main():
    application = Application.builder().token(BOT_TOKEN).read_timeout(60).connect_timeout(60).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("roulette", roulette))
    application.add_handler(CommandHandler("log", log))
    application.add_handler(CommandHandler("bet", bet))
    application.add_handler(CommandHandler("menu", menu))
    application.run_polling()

if __name__ == "__main__":
    main()
