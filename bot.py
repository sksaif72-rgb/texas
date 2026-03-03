# bot.py
# كود بسيط ومختبر لتشغيل بوت تيليجرام على Railway أو Render أو أي منصة مشابهة

import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# إعداد الـ logging عشان تشوف الأخطاء بسهولة في الـ console / logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# جيب التوكن من الـ Environment Variables (أفضل وأأمن طريقة)
# في Railway: Settings → Environment Variables → أضف Key: TOKEN   Value: توكنك
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logger.error("التوكن مو موجود! أضفه في Environment Variables باسم TOKEN")
    raise ValueError("TOKEN is not set in environment variables!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    الدالة اللي تشتغل لما المستخدم يكتب /start
    """
    user = update.effective_user
    await update.message.reply_text(
        f"مرحبا {user.first_name}! البوت شغال تمام ✓\n"
        "اكتب أي شي تبي تجربة..."
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    يرد على أي رسالة نصية عادية بنفس النص (للتجربة)
    """
    await update.message.reply_text(
        f"قلت: {update.message.text}\n\nحلو، البوت يسمعك 😄"
    )


def main() -> None:
    """ الدالة الرئيسية لتشغيل البوت """
    logger.info("جاري تشغيل البوت...")

    # بناء التطبيق (الطريقة الصحيحة في v20+ و v21+ و v22)
    application = Application.builder().token(TOKEN).build()

    # إضافة الأوامر / handlers
    application.add_handler(CommandHandler("start", start))

    # رد على أي نص عادي (اختياري - للتجربة)
    from telegram.ext import MessageHandler, filters
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )

    # تشغيل البوت بطريقة Polling (مناسبة لـ Railway / Render)
    logger.info("البوت بدأ يشتغل بالـ polling...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,   # يتجاهل الرسائل القديمة لو كان البوت مطفي
    )


if __name__ == "__main__":
    main()
