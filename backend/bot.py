import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types.web_app_info import WebAppInfo

# Инициализация бота и диспетчера
bot = Bot(token='7960542844:AAH2nSW1Zq7BH24OnRcgoepI8jX2LQ8e-Gg')
dp = Dispatcher()

# URL вашего веб-приложения
WEB_APP_URL = 'https://testvueproject.vercel.app/'

@dp.message(Command('start'))
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(
                    text='Открыть приложение',
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ],
        resize_keyboard=True
    )
    await message.answer('Привет! Нажми на кнопку, чтобы открыть приложение', reply_markup=keyboard)

@dp.message()
async def handle_web_app_data(message: types.Message):
    try:
        # Проверяем, есть ли данные веб-приложения
        if message.web_app_data:
            # Получаем данные
            data = message.web_app_data.data
            await message.answer(f"Получены данные от веб-приложения: {data}")
        else:
            # Если это обычное сообщение, просто отвечаем
            await message.answer("Используйте кнопку для открытия приложения")
    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке данных: {str(e)}")

# Функция для запуска бота
async def main():
    # Включаем логирование
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())





