import urllib2
from bs4 import BeautifulSoup

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode

def arsenal(update, context):
    """Display current PL standing and next 5 matches"""
    m = update.message.reply_text("Fetching...", parse_mode=ParseMode.HTML)
    m.edit_text(fetch_fixtures(), parse_mode=ParseMode.HTML)

def fetch_fixtures():
  arsenal_page = 'https://fbref.com/en/squads/18bb7c10/Arsenal'
  page = urllib2.urlopen(arsenal_page)

  soup = BeautifulSoup(page, "html.parser")

  s = soup.find(id="meta").contents[3].p.contents[2].strip().replace("-", " ").replace(",", " ").replace("st", " ").replace("th", " ").replace("nd", " ").replace("rd", " ")
  s2 = [int(i) for i in s.split() if i.isdigit()]
  mp = s2[0]+s2[1]+s2[2]
  points = s2[3]
  pos = s2[4]

  t = soup.find(id="ks_sched_3232").find("tbody").find_all("tr")[mp:mp+5]

  suffix = "th"
  if pos % 10 == 1:
    suffix = "st"
  elif pos % 10 == 2:
    suffix = "nd"
  elif pos % 10 == 3:
    suffix = "rd"

  result = "<u>Arsenal: " + str(pos) + suffix + " - " + str(points) + " points</u>\n"
  for i in range(0,5): 
    result += "    (" + t[i].find("td", {"data-stat": "date"}).contents[0] + ")"
    if t[i].find("td", {"data-stat": "venue"}).contents[0] == 'Away':
      result += "\t@\t"
    else:
      result += "\tvs.\t"
    result += t[i].find("td", {"data-stat": "opponent"}).contents[0].contents[0]
    result += "\n"

  return result[:-1]