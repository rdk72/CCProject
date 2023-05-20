from django import template
from datetime import datetime, timezone
from django.db.models import *

register = template.Library()

@register.filter()
def period(date_from, date_to):
    if date_to:
        duration = date_to-date_from
    else:
        duration = datetime.now(timezone.utc)-date_from
    seconds = duration.seconds #total seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    #return plural_days(duration.days)+'{:02}ч {:02}м {:02}с'.format(hours,minutes,seconds % 60 )
    return plural_days(duration.days)+'{:02}ч {:02}м'.format(hours,minutes)


@register.simple_tag
def delta_time_to_period(delta_time):
    seconds = round(delta_time)
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    days = seconds // 86400
    #return plural_days(duration.days)+'{:02}ч {:02}м {:02}с'.format(hours,minutes,seconds % 60 )
    return plural_days(days)+'{:02}ч {:02}м'.format(hours,minutes)



def plural_days(n):
    if n<1:
        return ""
    days = ['день', 'дня', 'дней']

    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p] + ' '


