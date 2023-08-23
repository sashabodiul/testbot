from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from utils.db_api import db_commands as commands
from loader import dp

@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer('Наразі недоступно')