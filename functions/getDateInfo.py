import locale
from datetime import date

dateToday = date.today()
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

class getDateInfo():
    def dateFormated():
        return f"{dateToday.day}-{dateToday.month}-{dateToday.year}"

    def nameDay():
        return dateToday.strftime('%A').capitalize()

    def nameMonth():
        return dateToday.strftime('%B').capitalize()
    
    def getYear():
        return dateToday.strftime('%Y').capitalize()