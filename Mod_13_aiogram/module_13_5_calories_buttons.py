# Необходимо сделать цепочку обработки состояний для нахождения нормы калорий для человека, внедрив кнопки в бот.


from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

# получение api-ключа
with open('../api.txt', 'r', encoding='utf-8') as file_api:
    api = file_api.read()

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton(text='Информация')
btn2 = KeyboardButton(text='Рассчитать')
kb.row(btn1, btn2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()
    activity = State()


@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст (полных лет):')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_gender(message, state):
    await state.update_data(age=message.text)
    await message.answer('Ваш пол (1 - мужской, 2 - женский):')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_growth(message, state):
    await state.update_data(gender=message.text)
    await message.answer('Введите свой рост (в см.):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (в кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_activity(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Какая у вас степень физической активности?\n'
                         '(1 - минимальная, 2 - слабая, 3 - средняя, 4 - высокая, 5 - экста)')
    await UserState.activity.set()


@dp.message_handler(state=UserState.activity)
async def send_calories(message, state):
    await state.update_data(activity=message.text)
    data = await state.get_data()
    data = {k: int(v) for k, v in data.items()}
    activity_ratio = [1.2, 1.375, 1.55, 1.725, 1.9][data['activity'] - 1]
    gender_ratio = (-161 if data['gender'] == 2 else 5)
    calories = (10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + gender_ratio) * activity_ratio
    await message.answer(f'Ваша суточная норма калорий: {int(calories)}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий вашему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать работу с ботом.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
