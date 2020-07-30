import os
import logging

def start_drugs_reminder_jobs():
    logging.debug('Telegram bot token: %s', os.getenv('BOT_TOKEN'))
    return 'started'