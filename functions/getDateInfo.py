import locale
from datetime import date
from datetime import datetime

dateToday = date.today()
hourNow   = datetime.now()

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

class getDateInfo():
    def dateFormated():
        return f"{dateToday.day}-{dateToday.month}-{dateToday.year}"
    
    def getDay():
        return dateToday.day
    
    def getMonth():
        return dateToday.month
    
    def getHour():
        return hourNow.strftime("%H:%M:%S")

    def nameDay():
        return dateToday.strftime('%A').capitalize()

    def nameMonth():
        return dateToday.strftime('%B').capitalize()
    
    def getYear():
        return dateToday.strftime('%Y').capitalize()