from collections import namedtuple
from telegram.ext import CommandHandler

from app.commands.start import start_command_handler
from app.commands.help import help_command_handler
from app.commands.add_reminder import add_reminder_conversation_handler

HandlerConfig = namedtuple('HandlerConfig', ['handler_name', 'handler_instance'])

COMMANDS_HANDLERS = [
    HandlerConfig(handler_name='start', handler_instance=start_command_handler),
    HandlerConfig(handler_name='help', handler_instance=help_command_handler),
    HandlerConfig(handler_name='addreminder', handler_instance=add_reminder_conversation_handler),
]
