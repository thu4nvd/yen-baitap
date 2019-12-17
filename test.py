import datetime

from datetime import date, timedelta

year = 1980
start_date = date(year, 1, 1)
end_date = date(year, 12, 31)
# delta = timedelta(days=1)
while start_date <= end_date:
    print (start_date.strftime("%Y-%m-%d"))
    start_date += timedelta(days=1)
