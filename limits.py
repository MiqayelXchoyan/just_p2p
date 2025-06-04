import time
import json
import os

LIMITS_FILE = "limits.json"
PREMIUM_FILE = "premium.json"


ADMIN_ID = {YOU TELEGRAM ID }

if os.path.exists(LIMITS_FILE):
    with open(LIMITS_FILE, "r") as f:
        user_limits = json.load(f)
        user_limits = {int(k): v for k, v in user_limits.items()}
else:
    user_limits = {}

if os.path.exists(PREMIUM_FILE):
    with open(PREMIUM_FILE, "r") as f:
        premium_users = set(json.load(f))
else:
    premium_users = set()

MAX_REQUESTS_PER_DAY = 3

def save_limits():
    with open(LIMITS_FILE, "w") as f:
        json.dump(user_limits, f)

def save_premium():
    with open(PREMIUM_FILE, "w") as f:
        json.dump(list(premium_users), f)

def is_premium(user_id: int) -> bool:
    return user_id in premium_users

def add_premium(user_id: int):
    premium_users.add(user_id)
    save_premium()

def remove_premium(user_id: int):
    premium_users.discard(user_id)
    save_premium()

def can_access(user_id: int) -> bool:
    # ✅ Безлимит для админов
    if user_id in ADMIN_ID:
        return True

    if is_premium(user_id):
        return True

    now = int(time.time())
    day = 86400

    if user_id not in user_limits:
        user_limits[user_id] = [1, now]
        save_limits()
        return True

    count, last_reset = user_limits[user_id]

    if now - last_reset > day:
        user_limits[user_id] = [1, now]
        save_limits()
        return True

    if count < MAX_REQUESTS_PER_DAY:
        user_limits[user_id][0] += 1
        save_limits()
        return True

    return False
