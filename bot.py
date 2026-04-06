import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
conversation_history = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_message = update.message.text

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="Bạn là trợ lý AI hữu ích. Trả lời bằng tiếng Việt.",
        messages=conversation_history[user_id]
    )

    assistant_reply = response.content[0].text

    conversation_history[user_id].append({
        "role": "assistant",
        "content": assistant_reply
    })

    await update.message.reply_text(assistant_reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot đang chạy...")
app.run_polling()