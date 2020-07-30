import logging
import os
from dotenv import load_dotenv
from app.start import start_drugs_reminder_jobs

load_dotenv(verbose=True)

ENV_LOG_LEVEL = os.getenv('LOG_LEVEL')
LOG_LEVEL = ENV_LOG_LEVEL or logging.INFO
logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    logging.info('Starting drugs reminder bot app')
    start_drugs_reminder_jobs()