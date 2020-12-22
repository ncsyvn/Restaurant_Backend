import datetime
from calendar import monthrange


y = datetime.datetime.today() - datetime.timedelta(10)
print(y)
y = y.replace(day=1)
print(y)

print(y.day)
t = monthrange(2020, 7)
print(t[1])

datetime_now = datetime.datetime.now()
print("datetime now is: ", datetime_now)
print("Day of week is: ", datetime_now.weekday())
previous_day = datetime_now - datetime.timedelta(1)
print("Previous day is: ", previous_day)


datetime_now = datetime.datetime.now()
list_day_of_week = []
list_day_in_week = []
for i in range(7):
    date = datetime_now - datetime.timedelta(i)
    list_day_in_week.append(date)
    list_day_of_week.append(date.weekday())
print(list_day_of_week)
print(list_day_in_week)
