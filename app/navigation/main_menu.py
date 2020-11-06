from telegram.ext import CommandHandler, ConversationHandler, CallbackQueryHandler

from app.navigation.add_reminder_buttons import add_reminder_conversation_handler
from app.navigation.common_handlers.start_handler import start_buttons
from app.navigation.common_handlers.help import help_command

# def start(update, context):
#     full_name = update.effective_user.full_name
#     user_name = update.effective_user.name
#
#     name_to_greet = full_name or user_name
#
#     text = f"Hi {name_to_greet}! " \
#            f"I'm a bot designed for reminding you to take your drugs on time! " \
#            f"type /help for more info on how to use me"
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text)

# start_command_handler = CommandHandler('start', start)

main_menu_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start_buttons)],
    states={
        'MAIN_MENU': [
            add_reminder_conversation_handler,
            CallbackQueryHandler(help_command, pattern="^SHOW_HELP_INFO"),
        ]
    },
    fallbacks=[],
)
