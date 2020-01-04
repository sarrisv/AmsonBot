from datetime import datetime, time,  timedelta

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode

exam_bool = False
f = None

def exam(update, context):
    """nightly reminder"""
    global exam_bool, f
    f = open(str(update.message.from_user.id) + "-exam.txt", "a+")
    requested_exam = str(" ".join(update.message.text.split(" ")[1:]))
    if len(requested_exam.replace(" ", "")) > 0:
        context.bot.send_message(chat_id=update.message.chat_id, text=('Added *' + requested_exam + '* to list!'), parse_mode=ParseMode.MARKDOWN)
        f.write(requested_exam + "\n")
        if exam_bool == False:
            context.job_queue.run_repeating(exam_alarm, timedelta(days=7), time(hour=15), context=update.message.chat_id)
            exam_bool = True
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=('Problem adding \"*' + requested_exam + '*\" to list!'), parse_mode=ParseMode.MARKDOWN)
    f.close()


def remove_exam(update, context):
    """remove nightly reminder"""
    eList = []
    with open(str(update.message.from_user.id) + "-exam.txt", "r") as f:
        eList = f.readlines()
    eList = [w.strip("\n") for w in eList]
    print eList
    print " ".join(str(update.message.text).split(" ")[1:])
    removed_item = " ".join(str(update.message.text).split(" ")[1:])
    if removed_item in eList:
        eList.remove(removed_item)
        with open(str(update.message.from_user.id) + "-exam.txt", "w") as f:
            for line in eList:
                if line.strip("\n") != removed_item:
                    f.write(line + "\n")
        context.bot.send_message(chat_id=update.message.chat_id, text=('Removed *' + removed_item + '* from list!'), parse_mode=ParseMode.MARKDOWN)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=('Problem removing \"*' + removed_item + '*\" from list!'), parse_mode=ParseMode.MARKDOWN)
    f.close()

def list_exam(update, context):
    eList = []
    with open(str(update.message.from_user.id) + "-exam.txt", "r+") as f:
        eList = f.readlines()
    if len(eList) != 0:  
        eList = [w.strip("\n") for w in eList]
        exam_text = ""
        counter = 1
        for i in eList:
            exam_text += "\n    " + str(counter) + ".  " + i
            counter += 1
        context.bot.send_message(chat_id=update.message.chat_id, text=("Here is your exam:" + exam_text), parse_mode=ParseMode.MARKDOWN)
    else: 
        context.bot.send_message(chat_id=update.message.chat_id, text=("Congrats, You have no exam!"), parse_mode=ParseMode.MARKDOWN)
    f.close()

def clear_exam(update, context):
    open(str(update.message.from_user.id) + "-exam.txt", "w")
    context.bot.send_message(chat_id=update.message.chat_id, text=('Cleared exam!'), parse_mode=ParseMode.MARKDOWN)


def exam_alarm(update, context):
    global exam_bool
    exam_text = ""
    eList = []
    with open(str(update.message.from_user.id) + "-exam.txt") as f:
        eList = f.readlines()
    eList = [w.strip("\n") for w in eList]
    counter = 1
    exam_bool = False
    for i in eList:
        exam_text += "\n    " + str(counter) + ".  " + i
        counter += 1
    context.bot.send_message(chat_id=context.job.context, text="exam:"+exam_text)