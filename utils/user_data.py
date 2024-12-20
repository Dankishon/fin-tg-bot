import json
from config import DATA_PATH

# Загружает данные пользователя
def get_user_data(user_id):
    try:
        with open(DATA_PATH, "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
    if str(user_id) not in users:
        users[str(user_id)] = {
            "balance": 1000,
            "log": [],
            "last_bonus_time": "2024-01-01T00:00:00"
        }
    return users[str(user_id)]

# Сохраняет данные пользователя
def save_user_data(user_id, user_data):
    try:
        with open(DATA_PATH, "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
    users[str(user_id)] = user_data
    with open(DATA_PATH, "w") as file:
        json.dump(users, file, indent=4)
