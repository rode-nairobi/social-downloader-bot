from telegram import Update
from telegram.ext import ContextTypes

# قائمة محظورين
banned_users = set()
admins = set()

def is_admin(user_id, admin_ids):
    return user_id in admin_ids

async def handle_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    user_id = update.message.from_user.id

    if msg.startswith("/admin ban"):
        try:
            target_id = int(msg.split()[2])
            banned_users.add(target_id)
            await update.message.reply_text(f"تم حظر المستخدم {target_id}")
        except:
            await update.message.reply_text("خطأ في صيغة الأمر. استخدم: /admin ban <user_id>")

    elif msg.startswith("/admin unban"):
        try:
            target_id = int(msg.split()[2])
            if target_id in banned_users:
                banned_users.remove(target_id)
                await update.message.reply_text(f"تم رفع الحظر عن المستخدم {target_id}")
            else:
                await update.message.reply_text("المستخدم غير محظور.")
        except:
            await update.message.reply_text("خطأ في صيغة الأمر. استخدم: /admin unban <user_id>")

    elif msg.startswith("/admin stats"):
        await update.message.reply_text(f"عدد المحظورين: {len(banned_users)}")

    elif msg.startswith("/admin broadcast"):
        text = msg[len("/admin broadcast "):]
        # هنا يمكنك تنفيذ بث الرسائل لكل المستخدمين (يجب إضافة قائمة المستخدمين المسجلين)

        await update.message.reply_text("تم إرسال الرسالة لجميع المستخدمين (غير مفعّل حالياً).")

    else:
        await update.message.reply_text("أمر إداري غير معروف.")
