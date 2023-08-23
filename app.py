import asyncio


async def on_startup(dp):

    from utils.notify_admins import on_startup_notify
    from utils.set_bot_commands import set_default_commands
    from handlers.users import sender
    await set_default_commands(dp)
    await on_startup_notify(dp)
    
    # Создаем и запускаем задание для sender.send_message_to_user()
    asyncio.create_task(sender.action_at_noon())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    # Запускаем бот в основном потоке
    executor.start_polling(dp, on_startup=on_startup)
