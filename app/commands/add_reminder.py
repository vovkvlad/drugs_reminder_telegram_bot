import re
from telegram import ParseMode
from telegram.ext import Filters, MessageHandler, CommandHandler, ConversationHandler

# top level states
DRUG_NAME, REMINDER_CONFIG_TYPE, CONFIG_SUCCESS = map(chr, range(3))

# interactive reminder setup states
MONTH, DATE, DAY_OF_THE_WEEK, TIME, START_DATE, ABORT_INTERACTIVE = map(chr, range(3, 9))

# cron reminder setup steps
ENTERED_CRON_CONFIG = map(chr, range(9, 10))

ALLOWED_MONTHS_SHORTCUTS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
ALLOWED_WEEKDAYS_SHORTCUTS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


def add_reminder(update, context):
    update.message.reply_text('Please, enter the name of the prescribed drug:')
    return DRUG_NAME


def drug_name(update, context):
    drug_name = update.message.text
    context.chat_data['drug_name'] = drug_name
    text = """Gotcha! Now I need to know when do you need to take that drug. \n
    - to start interactive mode - send me <i>/interactive</i> message \n
    - or can specify cron-like scheduler by hitting <i>/cron</i> command (<a href="https://en.wikipedia.org/wiki/Cron">Read about cron format</a>) \n """
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
    return REMINDER_CONFIG_TYPE


def config_success(update, context):
    update.message.reply_text(
        text='Your reminder has been added successfully. You can review all your reminders with <i>/listallreminders</i>',
        parse_mode=ParseMode.HTML)

    return ConversationHandler.END


def cacnel(update, context):
    update.message.reply_text('Cancelling addition of reminder')
    return ConversationHandler.END


def cron_command_handler(update, context):
    update.message.reply_text('CRON')
    return ConversationHandler.END


def interactive_command_handler(update, context):
    text = f"""Do yo need to take medicine on specific month or every month ? \n
     - type months names separated by comma. (E.g. <code>{','.join(ALLOWED_MONTHS_SHORTCUTS)}</code>) \n
     - or type "every" if you need to take it every month"""
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
    return MONTH


def month_selected(update, context):
    selected_month = update.message.text.lower()

    if selected_month == 'every':
        month_scheduler_value = '*'
    elif selected_month in ALLOWED_MONTHS_SHORTCUTS:
        month_scheduler_value = selected_month
    else:
        update.message.reply_text('You have entered month in the wrong format. Please, try again.')
        return MONTH

    context.chat_data['month'] = month_scheduler_value
    reply_text = """Do you want to take medicine on specific dates of the month, or not? \n
     - type dates (<code>1-31</code>) separated by commas
     - or type "every" if it doesn't matter
    """
    update.message.reply_text(text=reply_text, parse_mode=ParseMode.HTML)
    return DATE


def date_selected(update, context):
    selected_date = update.message.text.lower()

    if selected_date == 'every':
        date_scheduler_value = '*'
    else:
        try:
            int_date = int(selected_date)
        except ValueError:
            int_date = -1

        if int_date > 31 or int_date < 1:
            update.message.reply_text('You have entered date in the wrong format. Please, try again.')
            return DATE
        else:
            date_scheduler_value = int_date

    context.chat_data['date'] = date_scheduler_value
    text = f"""Do you want to take medicine on specific day of the week? \n
     - enter weekdays separated by comma (<code>{','.join(ALLOWED_WEEKDAYS_SHORTCUTS)}</code>)
     - or enter every if it doesn't matter 
    """
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
    return DAY_OF_THE_WEEK


def day_of_the_week_selected(update, context):
    selected_weekday = update.message.text.lower()

    if selected_weekday == 'every':
        weekday_scheduler_value = '*'
    elif selected_weekday in ALLOWED_WEEKDAYS_SHORTCUTS:
        weekday_scheduler_value = selected_weekday
    else:
        update.message.reply_text('You have entered weekday in the wrong format. Please, try again.')
        return DAY_OF_THE_WEEK

    context.chat_data['weekday'] = weekday_scheduler_value
    text = """Enter time at which I need to remind you to take drugs. Format is HH:MM (E.g. 23.47)"""
    update.message.reply_text(text=text)
    return TIME


def time_selected(update, context):
    time_pattern = re.compile('^(0[0-9]|1[0-9]|2[0-3]|[1-9]):[0-5][0-9]$')
    selected_time = update.message.text

    if time_pattern.match(selected_time) is None:
        update.message.reply_text('You have entered time in the wrong format. Please, try again.')
        return TIME
    else:
        context.chat_data['hour'] = selected_time[:2]
        context.chat_data['minutes'] = selected_time[3:5]
        text = """At which date do you want to start reminder? \n
         - type date in format <code>YYYY-MM-DD</code> (e.g. 2025-05-12)
         - or type "-" to start reminder in the nearest configured time
        """
        update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
        return START_DATE


def start_date_selected(update, context):
    selected_start_date = update.message.text.lower()

    # TODO add validation later
    if selected_start_date == '-':
        start_date_scheduler_value = None
    else:
        start_date_scheduler_value = selected_start_date

    context.chat_data['start_date'] = start_date_scheduler_value
    text = """At which date do you want to stop reminder? \n
             - type date in format <code>YYYY-MM-DD</code> (e.g. 2025-05-12)
             - or type "-" to start reminder in the nearest configured time
            """
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
    return END_DATE


def stop_date_selected(update, context):
    selected_stop_date = update.message.text.lower()
    # TODO add validation later
    if selected_stop_date == '-':
        stop_date_scheduler_value = None
    else:
        stop_date_scheduler_value = selected_stop_date

    context.chat_data['stop_date'] = stop_date_scheduler_value
    text = """This is what you configured: \n
    [configured value] \n
     - <i>/confirm</i>?
     - <i>/startover</i>?
    """
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def abort_interactive(update, context):
    update.message.reply_text('AAAAAAA')
    return ABORT_INTERACTIVE


cron_config_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('cron', cron_command_handler)],
    states={},
    fallbacks=[],
    map_to_parent={
        ConversationHandler.END: CONFIG_SUCCESS,
    }
)

interactive_config_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('interactive', interactive_command_handler)],
    states={
        MONTH: [MessageHandler(Filters.text & ~Filters.command, month_selected)],
        DATE: [MessageHandler(Filters.text & ~Filters.command, date_selected)],
        DAY_OF_THE_WEEK: [MessageHandler(Filters.text & ~Filters.command, day_of_the_week_selected)],
        TIME: [MessageHandler(Filters.text & ~Filters.command, time_selected)],
        START_DATE: [MessageHandler(Filters.text & ~Filters.command, start_date_selected)],
    },
    fallbacks=[CommandHandler('abort', abort_interactive)],
    map_to_parent={
        ConversationHandler.END: CONFIG_SUCCESS,
        ABORT_INTERACTIVE: DRUG_NAME,
    }
)

add_reminder_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('addreminder', add_reminder)],
    states={
        DRUG_NAME: [MessageHandler(Filters.text & ~Filters.command, drug_name)],
        REMINDER_CONFIG_TYPE: [cron_config_conversation_handler, interactive_config_conversation_handler],
        CONFIG_SUCCESS: [MessageHandler(Filters.text & ~Filters.command, config_success)]
        # REMINDER_CONFIG_TYPE: [MessageHandler(Filters.text & ~Filters.command, reminder_config_type)],
        # INTERACTIVE_CONFIGURATION: [MessageHandler(Filters.text & ~Filters.command, interactive_config)],
    },
    fallbacks=[CommandHandler('cancel', cacnel)]
)
