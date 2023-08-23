import asyncio
import datetime
from loader import dp,bot
from utils.db_api import db_commands
# from utils.misc import collect_currency, parse_exchange_table, collect_exchange_rate
from utils.misc.collect_exchange_rate import get_goverla_data,get_privat24_data,get_monobank_data,get_nbu_data


async def send_notifications():
    users = db_commands.select_users()  # Список пользователей из базы данных
    latest_record = db_commands.get_latest_currency_record()
    if latest_record:
        buy_data = latest_record[0]
        sell_data = latest_record[1]
        created_at = latest_record[2]
        
        message = "Курси валют:\n"
        message += f"Актуальний курс на годину: {created_at.strftime('%d.%m.%y')}\n\n"
        
        currencies = ["usd", "eur", "gbp"]  # List of currencies you're interested in
        
        for currency in currencies:
            message += f"{currency.upper()} - UAH\n"
            message += f"🔴{buy_data['nbu'][currency]:.5f}/🟢{sell_data['nbu'][currency]:.5f} - НБУ\n"
            message += f"🔴{buy_data['Goverla'][currency]:.5f}/🟢{sell_data['Goverla'][currency]:.5f} - Goverla\n"
            message += f"🔴{buy_data['monobank'][currency]:.5f}/🟢{sell_data['monobank'][currency]:.5f} - Monobank\n"
            message += f"🔴{buy_data['privat24'][currency]:.5f}/🟢{sell_data['privat24'][currency]:.5f} - Privatbank\n\n"

        message += "Для отримання більш докладної інформації введіть команду /exchange"
        
        for user_id in users:
            await bot.send_message(chat_id=user_id[0], text=message)
            await asyncio.sleep(1)

        
async def action_at_noon():
    while True:
        current_time = datetime.datetime.now().time()
        target_time = datetime.time(12, 0)  # 12:00 PM

        if current_time >= target_time:
            next_target_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), target_time)
        else:
            next_target_time = datetime.datetime.combine(datetime.date.today(), target_time)

        time_until_target = next_target_time - datetime.datetime.now()

        await asyncio.sleep(time_until_target.total_seconds())

        try:
            goverla_data = get_goverla_data()
        except Exception as e:
            print("Error getting Goverla data:", e)
            goverla_data = []

        try:
            privat24_data = get_privat24_data()
        except Exception as e:
            print("Error getting Privat24 data:", e)
            privat24_data = []

        try:
            monobank_data = get_monobank_data()
        except Exception as e:
            print("Error getting Monobank data:", e)
            monobank_data = []

        try:
            nbu_data = get_nbu_data()
        except Exception as e:
            print("Error getting NBU data:", e)
            nbu_data = []

        # Создание пустых словарей для buy_data и sell_data
        buy_data = {}
        sell_data = {}

        # Добавление данных в buy_data и sell_data, если они не пустые
        if goverla_data:
            buy_data["Goverla"] = {
                "usd": goverla_data[0]['values'][0],
                "eur": goverla_data[1]['values'][0],
                "gbp": goverla_data[2]['values'][0]
            }
            sell_data["Goverla"] = {
                "usd": goverla_data[0]['values'][1],
                "eur": goverla_data[1]['values'][1],
                "gbp": goverla_data[2]['values'][1]
            }

        if privat24_data:
            buy_data["privat24"] = {
                "usd": privat24_data[2]['purchaseRate'],
                "eur": privat24_data[0]['purchaseRate'],
                "gbp": privat24_data[1]['purchaseRate']
            }
            sell_data["privat24"] = {
                "usd": privat24_data[2]['saleRate'],
                "eur": privat24_data[0]['saleRate'],
                "gbp": privat24_data[1]['saleRate']
            }

        if monobank_data:
            buy_data["monobank"] = {
                "usd": monobank_data[0]['rateBuy'],
                "eur": monobank_data[1]['rateBuy'],
                "gbp": monobank_data[2]['rateBuy']
            }
            sell_data["monobank"] = {
                "usd": monobank_data[0]['rateSell'],
                "eur": monobank_data[1]['rateSell'],
                "gbp": monobank_data[2]['rateSell']
            }

        if nbu_data:
            buy_data["nbu"] = {
                "usd": nbu_data[1]['rate'],
                "eur": nbu_data[2]['rate'],
                "gbp": nbu_data[0]['rate']
            }
            sell_data["nbu"] = {
                "usd": nbu_data[1]['rate'],
                "eur": nbu_data[2]['rate'],
                "gbp": nbu_data[0]['rate']
            }
            db_commands.add_currency_record(buy_data, sell_data)
            await send_notifications()
            await asyncio.sleep(86400)    

#для теста отправки по заданому времени
async def action_every_minute():
    while True:
        await send_notifications()
        await asyncio.sleep(60)