from loader import dp, bot
import asyncio
from utils.db_api import db_commands as commands
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram import types
from datetime import datetime, timezone


async def send_message(user_id):
    try:
        settings_bot = commands.get_settings()
        settings_bot = list(settings_bot)
        settings_bot = settings_bot[0]

        questionnaire_message = []
        questionnaires = commands.select_all_active_questionnaires_to_sender()
        questionnaires = list(questionnaires)

        current_time = datetime.now(timezone.utc)

        for questionnaire in questionnaires:
            start_time = questionnaire[2].astimezone(timezone.utc)
            end_time = questionnaire[3].astimezone(timezone.utc)
            if questionnaire[-5] and start_time <= current_time <= end_time:
                if questionnaire[-4] is None or commands.all_answers_match(questionnaire[0], str(user_id), questionnaire[-4]):
                    questionnaire_text = f"\n\nАнкета: {questionnaire[0]}"
                    questionnaire_message.append(questionnaire_text)

        if questionnaire_message:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(KeyboardButton('Перевірити'))
            keyboard.add(KeyboardButton('Не зараз'))
            await bot.send_message(chat_id=str(user_id), text=f"Анкет для проходження доступно: {len(questionnaire_message)} ", reply_markup=keyboard)
            print(f"Повідомлення відправлено користувачу з ID: {user_id}")
        else:
            print(f"Немає активних опитувань для користувача з ID: {user_id}")
    except Exception as e:
        print(f"Помилка при відправлені користувачу з ID: {user_id}")
        print(str(e))


async def send_message_to_user():
    while True:
        settings_bot = list(commands.get_settings())[0]
        user_data = {}
        user_in_db = commands.select_all_users()
        if user_in_db:
            user_in_db = [user[3] for user in user_in_db]

            questionnaires = commands.select_all_active_questionnaires_to_sender()
            questionnaires = list(questionnaires)
            answers = commands.select_all_answers_to_sender()
            answers = list(answers)

            current_time = datetime.now(timezone.utc)

            for questionnaire in questionnaires:
                start_time = questionnaire[2].astimezone(timezone.utc)
                end_time = questionnaire[3].astimezone(timezone.utc)
                if questionnaire[-5] and start_time <= current_time <= end_time:
                    for user in user_in_db:
                        if questionnaire[-4] is None or commands.all_answers_match(questionnaire[0], str(user), questionnaire[-4]):
                            user_id = commands.select_user(user)
                            if user_id not in user_data:
                                user_data[user] = []

                            user_answered_questionnaires = set(answer[-2] for answer in answers if str(commands.select_user_to_id(answer[-3])[0]) == str(user))
                            if questionnaire[0] not in user_answered_questionnaires:
                                user_data[user].append(questionnaire[0])

            for user_id, questionnaires in user_data.items():
                if questionnaires:
                    await send_message(user_id)

        await asyncio.sleep(settings_bot[22]*60)  # Задержка в 30 минут (1800 секунд)



@dp.message_handler(text='Перевірити')
async def start_question(message: types.Message, state: FSMContext):
    # await quiz_start(message.from_user.id, message, state)
    await message.answer('Sender')

@dp.message_handler(text='Не зараз')
async def end_question(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = ReplyKeyboardRemove()
    await message.answer('Будемо очікувати', reply_markup=keyboard)