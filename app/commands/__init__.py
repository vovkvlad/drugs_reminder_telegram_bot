from collections import namedtuple
from app.commands.start import start

CommandHandlerConfig = namedtuple('CommandHandlerConfig', ['command_name', 'handler'])

COMMANDS_HANDLERS = [
    CommandHandlerConfig(command_name='start', handler=start)
]