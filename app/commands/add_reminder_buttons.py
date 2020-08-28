import re
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)


TOP_LEVEL_STATES = {
    'DRUG_NAME': 'DRUG_NAME',
    'SELECTING_ACTION': 'SELECTING_ACTION',
    'REMINDER_CONFIG_TYPE': 'REMINDER_CONFIG_TYPE',
    'CONFIG_SUCCESS': 'CONFIG_SUCCESS',
}

INTERACTIVE_REMINDER_STATES = {
    'MONTH': 'MONTH',
    'DATE': 'DATE',
    'DAY_OF_THE_WEEK': 'DAY_OF_THE_WEEK',
    'TIME': 'TIME',
    'START_DATE': 'START_DATE',
    'ABORT_INTERACTIVE': 'ABORT_INTERACTIVE',
}

CRON_REMINDER_STATE = {'ENTERED_CRON_CONFIG': 'ENTERED_CRON_CONFIG'}

ALLOWED_MONTHS_SHORTCUTS = [
    'jan',
    'feb',
    'mar',
    'apr',
    'may',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec',
]
ALLOWED_WEEKDAYS_SHORTCUTS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


def get_printable_interactive_config(context):
    interactive_config = context.user_data.get('interactive_config')

    if interactive_config is None:
        text = "You don't configured anything yet"
    else:
        text = "Here is what you've configured so far: \n \n"
        for key in interactive_config:
            text += f"- {key}:  {interactive_config[key]} \n"

    return text


def add_reminder(update, context):
    text = """Okay, let's setup a reminder for your medicine. To do so, please add the name of the medicine and reminder itself"""
    buttons = [
        [
            InlineKeyboardButton(text="Add a name of the drug", callback_data='DRUG_NAME'),
            InlineKeyboardButton(text="Setup a reminder", callback_data='CHOOSE_REMINDER_TYPE'),
        ],
        [
            InlineKeyboardButton(text="Show progress", callback_data='SHOW_CONFIGURED'),
            InlineKeyboardButton(
                text="Abort adding drug reminder", callback_data='ABORT_ADDING_DRUG_REMINDER'
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if update.message:
        update.message.reply_text(text=text, reply_markup=keyboard)
    elif update.callback_query:
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return 'SELECTING_ACTION'


def show_configured(update, context):
    drug_name = context.user_data.get('drug_name')
    cron_config = context.user_data.get('cron_config')
    interactive_config = context.user_data.get('interactive_config')

    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text='Go back', callback_data='GO_BACK_FROM_SHOW_RESULTS')
    )

    text = f"""Here is what you've configured so far: \n
Drug name: {drug_name or 'Not configured'} \n
    """

    if interactive_config is not None:
        interactive_config_text = get_printable_interactive_config(context)
        text += '\n---------Reminder Config---------\n'
        text += interactive_config_text
        text += '\n---------------------------------'
    elif cron_config is not None:
        text += f"Cron config: {cron_config or 'Not configured'}"

    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)


def go_back_from_show_configured(update, context):
    return add_reminder(update, context)


def adding_drug_name(update, context):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text='Okay, tell me:')
    return 'DRUG_ADDED'


def drug_name_added(update, context):
    context.user_data['drug_name'] = update.message.text

    return add_reminder(update, context)


