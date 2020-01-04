#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging, random 
from bs4 import BeautifulSoup

from datetime import time
import sys
import os
import signal

from arsenal_data import *
from work import *
from exam import *

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

alarm_text = ""
updater = None

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Type \'/\' for list of functions')

def remind(update, context):
    """daily reminder"""
    global alarm_text
    context.bot.send_message(chat_id=update.message.chat_id, text='Setting daily notification!')
    t = time(hour=random.randint(10, 16), minute=random.randint(0, 59))
    alarm_text = " ".join(update.message.text.split(" ")[1:])
    context.job_queue.run_daily(remind_alarm, t, days=tuple(range(6)), context=update.message.chat_id)

def remind_alarm(context):
    global alarm_text
    context.bot.send_message(chat_id=context.job.context, text="Reminder for: "+alarm_text)

def nope(update, context):
    """Echo the user message."""
    update.message.reply_text('Not a thing try again')

def error(update, context):
    """Log Errors caused by Updates."""
    global updater
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    global updater
    # Create the Updater and pass it your bot's token.
    updater = Updater("989937583:AAEF17ZzFeU1qT53cOK4errckwRDPPcWeO8", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("arsenal", arsenal))
    dp.add_handler(CommandHandler('remind', remind, pass_job_queue=True))
    dp.add_handler(CommandHandler('work', work))
    dp.add_handler(CommandHandler('rw', remove_work))
    dp.add_handler(CommandHandler('lw', list_work))
    dp.add_handler(CommandHandler('cw', clear_work))
    dp.add_handler(CommandHandler("exam", exam))
    dp.add_handler(CommandHandler('re', remove_exam))
    dp.add_handler(CommandHandler('le', list_exam))
    dp.add_handler(CommandHandler('ce', clear_exam))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, nope))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    print "Started polling..."

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
