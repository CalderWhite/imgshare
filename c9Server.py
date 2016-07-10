import datetime, calendar
def currentTime():
    x = datetime.datetime.now()
    retstr = str(x.day) + "-" + calendar.month_name[x.month] + "-" + str(x.year) + "_" + str(x.hour) + ":" + str(x.minute) + ":" + str(x.second)
    return retstr