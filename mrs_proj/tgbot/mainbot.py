from telebot.async_telebot import AsyncTeleBot
from decouple import config

dotenv_path = 'mrs_proj/.env'
config.search_path = dotenv_path
BOT_TOKEN = '7073828926:AAH2qZiwFxOw4xvEjTes6G8V---S9Kgf2Kc'

bot = AsyncTeleBot(BOT_TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    await bot.reply_to(message, 'ABOBA')


@bot.message_handler(func=lambda message: True, content_types=['text'])
async def send_message(message):
    await bot.reply_to(message, message.text)
