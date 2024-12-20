import os
from datetime import datetime
from config import LOG_PATH

def log_event(user_id, message):
    os.makedirs(LOG_PATH, exist_ok=True)
    log_file = os.path.join(LOG_PATH, f"{datetime.now().date()}.log")
    with open(log_file, "a") as file:
        file.write(f"[{datetime.now()}] ID: {user_id}, {message}\n")
