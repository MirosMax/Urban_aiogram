from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

# получение api-ключа
with open('../api.txt', 'r', encoding='utf-8') as file_api:
    api = file_api.read()

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')
    print('На сообщение "/start" отвечено')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')
    print('Отвечено на любое сообщение пользователя')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
