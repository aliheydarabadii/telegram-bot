from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler


print("hello")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name} {update.effective_user.id}')


async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("فیلم", callback_data='1'),
         InlineKeyboardButton("سریال", callback_data='2')]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Please choose:', reply_markup=reply_markup)


async def movie(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hello {update.effective_user.first_name} {update.effective_user.id}')



app = ApplicationBuilder().token("2019821043:AAEgjiZnRAnUWerheUfGglcAIwM6NVINcsQ").build()

app.add_handler(CommandHandler("hello", hello))



app.add_handler(CommandHandler('start', start))

app.add_handler(CommandHandler('1', movie))

app.run_polling()
