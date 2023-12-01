from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


print("hello")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name} {update.effective_user.id}')


app = ApplicationBuilder().token("2019821043:AAEgjiZnRAnUWerheUfGglcAIwM6NVINcsQ").build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()
