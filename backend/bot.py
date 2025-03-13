import asyncio
import aiogram

bot = aiogram.Bot(token='789456123:AAHdqweFJXY789456123')
WEB_APP_URL = 'https://testvueproject.vercel.app/'

@bot.message_handler(commands=['start'])
async def start(message):
    keyboard = aiogram.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(aiogram.types.KeyboardButton(text='Open Web App', web_app=aiogram.types.WebAppInfo(url=WEB_APP_URL)))
    await bot.send_message(message.chat.id, 'Hello, world!', reply_markup=keyboard)





