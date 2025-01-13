#name - KanBot
#user - KanTrainingBot
#API token - 7898382293:AAHPegX5CCa6JJP_kojyMd2DdWOWYnZSKWQ

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = '7898382293:AAHPegX5CCa6JJP_kojyMd2DdWOWYnZSKWQ'
bot = Bot(api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button_calc = KeyboardButton(text = 'Рассчитать')
button_info = KeyboardButton(text = 'Информация')

kb.row(button_calc, button_info)
#kb.add(button_info)
#kb.insert(button_info)

@dp.message_handler(text = ['Информация'])
async def info(message):
    await message.answer('Привет! Я могу рассчитать суточную норму калорий ')

@dp.message_handler(text = ['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    norma = int(data['weight']) * 10 + int(data['growth']) * 6.25 - int(data['age']) * 5 + 5
    await message.answer(f'Ваша норма калорий {norma}')
    await state.finish()

@dp.message_handler(text = ['Привет', 'Hello'])
async def all_message(message):
    await message.answer('Привет-привет!')

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью. Выберите действие',
                         reply_markup = kb)

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
