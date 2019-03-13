import json
from time import time, localtime, strftime
import datetime
from util import database

ISOTIMEFORMAT='%Y-%m-%d %X'
meeting = json.load(database.meeting)
member = json.load(database.member)

#get what date is it today
def getWeekn():
    x = localtime(time())
    return strftime("%A", x)

#Is this person late for the meeting longer than 15 minutes or not
def isLate(meetingtime):
    now = datetime.datetime.now()
    meetingTime = now.replace(hour = meetingtime, minute=15, second=0, microsecond=0)
    return now > meetingTime

#Is this person late for meeting
def PersonLate(name):
   #what team they belong to
   team = ""
   meetinghour = 0
   meetingName = ""
   if member["R2"].contains(name):
       team = "R2"
   if member["Communication"].contains(name):
       team = "Communication"
   if member["Minibot"].contains(name):
       team = "Minibot"

   today = getWeekn()
   meetingslst = meeting[team]
   for m in meetingslst:
       if m["dayofWeek"] == today:
           meetinghour = m["time"]
           meetingName = m["name"]

   late = isLate(meetinghour)
   return (name, meetingName, late)



