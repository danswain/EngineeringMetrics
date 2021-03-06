import datetime
import locale
import numpy as np


def to_ts(dt):
    td = dt - datetime.datetime(1970, 1, 1)
    return (
        td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6
    ) / 10 ** 6 - 60 * 60


def to_dt(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def utc_ts(dt=datetime.datetime.utcnow()):
    """ timestamp in seconds """
    return to_ts(dt)


def day_ts(dt=datetime.datetime.utcnow()):
    """ timestamp in seconds for a day """
    return to_ts(datetime.datetime(year=dt.year, month=dt.month, day=dt.day))


def is_int(s):
    try:
        if isinstance(s, str):
            num = to_num(s)
            if isinstance(num, float):
                return num.is_integer()
            return isinstance(num, int)
        elif isinstance(s, int):
            int(s)
            return True
        else:
            return False
    except ValueError:
        return False


def is_num(s):
    try:
        locale.atoi(str(s))
    except ValueError:
        try:
            locale.atof(str(s))
        except ValueError:
            return False
    return True


def to_num(s):
    try:
        return locale.atoi(str(s))
    except ValueError:
        return locale.atof(str(s))


def to_str(value):
    try:
        strval = u"".join(value)
    except TypeError:
        strval = str(value, errors="ignore")
    return strval


def business_days(earlier_date: datetime, later_date: datetime):
    full_duration = later_date - earlier_date
    # pylint: disable=no-member
    bus_days = np.busday_count(earlier_date.date(), later_date.date()).item()
    duration = full_duration

    if full_duration.days == 2 and bus_days == 1:
        duration = full_duration - datetime.timedelta(days=(2))
    elif full_duration.days > bus_days:
        duration = full_duration - datetime.timedelta(days=(full_duration.days - bus_days))

    return duration