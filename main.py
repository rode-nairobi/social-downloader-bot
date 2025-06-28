import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler,
    filters, CallbackQueryHandler
)
from downloader import download_media
from admin_panel import is_admin, handle_admin_command
from utils import register_user

BOT_TOKEN = os.getenv("8108336418:AAEUlAy4boFdK1ZO9rvEWQ5p92pOLoKLmrc")
ADMIN_IDS = set(int(x) for x in os.getenv("7823200871", "").split(","))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await register_user(update)
    keyboard = [
        [InlineKeyboardButton("📥 أرسل رابط التحميل", switch_inline_query_current_chat="")],
    ]
    await update.message.reply_text("أهلاً بك! أرسل لي رابط من مواقع التواصل لأبدأ التحميل.", 
                                    reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if text.startswith("/admin") and is_admin(user_id, ADMIN_IDS):
        await handle_admin_command(update, context)
        return

    # حاول تحميل الرابط
    await download_media(update, context, text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # يمكن هنا إضافة أزرار تفاعلية للوحة الأدمن أو خيارات أخرى لاحقاً

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
