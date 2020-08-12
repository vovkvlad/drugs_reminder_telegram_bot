from telegram.ext import Filters, MessageHandler, CommandHandler, ConversationHandler

DRUG_NAME, REMINDER_CONFIG = range(2)


def add_reminder(update, context):
    update.message.reply_text('Please, enter the name of the prescribed drug:')
    return DRUG_NAME


def drug_name(update, context):
    drug_name = update.message.text
    update.message.reply_text(f'Gotcha! Now let me know when dou you need to take {drug_name} and how often?')
    return REMINDER_CONFIG


def reminder_config(update, context):
    reminder_config = update.message.text
    update.message.reply_text(f'Got it, you need to take it {reminder_config}. Will notify you soon!')
    return ConversationHandler.END

def cacnel(update, context):
    update.message.reply_text('Cancelling addition of reminder')
    return ConversationHandler.END


add_reminder_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('addreminder', add_reminder)],
    states={
        DRUG_NAME: [MessageHandler(Filters.text & ~Filters.command, drug_name)],
        REMINDER_CONFIG: [MessageHandler(Filters.text & ~Filters.command, reminder_config)]
    },
    fallbacks=[CommandHandler('cancel', cacnel)]
)
