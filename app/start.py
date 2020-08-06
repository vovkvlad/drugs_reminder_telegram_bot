import os
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler

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
    for commandHandlerConfig in COMMANDS_HANDLERS:
        logging.debug('Adding handler for command: %s', commandHandlerConfig.command_name)
        handler = CommandHandler(commandHandlerConfig.command_name, commandHandlerConfig.handler)
        dispatcher.add_handler(handler)
        logging.debug('Handler for %s registered', commandHandlerConfig.command_name)