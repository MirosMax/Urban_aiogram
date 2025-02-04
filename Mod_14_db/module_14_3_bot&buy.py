from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# получение api-ключа
with open('../api.txt', 'r', encoding='utf-8') as file_api:
    api = file_api.read()

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Основная клавиатура
kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn_info = KeyboardButton(text='Информация')
btn_calculate = KeyboardButton(text='Рассчитать')
btn_buy = KeyboardButton(text='Купить')
kb.row(btn_info, btn_calculate)
kb.row(btn_buy)

# Инлайн клавиатура для расчета каллорий
i_kb_calc = InlineKeyboardMarkup()
i_btn_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
i_btn_formulas = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
i_kb_calc.row(i_btn_calories, i_btn_formulas)

# Инлайн клавиатура для выбора товаров
i_kb_products = InlineKeyboardMarkup()
i_kb_products.row(
    InlineKeyboardButton(text='Витамины 1', callback_data='product_buying'),
    InlineKeyboardButton(text='Витамины 2', callback_data='product_buying'),
    InlineKeyboardButton(text='Витамины 3', callback_data='product_buying'),
    InlineKeyboardButton(text='Витамины 4', callback_data='product_buying')
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()
    activity = State()


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=i_kb_calc)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(
        '''для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A;
для женщин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x A.

A – это уровень активности человека, его различают обычно по пяти степеням физических нагрузок в сутки:

Минимальная активность: A = 1,2.
Слабая активность: A = 1,375.
Средняя активность: A = 1,55.
Высокая активность: A = 1,725.
Экстра-активность: A = 1,9 (под эту категорию обычно подпадают люди, занимающиеся, например, тяжелой атлетикой, или другими силовыми видами спорта с ежедневными тренировками, а также те, кто выполняет тяжелую физическую работу).'''
    )
    await call.answer()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        text_about = f'Название: Витамины {i} | Описание: Витамины из группы {i} | Цена: {i * 100}'
        with open(f'bot_img/product_{i}.jpg', 'rb') as img_file:
            await message.answer_photo(img_file, text_about)
    await message.answer('Выберите продукт для покупки', reply_markup=i_kb_products)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')


# Начало блока хендлеров по расчету каллорий
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст (полных лет):')
    await call.answer()
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


# Конец блока хендлеров по расчету каллорий


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий вашему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать работу с ботом.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
