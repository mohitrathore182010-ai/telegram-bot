from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# User message -> owner ko bhejna
async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id != OWNER_ID:
        sent = await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"UserID:{user.id}\n"
                 f"Name:{user.first_name}\n\n"
                 f"{update.message.text}"
        )

        context.bot_data[sent.message_id] = user.id


# Owner ka reply -> user ko bhejna
async def owner_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == OWNER_ID:

        if update.message.reply_to_message:
            original_msg_id = update.message.reply_to_message.message_id

            if original_msg_id in context.bot_data:
                target_user = context.bot_data[original_msg_id]

                await context.bot.send_message(
                    chat_id=target_user,
                    text=update.message.text
                )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.REPLY,
        user_message
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & filters.REPLY,
        owner_reply
    )
)

print("Bot started...")
app.run_polling()
