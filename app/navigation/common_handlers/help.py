from telegram import ParseMode
from telegram.ext import CommandHandler


def help_command(update, context):
    bot_commands = context.bot.commands

    text = """<b>Available navigation:</b> \n \n"""

    for command_config in bot_commands:
        command_name = command_config.command
        command_description = command_config.description
        text += f"""<i>/{command_name}</i>:  {command_description} \n \n"""

    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)