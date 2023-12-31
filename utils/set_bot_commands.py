from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start Bot"),
            types.BotCommand("help", "Helpful Information"),
            types.BotCommand("currency",'Check Exchange Rates'),
            types.BotCommand("exchange",'Check Exchange Rates')
        ]
    ) 