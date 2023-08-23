from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram import types
from loader import dp, bot

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer('Hello')