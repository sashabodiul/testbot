import asyncio
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from utils.db_api import db_commands as commands
from utils.misc import collect_currency, parse_exchange_table
from loader import dp

@dp.message_handler(Command("currency"))
async def bot_help(message: types.Message):
    async def send_currency_message(delay=3):
        loading_message = await message.answer("Данные загружаются...")
        await asyncio.sleep(delay)
        await loading_message.delete()
        
        currency_dict = collect_currency()
        if currency_dict is not None:
            privat24_eur = currency_dict['privat24']['data_0']
            privat24_usd = currency_dict['privat24']['data_1']
            monobank_usd = currency_dict['monobank']['data_0']
            monobank_eur = currency_dict['monobank']['data_1']
            nbu_usd = currency_dict['nbu']['data_24']
            nbu_eur = currency_dict['nbu']['data_31']
            nbu_gbp = currency_dict['nbu']['data_23']

            privat24_gbp = parse_exchange_table("https://banker.ua/bank/privatbank/kurs-valyut/", "exchange-table", "GBP")
            monobank_gbp = parse_exchange_table("https://banker.ua/bank/monobank/kurs-valyut/", "exchange-table", "GBP")

            message_text = (
                "<b>Курси валют: </b>\n\n"
                f"<b>USD:UAH - 💵</b>\n"
                f"🔴<b>{privat24_usd['buy']}</b> 🟢<b>{privat24_usd['sale']}</b> - Privat24\n"
                f"🔴<b>{monobank_usd['rateBuy']}</b> 🟢<b>{monobank_usd['rateSell']}</b> - Monobank\n"
                f"🔴<b>{nbu_usd['rate']}</b> - НБУ\n\n"
                f"<b>EUR:UAH - 💶</b>\n"
                f"🔴<b>{privat24_eur['buy']}</b> 🟢<b>{privat24_eur['sale']}</b> - Privat24\n"
                f"🔴<b>{monobank_eur['rateBuy']}</b> 🟢<b>{monobank_eur['rateSell']}</b> - Monobank\n"
                f"🔴<b>{nbu_eur['rate']}</b> - НБУ\n\n"
                f"<b>GBP:UAH - 💷</b>\n"
                f"🔴<b>{privat24_gbp[0][0]}</b> 🟢<b>{privat24_gbp[0][1]}</b> - Privat24\n"
                f"🔴<b>{monobank_gbp[0][0]}</b> 🟢<b>{monobank_gbp[0][1]}</b> - Monobank\n"
                f"🔴<b>{nbu_gbp['rate']}</b> - НБУ"
            )

            await message.answer(message_text, parse_mode=types.ParseMode.HTML)
        else:
            await message.answer('Наразі недоступно')

    await send_currency_message()
