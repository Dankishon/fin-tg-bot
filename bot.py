import json
import time
import random
import threading
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from config import BOT_TOKEN, ADMIN_ID, BONUS_INTERVAL, DATA_PATH
from utils.user_data import get_user_data, save_user_data
from utils.logger import log_event

# Команда /start
def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    update.message.reply_text(f"Добро пожаловать! Ваш текущий баланс: {user_data['balance']} монет.")

# Функция рулетки
def рулетка(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id
        user_data = get_user_data(user_id)

        # Проверяем корректность входных данных
        args = context.args
        if len(args) < 2:
            update.message.reply_text('Используйте формат: /рулетка <ставка> <число или цвет>.')
            return

        amount = int(args[0])
        bet = args[1].lower()

        if amount <= 0 or amount > user_data['balance']:
            update.message.reply_text('Неверная сумма ставки.')
            return

        user_data["balance"] -= amount
        update.message.reply_text('Крутится... ждите 10 секунд.')
        time.sleep(10)

        # Генерация результата рулетки
        result = random.randint(0, 12)
        color = 'зеленый' if result == 0 else ('черный' if result % 2 == 0 else 'красный')
        update.message.reply_text(f'Выпало: {result}, цвет: {color}')

        # Рассчитываем выигрыш
        winnings = 0
        if bet.isdigit() and int(bet) == result:
            winnings = amount * 12
        elif '-' in bet:
            start, end = map(int, bet.split('-'))
            if result in range(start, end + 1):
                winnings = amount * (12 / (end - start + 1))
        elif (bet in ['к', 'красный'] and color == 'красный') or (bet in ['ч', 'черный'] and color == 'черный'):
            winnings = amount * 2
        elif bet == '0' and result == 0:
            winnings = amount * 24

        user_data['balance'] += winnings
        save_user_data(user_id, user_data)
        log_event(user_id, f"Ставка: {amount}, Выигрыш: {winnings}, Баланс: {user_data['balance']}")
        update.message.reply_text(f'Ваш выигрыш: {winnings}. Ваш баланс: {user_data["balance"]}')
    except Exception as e:
        update.message.reply_text(f'Произошла ошибка: {e}')

# Автоматическая выдача бонусов
def выдача_бонусов():
    while True:
        now = datetime.now()
        for user_id in list(users.keys()):
            user_data = get_user_data(user_id)
            if now - datetime.fromisoformat(user_data['last_bonus_time']) >= timedelta(hours=BONUS_INTERVAL):
                user_data['balance'] += 10000
                user_data['last_bonus_time'] = now.isoformat()
                save_user_data(user_id, user_data)
                log_event(user_id, "Выдан бонус: 10000")
        time.sleep(3600)

# Основная функция
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("рулетка", рулетка))

    threading.Thread(target=выдача_бонусов, daemon=True).start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
