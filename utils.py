import os
from telegram.ext import Update

# ملف لتسجيل المستخدمين
USERS_FILE = "users.txt"

async def register_user(update: Update):
    user_id = update.message.from_user.id
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write("")
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")
