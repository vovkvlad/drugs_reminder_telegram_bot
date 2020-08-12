from telegram.ext import CommandHandler

def start(update, context):
    full_name = update.effective_user.full_name
    user_name = update.effective_user.name

    name_to_greet = full_name or user_name

    text = f"Hi {name_to_greet}! " \
           f"I'm a bot designed for reminding you to take your drugs on time! " \
           f"type /help for more info on how to use me"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

start_command_handler = CommandHandler('start', start)