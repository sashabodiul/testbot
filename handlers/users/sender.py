import asyncio
import datetime
from loader import dp,bot
from utils.db_api import db_commands
from utils.misc import collect_currency, parse_exchange_table


async def send_notifications():
    users = db_commands.select_users()  # Список пользователей из базы данных
    message = "Уведомление о обновлении курсов!"
    
    for user_id in users:
        print(user_id)
        await bot.send_message(chat_id=user_id[0], text=message)  # user_id[0] содержит ID пользователя
        await asyncio.sleep(1)
        

async def action_at_noon():
    current_time = datetime.datetime.now().time()
    target_time = datetime.time(12, 0)  # 12:00 PM

    time_until_target = datetime.datetime.combine(datetime.date.today(), target_time) - datetime.datetime.combine(datetime.date.today(), current_time)
    
    if time_until_target.total_seconds() < 0:
        # Если текущее время уже прошло 12:00 PM, переносим на следующий день
        time_until_target = datetime.timedelta(days=1) - time_until_target

    await asyncio.sleep(time_until_target.total_seconds())
    
    send_notifications()
    

#для теста отправки по заданому времени
async def action_every_minute():
    while True:
        await send_notifications()
        await asyncio.sleep(60)