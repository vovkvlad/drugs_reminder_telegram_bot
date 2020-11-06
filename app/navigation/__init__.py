from collections import namedtuple
from telegram.ext import CommandHandler

from app.navigation.main_menu import main_menu_conversation_handler
from app.navigation.common_handlers.help import help_command
from app.navigation.add_reminder_buttons import add_reminder_conversation_handler

HandlerConfig = namedtuple('HandlerConfig', ['handler_name', 'handler_instance'])

COMMANDS_HANDLERS = [
    HandlerConfig(handler_name='start', handler_instance=main_menu_conversation_handler),
    HandlerConfig(handler_name='help', handler_instance=CommandHandler('help', help_command)),
    HandlerConfig(handler_name='addreminder', handler_instance=add_reminder_conversation_handler),
]
