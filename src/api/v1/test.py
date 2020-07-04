import datetime
from calendar import monthrange


y = datetime.datetime.today() - datetime.timedelta(10)
print(y)
y = y.replace(day=1)
print(y)


t = monthrange(2020, 7)
print(t)
