import json
import os
from config import DATA_PATH

def get_user_data(user_id):
    """
    Получает данные пользователя по ID. Если данных нет, создаёт запись.
    """
    try:
        if not os.path.exists(DATA_PATH):
            with open(DATA_PATH, "w") as file:
                json.dump({}, file)

        with open(DATA_PATH, "r") as file:
            users = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    if str(user_id) not in users:
        users[str(user_id)] = {
            "balance": 1000000,
            "log": [],
            "last_bonus_time": "1970-01-01T00:00:00",
        }
    return users[str(user_id)]

def save_user_data(user_id, user_data):
    """
    Сохраняет данные пользователя по ID.
    """
    try:
        with open(DATA_PATH, "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    users[str(user_id)] = user_data

    with open(DATA_PATH, "w") as file:
        json.dump(users, file, indent=4)
