from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler,MessageHandler, filters
import os

my_map={}
print("hello")
client = OpenAI(api_key=os.environ.get('API_KEY'))
my_assistant = client.beta.assistants.retrieve("asst_veUrx3MwQpT6XccwsBKEZDzF")


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
    await query.answer()  # This is necessary to stop the loading animation on the button
    user_id = query.from_user.id  # This is necessary to prevent small loading circle on the button
    
    # Handle the callback_data
    if query.data == '1':
        response = f"You selected Option 1.{user_id}"
    elif query.data == '2':
        response = f"You selected Option 2.{user_id}"
    else:
        response = f"Unknown option. {user_id}"

    await context.bot.send_message(chat_id=query.message.chat_id, text=response)

async def handle_message(update, context):
    text_received = update.message.text
    # You can add custom logic here to respond based on the text received
    await update.message.reply_text(f'You said: {text_received}')




app = ApplicationBuilder().token(os.environ.get('BOT_ID')).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))



app.add_handler(CommandHandler('start', start))

app.add_handler(CallbackQueryHandler(button))

app.run_polling()
