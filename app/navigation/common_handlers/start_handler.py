from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def start_buttons(update, context):
    buttons = [
        [
            InlineKeyboardButton(text="Add a new reminder", callback_data='ADD_NEW_REMINDER'),
            InlineKeyboardButton(
                text="Manage your reminders", callback_data='AAAA'
            ),
        ],
        [InlineKeyboardButton(text="Show help", callback_data='SHOW_HELP_INFO')],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if update.message:
        full_name = update.effective_user.full_name
        user_name = update.effective_user.name

        name_to_greet = full_name or user_name
        text = (
            f"Hi {name_to_greet}! "
            f"I'm a bot designed for reminding you to take your drugs on time! "
            f"type /help for more info on how to use me"
        )
        update.message.reply_text(text=text, reply_markup=keyboard)
    elif update.callback_query:
        text = "Please, choose your action:"
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return 'MAIN_MENU'