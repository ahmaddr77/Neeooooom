import sqlite3, time, uuid
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = "8343659359:AAHa2vNnm6nx7I-OHvgYLtB9q6s0P-ULqg0"
CHANNEL_ID = -1002855710104
DB = "tokens.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tokens(
                    token TEXT PRIMARY KEY,
                    message_id INTEGER,
                    created INTEGER,
                    expiry INTEGER,
                    used INTEGER DEFAULT 0,
                    user_id INTEGER
                )""")
    conn.commit()
    conn.close()

def post_to_channel(update: Update, context: CallbackContext):
    text = "محتوى دراسي محمي — اضغط الزر للدخول."
    sent = context.bot.send_message(chat_id=CHANNEL_ID, text=text)
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("webappneom", url="https://dainty-platypus-18dc9a.netlify.app/")]]
    )
    context.bot.edit_message_reply_markup(
        chat_id=CHANNEL_ID,
        message_id=sent.message_id,
        reply_markup=keyboard
    )
    update.message.reply_text("✅ تم نشر الرسالة مع الزر webappneom في القناة.")

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer("🌐 الزر يفتح الموقع مباشرة")

def start_polling():
    init_db()
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("post", post_to_channel))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    start_polling()