def choose_reminder_type(update, context):
    text = "Now I need to know when do you need to take that drug. You can go user-friendly way with interactive mode or go hardcore with cron syntax."
    buttons = [
        [
            InlineKeyboardButton(text="Interactive mode", callback_data='INTERACTIVE_MODE'),
            InlineKeyboardButton(text="CRON syntax", callback_data='CRON_MODE'),
            InlineKeyboardButton(text="Go Back", callback_data="EXIT_REMINDER_TYPE"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return 'SELECTING_REMINDER_TYPE'


def exit_reminder_type(update, context):
    add_reminder(update, context)

    return ConversationHandler.END


def cron_mode(update, context):
    text = 'Okay, hardcore way it is! Enter cron config:'

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return 'CRON_ADDED'


def cron_reminder_added(update, context):
    context.user_data['cron_config'] = update.message.text

    add_reminder(update, context)
    return ConversationHandler.END


def interactive_reminder_menu(update, context):
    text = (
        'Add required parameters of the reminder \n \n '
        '(To setup reminder for each day for a specific time - just specify time and that would be enough)'
    )
    buttons = [
        [
            InlineKeyboardButton(text="Add Time", callback_data='ADD_TIME'),
            InlineKeyboardButton(text="Add Day of the week", callback_data='ADD_DAY_OF_WEEK'),
            InlineKeyboardButton(text="Add Dates", callback_data='ADD_DATES'),
        ],
        [
            InlineKeyboardButton(text="Add Months", callback_data='ADD_MONTHS'),
            InlineKeyboardButton(text="Add Start Date", callback_data='ADD_START_DATE'),
            InlineKeyboardButton(text="Add End Date", callback_data='ADD_END_DATE'),
        ],
        [
            InlineKeyboardButton(text="Save & Exit", callback_data='SAVE_AND_EXIT_INTERACTIVE'),
            InlineKeyboardButton(text="Show progress", callback_data='SHOW_INTERACTIVE_PROGRESS'),
            InlineKeyboardButton(text="Abort interactive mode", callback_data='CANCEL_INTERACTIVE'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if update.callback_query is None:
        update.message.reply_text(text=text, reply_markup=keyboard)
    else:
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return 'SELECTING_INTERACTIVE_DATA'


def add_interactive_time(update, context):
    text = 'Enter time at which I need to remind you to take drugs. Format is HH:MM (E.g. 23.47)'

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)
    return 'TIME_ADDED'


def time_added(update, context):
    # TODO add validation
    if context.user_data.get('interactive_config') is None:
        context.user_data['interactive_config'] = {}

    context.user_data['interactive_config']['time'] = update.message.text
    return interactive_reminder_menu(update, context)


def add_interactive_weekday(update, context):
    text = f"""Do you want to take medicine on specific day of the week? \n
         - enter weekdays separated by comma (<code>{','.join(ALLOWED_WEEKDAYS_SHORTCUTS)}</code>)
         - or enter every if it doesn't matter 
        """

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.HTML)

    return 'WEEKDAY_ADDED'


def weekday_added(update, context):
    if context.user_data.get('interactive_config') is None:
        context.user_data['interactive_config'] = {}

    context.user_data['interactive_config']['weekday'] = update.message.text
    return interactive_reminder_menu(update, context)


def add_interactive_dates(update, context):
    text = """Do you want to take medicine on specific dates of the month, or not? \n
- type dates (<code>1-31</code>) separated by commas
- or type "every" if it doesn't matter
"""
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.HTML)

    return 'DATES_ADDED'


def dates_added(update, context):
    if context.user_data.get('interactive_config') is None:
        context.user_data['interactive_config'] = {}

    context.user_data['interactive_config']['dates'] = update.message.text
    return interactive_reminder_menu(update, context)


def add_interactive_months(update, context):
    text = f"""Do yo need to take medicine on specific month or every month ? \n
- type months names separated by comma. (E.g. <code>{','.join(ALLOWED_MONTHS_SHORTCUTS)}</code>) \n
- or type "-" if you need to take it every month"""
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.HTML)

    return 'MONTHS_ADDED'


def months_added(update, context):
    if context.user_data.get('interactive_config') is None:
        context.user_data['interactive_config'] = {}

    context.user_data['interactive_config']['months'] = update.message.text
    return interactive_reminder_menu(update, context)


def add_interactive_start_date(update, context):
    text = """At which date do you want to start reminder? \n
- type date in format <code>YYYY-MM-DD</code> (e.g. 2025-05-12)
- or type "-" to start reminder in the nearest configured time"""
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.HTML)

    return 'START_DATED_ADDED'


def start_date_added(update, context):
    if context.user_data.get('interactive_config') is None:
        context.user_data['interactive_config'] = {}

    context.user_data['interactive_config']['start_date'] = update.message.text
    return interactive_reminder_menu(update, context)


def add_interactive_end_date(update, context):
    text = """At which date do you want to stop reminder? \n
- type date in format <code>YYYY-MM-DD</code> (e.g. 2025-05-12)
- or type "-" to start reminder in the nearest configured time"""
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.HTML)

    return 'END_DATE_ADDED'


def end_date_added(update, context):
    if context.user_data.get('interactive_config') is None:
        context.user_data['interactive_config'] = {}

    context.user_data['interactive_config']['end_date'] = update.message.text
    return interactive_reminder_menu(update, context)


