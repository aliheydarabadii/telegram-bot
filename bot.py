from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler

my_map={}
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


async def button(update:Update, context):
    query = update.callback_query
    query.answer()  # This is necessary to stop the loading animation on the button
    user_id = query.from_user.id  # This is necessary to prevent small loading circle on the button
    
    # Handle the callback_data
    if query.data == '1':
        response = f"You selected Option 1.{user_id}"
    elif query.data == '2':
        response = f"You selected Option 2.{user_id}"
    else:
        response = f"Unknown option. {user_id}"

    await context.bot.send_message(chat_id=query.message.chat_id, text=response)




app = ApplicationBuilder().token("2019821043:AAEgjiZnRAnUWerheUfGglcAIwM6NVINcsQ").build()

app.add_handler(CommandHandler("hello", hello))



app.add_handler(CommandHandler('start', start))

app.add_handler(CallbackQueryHandler(button))

app.run_polling()
