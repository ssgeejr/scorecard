import datetime
from datetime import datetime, date, timedelta


dtkey = '0721'

my_date = datetime.strptime(dtkey, "%m%y")
last_month = my_date - timedelta(1)

print(my_date)

print(last_month.strftime('%m%y'))




