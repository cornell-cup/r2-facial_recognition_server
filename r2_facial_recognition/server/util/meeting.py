import json
from time import time, localtime, strftime
import datetime
from r2_facial_recognition.server.util import database

ISOTIMEFORMAT='%Y-%m-%d %X'
meeting = json.loads(json.dumps(database.meeting))
member = json.loads(json.dumps(database.member))


# get what date is it today
def get_weekn():
    x = localtime(time())
    return strftime("%A", x)


# Is this person late for the meeting longer than 15 minutes or not
def is_late(meeting_time):
    now = datetime.datetime.now()
    meeting_time = now.replace(hour=meeting_time, minute=15, second=0,
                               microsecond=0)
    return now > meeting_time


# Is this person late for meeting
def person_late(name):
    # what team they belong to
    team = ""
    meeting_hour = 0
    meeting_name = ""
    if name in member["R2"]:
        team = "R2"
    if name in member["Communication"]:
        team = "Communication"
    if name in member["Minibot"]:
        team = "Minibot"
    '''
    today = get_weekn()
    meetingslst = meeting[team]
    for m in meetingslst:
       if m["dayofWeek"] == today:
           meeting_hour = m["time"]
           meeting_name = m["name"]
    
    late = isLate(meeting_hour)
    return (name, meeting_name, late)
    '''
    # FIXME: Erm, what? Defs a last second patch for NASA.
    return name, "NASA", False



