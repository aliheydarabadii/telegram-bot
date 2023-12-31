from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler,MessageHandler, filters
import os
from open_ai import send_message
my_client_ai={}
print("hello")
client = OpenAI(api_key=os.environ.get('API_KEY'))
my_assistant = client.beta.assistants.retrieve("asst_veUrx3MwQpT6XccwsBKEZDzF")

default_message="""
I want your help to recommend me some movies to watch. You ask me some questions and based on that you recommend movies. Each time you recommend five movies and get feedbacks on that recommendations to make better ones. Please ask questions one by one. Please do not recommend movies that you have recommended again. Please do not recommend movies that the I have seen. You keep recommending until the I like a movie to watch. After asking the questions you think is necessary to ask, please ask whether there is a movie that the user want you to recommend something like that. Please ask the questions in JSON format that has these parts: GPT_Description, Question. Please return the recommendations in JSON format that has these parts :Index, Name, Year, Discerption. Go ahead You:
"""
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
    
    if user_id not in my_client_ai.values():
        my_client_ai[user_id]=client.beta.threads.create()
    # Handle the callback_data
    if query.data == '1':
        response = send_message(default_message,my_client_ai[user_id],client,my_assistant)
    elif query.data == '2':
        response = f"not implemented it"
    else:
        response = f"Unknown option."

    await context.bot.send_message(chat_id=query.message.chat_id, text=response)

async def handle_message(update:Update, context):
    text_received = update.message.text
    thread=my_client_ai[update.message.from_user.id]
    message=send_message(text_received,thread,client,my_assistant)

    # You can add custom logic here to respond based on the text received
    await update.message.reply_text(f'{message}')




app = ApplicationBuilder().token(os.environ.get('BOT_ID')).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))



app.add_handler(CommandHandler('start', start))

app.add_handler(CallbackQueryHandler(button))

app.run_polling()
