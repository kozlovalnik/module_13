#name - KanBot
#user - KanTrainingBot
#API token - 7898382293:AAHPegX5CCa6JJP_kojyMd2DdWOWYnZSKWQ

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = '7898382293:AAHPegX5CCa6JJP_kojyMd2DdWOWYnZSKWQ'
bot = Bot(api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

kb = ReplyKeyboardMarkup(resize_keyboard = True, input_field_placeholder = "Выберите действие")
button_calc = KeyboardButton(text = 'Рассчитать')
button_info = KeyboardButton(text = 'Информация')
kb.row(button_calc, button_info)

inline_kb = InlineKeyboardMarkup(resize_keyboard = True)
inline_button_calories = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
inline_button_formulas = InlineKeyboardButton(text = 'Формулы расчета', callback_data = 'formulas')
inline_kb.row(inline_button_calories, inline_button_formulas)

@dp.message_handler(text = ['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup = inline_kb)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('вес * 10 + рост * 6.25 - возраст * 5 + 5')

@dp.message_handler(text = ['Информация'])
async def info(message):
    await message.answer('Привет! Я могу рассчитать суточную норму калорий ')

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
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

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.',
                         reply_markup = kb)

@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)