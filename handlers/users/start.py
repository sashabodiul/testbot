from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from utils.db_api import db_commands as commands
from loader import dp

@dp.message_handler(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id

    if not commands.user_exists(user_id):  # Проверка наличия пользователя
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        phone_button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        markup.add(phone_button)
        await message.reply("Пожалуйста, нажмите на кнопку для отправки своего номера телефона.", reply_markup=markup)
    else:
        await message.reply("Вы уже зарегистрированы.", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def process_contact(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    phone = message.contact.phone_number

    if not commands.user_exists(user_id):  # Проверка наличия пользователя
        commands.add_user(telegram_id=user_id, username=username, first_name=first_name, last_name=last_name, phone=phone)
        await message.reply("Спасибо! Ваш номер телефона был сохранен.")
    else:
        await message.reply("Вы уже зарегистрированы.")
