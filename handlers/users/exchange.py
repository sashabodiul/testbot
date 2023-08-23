from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from utils.db_api import db_commands
import json
from loader import dp


@dp.message_handler(Command("exchange"))
async def exchange(message: types.Message):
    latest_record = db_commands.get_latest_currency_record()

    if latest_record:
        buy_data = latest_record[0]
        sell_data = latest_record[1]
        created_at = latest_record[2]

        formatted_message = "Курси валют:\nАктуальний курс на : {}\n\n".format(created_at.strftime('%d.%m.%y'))

        for currency, rates in buy_data.items():
            formatted_message += "{} - {}\n".format(currency.upper(), get_currency_symbol(currency))
            
            for bank, rate in rates.items():
                formatted_message += "{}{:.4f}/{:.4f} - {}\n".format("🟢" if bank != "nbu" else "🔴", float(rate), float(sell_data[currency][bank]), get_bank_name(bank))
            
            formatted_message += "\n"
        
        await message.answer(formatted_message)
    else:
        await message.answer("No records found.")

def get_currency_symbol(currency):
    symbols = {
        "usd": "💵",
        "eur": "💶",
        "gbp": "💷"
    }
    return symbols.get(currency, currency.upper())

def get_bank_name(bank):
    names = {
        "privat24": "Privat24",
        "monobank": "Monobank",
        "nbu": "НБУ",
        "goverla": "Goverla"  # Add other bank names here
    }
    return names.get(bank, bank.capitalize())
