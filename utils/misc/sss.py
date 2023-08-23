from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from utils.db_api import db_commands as commands
from utils.misc import collect_currency, scrape_table_data, format_table_data
from loader import dp

@dp.message_handler(Command("currency"))
async def bot_help(message: types.Message):
    privatbank_url = 'https://banker.ua/bank/privatbank/kurs-valyut/'
    table_class_privatbank = 'exchange-table'
    privatbank_table_data = scrape_table_data(privatbank_url, table_class_privatbank)

    monobank_url = 'https://banker.ua/bank/monobank/kurs-valyut/'
    table_class_monobank = 'exchange-table'
    monobank_table_data = scrape_table_data(monobank_url, table_class_monobank)

    if privatbank_table_data and monobank_table_data:
        formatted_privatbank_data = format_table_data(privatbank_table_data, "Privat24")
        formatted_monobank_data = format_table_data(monobank_table_data, "Monobank")
        
        print("Курси валют:\n")
        for privat, monobank in zip(formatted_privatbank_data, formatted_monobank_data):
            print(privat)
            print(monobank)
            print()
    currency_dict = collect_currency()
    if currency_dict is not None:
        privat24_eur = currency_dict['privat24']['data_0']
        privat24_usd = currency_dict['privat24']['data_1']
        monobank_usd = currency_dict['monobank']['data_0']
        monobank_eur = currency_dict['monobank']['data_1']
        nbu_usd = currency_dict['nbu']['data_24']
        nbu_eur = currency_dict['nbu']['data_31']
        nbu_gbp = currency_dict['nbu']['data_23']
        
        message_text = (
            "<b>Курси валют:</b>\n\n"
            f"<b>USD:UAH - 💵</b>\n"
            f"🔴<b>{privat24_usd['buy']}</b> 🟢<b>{privat24_usd['sale']}</b> - Privat24\n"
            f"🔴<b>{monobank_usd['rateBuy']}</b> 🟢<b>{monobank_usd['rateSell']}</b> - Monobank\n"
            f"🔴<b>{nbu_usd['rate']}</b> - НБУ\n\n"
            f"<b>EUR:UAH - 💶</b>\n"
            f"🔴<b>{privat24_eur['buy']}</b> 🟢<b>{privat24_eur['sale']}</b> - Privat24\n"
            f"🔴<b>{monobank_eur['rateBuy']}</b> 🟢<b>{monobank_eur['rateSell']}</b> - Monobank\n"
            f"🔴<b>{nbu_eur['rate']}</b> - НБУ\n\n"
            f"<b>GBP:UAH - 💷</b>\n"
            f"🔴<b>{nbu_gbp['rate']}</b> - НБУ"
        )
        
        await message.answer(message_text, parse_mode=types.ParseMode.HTML)
        # Пример использования функции для первой ссылки
    else:
        await message.answer('Наразі недоступно')


bank_urls = [
        "https://banker.ua/bank/monobank/kurs-valyut/",
        "https://banker.ua/bank/privatbank/kurs-valyut/"
    ]
    table_class = "exchange-table"
    target_currency = "GBP"

    for url in bank_urls:
        rows_with_currency = parse_exchange_table(url, table_class, target_currency)
        if rows_with_currency:
            print(f"Результаты с {target_currency} для {url}:")
            for row in rows_with_currency:
                print(row)
        else:
            print(f"На {url} нет данных о {target_currency}.")