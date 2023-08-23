import logging

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import banned_users

class BigBro(BaseMiddleware):
    async def on_pre_process_update(self, update:types.Update, data:dict):
        logging.info('!________________New Update___________________!')
        logging.info('Pre process update')
        logging.info('Procces update')
        data["middlewares_data"] = 'Its go to on_post_process_update'
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query: 
            user = update.callback_query.from_user.id
        else:
            return
        
        if user in banned_users:
            raise CancelHandler()
        
    async def on_process_update(self, update:types.Update, data:dict):
        logging.info(f'!______________________Process Update________________________________!\n{data=}')
        logging.info('Pre process msg')

    async def on_pre_process_message(self, message: types.Message, data:dict):
        logging.info(f'!___________________Pre process message________________________________!')
        logging.info('Filters')
        data["middlewares_data"] = "On pre_process_message"

    async def on_process_message(self, message: types.Message, data:dict):
        logging.info(f'!___________Process Message____________!')
        logging.info('Handlers')
        data["middlewares_data"] = 'Handlers'