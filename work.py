from datetime import datetime, time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode

work_bool = False
f = None

def work(update, context):
    """nightly reminder"""
    global work_bool, f
    f = open(str(update.message.from_user.id) + "-work.txt", "a+")
    requested_work = str(" ".join(update.message.text.split(" ")[1:]))
    if len(requested_work.replace(" ", "")) > 0:
        context.bot.send_message(chat_id=update.message.chat_id, text=('Added *' + requested_work + '* to list!'), parse_mode=ParseMode.MARKDOWN)
        f.write(requested_work + "\n")
        if work_bool == False:
            context.job_queue.run_daily(work_alarm, time(hour=19), days=tuple(range(4)), context=update.message.chat_id)
            work_bool = True
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=('Problem adding \"*' + requested_work + '*\" to list!'), parse_mode=ParseMode.MARKDOWN)
    f.close()


def remove_work(update, context):
    """remove nightly reminder"""
    wList = []
    with open(str(update.message.from_user.id) + "-work.txt", "r") as f:
        wList = f.readlines()
    wList = [w.strip("\n") for w in wList]
    print wList
    print " ".join(str(update.message.text).split(" ")[1:])
    removed_item = " ".join(str(update.message.text).split(" ")[1:])
    if removed_item in wList:
        wList.remove(removed_item)
        with open(str(update.message.from_user.id) + "-work.txt", "w") as f:
            for line in wList:
                if line.strip("\n") != removed_item:
                    f.write(line + "\n")
        context.bot.send_message(chat_id=update.message.chat_id, text=('Removed *' + removed_item + '* from list!'), parse_mode=ParseMode.MARKDOWN)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=('Problem removing \"*' + removed_item + '*\" from list!'), parse_mode=ParseMode.MARKDOWN)
    f.close()

def list_work(update, context):
    wList = []
    with open(str(update.message.from_user.id) + "-work.txt", "r+") as f:
        wList = f.readlines()
    if len(wList) != 0:  
        wList = [w.strip("\n") for w in wList]
        work_text = ""
        counter = 1
        for i in wList:
            work_text += "\n    " + str(counter) + ".  " + i
            counter += 1
        context.bot.send_message(chat_id=update.message.chat_id, text=("Here is your work:" + work_text), parse_mode=ParseMode.MARKDOWN)
    else: 
        context.bot.send_message(chat_id=update.message.chat_id, text=("Congrats, You have no work!"), parse_mode=ParseMode.MARKDOWN)
    f.close()

def clear_work(update, context):
    open(str(update.message.from_user.id) + "-work.txt", "w")
    context.bot.send_message(chat_id=update.message.chat_id, text=('Cleared Work!'), parse_mode=ParseMode.MARKDOWN)


def work_alarm(update, context):
    global work_bool
    work_text = ""
    wList = []
    with open(str(update.message.from_user.id) + "-work.txt") as f:
        wList = f.readlines()
    wList = [w.strip("\n") for w in wList]
    counter = 1
    work_bool = False
    for i in wList:
        work_text += "\n    " + str(counter) + ".  " + i
        counter += 1
    context.bot.send_message(chat_id=context.job.context, text="Work:"+work_text)