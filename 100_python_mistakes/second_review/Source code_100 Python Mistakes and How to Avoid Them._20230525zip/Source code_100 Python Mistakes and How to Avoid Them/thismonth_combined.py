from datetime import datetime
this_year = datetime.now().year
this_month = datetime.now().month

from .calendar import this_year, this_month
from calendar import TextCalendar

TextCalendar().prmonth(this_year, this_month)
