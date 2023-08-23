import asyncio
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from utils.misc.collect_exchange_rate import *
from loader import dp

async def process_exchange(message: types.Message):
    # Вызов функций и вывод результатов
    goverla_data = get_goverla_data()
    print("Goverla Data:")
    print(goverla_data)
    print()

    privat24_data = get_privat24_data()
    print("Privat24 Data:")
    print(privat24_data)
    print()

    monobank_data = get_monobank_data()
    print("Monobank Data:")
    print(monobank_data)
    print()

    nbu_data = get_nbu_data()
    print("NBU Data:")
    print(nbu_data)

@dp.message_handler(Command("exchange"))
async def exchange(message: types.Message):
    await process_exchange(message)
