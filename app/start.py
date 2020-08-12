import os
import logging
from telegram.ext import Updater

from app.commands import COMMANDS_HANDLERS


def start_drugs_reminder_jobs():
    bot_token = os.getenv('BOT_TOKEN')
    logging.debug('Telegram bot token: %s', bot_token)

    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher

    logging.info('Registering command handlers...')
    register_commands_callbacks(dispatcher=dispatcher)

    updater.start_polling()


def register_commands_callbacks(dispatcher):
    for handler_config in COMMANDS_HANDLERS:
        logging.debug('Adding handler for command: "%s"', handler_config.handler_name)
        dispatcher.add_handler(handler_config.handler_instance)
        logging.debug('Handler for "%s" registered', handler_config.handler_instance)