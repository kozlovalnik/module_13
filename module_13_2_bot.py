#name - KanBot
#user - KanTrainingBot
#API token - 7898382293:AAHPegX5CCa6JJP_kojyMd2DdWOWYnZSKWQ

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = '7898382293:AAHPegX5CCa6JJP_kojyMd2DdWOWYnZSKWQ'
bot = Bot(api)
dp = Dispatcher(bot, storage=MemoryStorage())


#@dp.message_handler(text = ['Привет', 'Hello'])
#async def all_message(message):
#    print(f'Нас приветствуют: {message.text}')

@dp.message_handler(commands = ['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')

@dp.message_handler()
async def all_message(message):
    print('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