def show_interactive_progress(update, context):
    text = get_printable_interactive_config(context)

    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="Go back", callback_data='GO_BACK_FROM_INTERACTIVE_RESULTS')
    )
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)


def go_back_from_interactive_results(update, callback):
    return interactive_reminder_menu(update, callback)


def abort_interactive(update, context):
    if context.user_data.get('interactive_config') is not None:
        context.user_data['interactive_config'] = {}

    choose_reminder_type(update, context)

    return ConversationHandler.END


def save_and_exit_interactive(update, context):
    add_reminder(update, context)

    return 'GO_TO_MAIN_MENU'


selecting_interactive_data_handlers = [
    CallbackQueryHandler(add_interactive_time, pattern='^ADD_TIME$'),
    CallbackQueryHandler(add_interactive_weekday, pattern='^ADD_DAY_OF_WEEK'),
    CallbackQueryHandler(add_interactive_dates, pattern='^ADD_DATES'),
    CallbackQueryHandler(add_interactive_months, pattern='^ADD_MONTHS'),
    CallbackQueryHandler(add_interactive_start_date, pattern='^ADD_START_DATE'),
    CallbackQueryHandler(add_interactive_end_date, pattern='^ADD_END_DATE'),
    CallbackQueryHandler(show_interactive_progress, pattern='^SHOW_INTERACTIVE_PROGRESS'),
    CallbackQueryHandler(
        go_back_from_interactive_results, pattern='^GO_BACK_FROM_INTERACTIVE_RESULTS'
    ),
]

interactive_reminder_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(interactive_reminder_menu, pattern='^INTERACTIVE_MODE$')],
    states={
        'SELECTING_INTERACTIVE_DATA': selecting_interactive_data_handlers,
        'TIME_ADDED': [MessageHandler(Filters.text & ~Filters.command, time_added)],
        'WEEKDAY_ADDED': [MessageHandler(Filters.text & ~Filters.command, weekday_added)],
        'DATES_ADDED': [MessageHandler(Filters.text & ~Filters.command, dates_added)],
        'MONTHS_ADDED': [MessageHandler(Filters.text & ~Filters.command, months_added)],
        'START_DATED_ADDED': [MessageHandler(Filters.text & ~Filters.command, start_date_added)],
        'END_DATE_ADDED': [MessageHandler(Filters.text & ~Filters.command, end_date_added)],
    },
    fallbacks=[
        CallbackQueryHandler(abort_interactive, pattern='^CANCEL_INTERACTIVE$'),
        CallbackQueryHandler(save_and_exit_interactive, pattern='^SAVE_AND_EXIT_INTERACTIVE$'),
    ],
    map_to_parent={
        ConversationHandler.END: 'SELECTING_REMINDER_TYPE',
        'GO_TO_MAIN_MENU': 'SELECTING_ACTION',
    },
)

selecting_reminder_type_handlers = [
    CallbackQueryHandler(cron_mode, pattern='^CRON_MODE$'),
    interactive_reminder_conversation_handler,
]

reminder_type_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(choose_reminder_type, pattern="^CHOOSE_REMINDER_TYPE$")],
    states={
        'SELECTING_REMINDER_TYPE': selecting_reminder_type_handlers,
        'CRON_ADDED': [MessageHandler(Filters.text & ~Filters.command, cron_reminder_added)],
    },
    fallbacks=[CallbackQueryHandler(exit_reminder_type, pattern='^EXIT_REMINDER_TYPE$')],
    map_to_parent={ConversationHandler.END: 'SELECTING_ACTION'},
)

selecting_action_handlers = [
    CallbackQueryHandler(adding_drug_name, pattern="^DRUG_NAME$"),
    CallbackQueryHandler(show_configured, pattern="^SHOW_CONFIGURED$"),
    CallbackQueryHandler(go_back_from_show_configured, pattern="^GO_BACK_FROM_SHOW_RESULTS"),
    reminder_type_conversation_handler,
]

add_reminder_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('addreminder', add_reminder)],
    states={
        'SELECTING_ACTION': selecting_action_handlers,
        'DRUG_ADDED': [MessageHandler(Filters.text & ~Filters.command, drug_name_added)],
    },
    fallbacks=[],
)
