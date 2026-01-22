import datetime
from dateutil.relativedelta import relativedelta

from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import ObjectHelper, StringHelper, RandomHelper


DEFAULT_DATETIME_PATTERN = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATE_PATTERN = '%Y-%m-%d'
DEFAULT_TIME_PATTERN = '%H:%M:%S'

DATETIME_FULL_PATTERN = '%Y-%m-%d %H:%M:%S.%f'
TIME_FULL_PATTERN = '%H:%M:%S.%f'

PATTERNS = (
    DEFAULT_DATETIME_PATTERN,
    DEFAULT_DATE_PATTERN,
    DEFAULT_TIME_PATTERN,
    DATETIME_FULL_PATTERN,
    TIME_FULL_PATTERN
)

DATETIME_PATTERNS = (
    DEFAULT_DATETIME_PATTERN,
    DATETIME_FULL_PATTERN
)

DATE_PATTERNS = (
    DEFAULT_DATE_PATTERN
)

TIME_PATTERNS = (
    DEFAULT_TIME_PATTERN,
    TIME_FULL_PATTERN
)

DEFAULT_TIME_BEGIN = '00:00:00'
DEFAULT_TIME_END = '23:59:59'


def isDateTime(givenDatetime):
    return (
        isNativeDateTime(givenDatetime) or
        (
            isinstance(givenDatetime, str) and
            isinstance(of(givenDatetime), datetime.datetime)
        )
    )


def isNativeDateTime(givenDatetime):
    return isinstance(givenDatetime, datetime.datetime)


def toString(givenDatetime, pattern=DEFAULT_DATETIME_PATTERN):
    return givenDatetime if ObjectHelper.isNone(givenDatetime) or isinstance(givenDatetime, str) else parseToString(givenDatetime, pattern=pattern)

def parseToString(given, pattern=DEFAULT_DATETIME_PATTERN):
    # return str(parseToPattern(str(given), pattern=pattern))
    # return str(given)
    return str(forcedlyParse(str(given), pattern=pattern))

def parseToPattern(given, pattern=DEFAULT_DATETIME_PATTERN, timedelta=False):
    given = given.strip()
    if StringHelper.isNotBlank(given):
        parsed = datetime.datetime.strptime(given, pattern)
        if timedelta and pattern in TIME_PATTERNS :
            return timeDelta(hours=parsed.hour, minutes=parsed.minute, seconds=parsed.second, milliseconds=parsed.millisecond, microseconds=parsed.microsecond)
        if pattern in DATETIME_PATTERNS :
            return parsed
        elif pattern in DATE_PATTERNS :
            return parsed.date()
        elif pattern in TIME_PATTERNS :
            return parsed.time()

def forcedlyParse(given, pattern=DEFAULT_DATETIME_PATTERN, timedelta=False):
    parsed = None
    for pattern in [pattern, *PATTERNS] :
        try :
            parsed = parseToPattern(given, pattern=pattern, timedelta=timedelta)
            break
        except Exception as exception :
            pass
    return parsed

def parseToDateTime(givenDatetime, pattern=DEFAULT_DATETIME_PATTERN):
    return givenDatetime if ObjectHelper.isNone(givenDatetime) or not isinstance(givenDatetime, str) else parseToPattern(givenDatetime, pattern=pattern)

def forcedlyGetDateTime(givenDatetime, pattern=DEFAULT_DATETIME_PATTERN):
    return givenDatetime if ObjectHelper.isNone(givenDatetime) or not isinstance(givenDatetime, str) else forcedlyParse(givenDatetime, pattern=pattern)

def forcedlyGetDate(givenDate, pattern=DEFAULT_DATE_PATTERN):
    return givenDate if ObjectHelper.isNone(givenDate) or not isinstance(givenDate, str) else forcedlyParse(givenDate, pattern=pattern)

def forcedlyGetTime(givenTime, pattern=DEFAULT_TIME_PATTERN):
    return givenTime if ObjectHelper.isNone(givenTime) or not isinstance(givenTime, str) else forcedlyParse(givenTime, pattern=pattern)

def forcedlyGetInterval(givenTime, pattern=DEFAULT_DATETIME_PATTERN):
    return givenTime if ObjectHelper.isNone(givenTime) or not isinstance(givenTime, str) else forcedlyParse(givenTime, pattern=pattern, timedelta=True)

def timeDelta(days=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0, **kwargs):
    return datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds, microseconds=microseconds, **kwargs)

def dateTimeNow():
    # return datetime.datetime.utcnow()
    return datetime.datetime.now()

def now():
    return dateTimeNow()

def dateOf(dateTime=None, pattern=DEFAULT_DATE_PATTERN):
    if isinstance(dateTime, str):
        dateTime = forcedlyGetDateTime(dateTime)
    return dateTime.date()

def timeOf(dateTime=None, pattern=DEFAULT_TIME_PATTERN):
    if isinstance(dateTime, str):
        dateTime = forcedlyGetDateTime(dateTime)
    return dateTime.time()

def dateNow():
    # datetime.date.today()
    return dateOf(dateTime=dateTimeNow())

def timeNow():
    return timeOf(dateTime=dateTimeNow())

def timestampNow():
    return datetime.datetime.timestamp(dateTimeNow())

def ofTimestamp(timestamp):
    # return datetime.datetime.utcfromtimestamp(timestamp)
    return datetime.datetime.fromtimestamp(timestamp)

def of(dateTime=None, date=None, time=None, pattern=DEFAULT_DATETIME_PATTERN):
    if isinstance(dateTime, datetime.datetime):
        return forcedlyParse(str(dateTime), pattern=pattern)
    elif isinstance(dateTime, str):
        return forcedlyParse(dateTime, pattern=pattern)
    datePattern = None
    timePattern = None
    if ObjectHelper.isNotNone(pattern):
        splittedPattern = pattern.split()
        if 1 < len(splittedPattern):
            datePattern = splittedPattern[0]
            timePattern = splittedPattern[1]
    if ObjectHelper.isNone(datePattern) or ObjectHelper.isNone(timePattern):
        datePattern = DEFAULT_DATE_PATTERN
        timePattern = DEFAULT_TIME_PATTERN
    if ObjectHelper.isNotNone(dateTime):
        date = dateOf(dateTime, pattern=datePattern)
        time = timeOf(dateTime, pattern=timePattern)
    return datetime.datetime.combine(
        forcedlyGetDate(date if ObjectHelper.isNotNone(date) else dateNow(), pattern=datePattern),
        forcedlyGetTime(time if ObjectHelper.isNotNone(time) else DEFAULT_TIME_BEGIN, pattern=timePattern)
    )

def timestampOf(dateTime=None, date=None, time=None, pattern=DATETIME_FULL_PATTERN):
    return datetime.datetime.timestamp(of(date=date, time=time, dateTime=dateTime, pattern=pattern))

def plusSeconds(givenDateTimeOrTime, seconds=None, deltaInSeconds=None):
    if ObjectHelper.isNotNone(seconds):
        deltaInMinutes = timeDelta(seconds=seconds)
    if isinstance(givenDateTimeOrTime, datetime.time):
        givenDateTimeOrTime = forcedlyParse(f'{str(dateNow())} {givenDateTimeOrTime}')
    return forcedlyGetDateTime(str(givenDateTimeOrTime)) + deltaInMinutes

def minusSeconds(givenDateTimeOrTime, seconds=None, deltaInSeconds=None):
    if ObjectHelper.isNotNone(seconds):
        deltaInMinutes = timeDelta(seconds=seconds)
    if isinstance(givenDateTimeOrTime, datetime.time):
        givenDateTimeOrTime = forcedlyParse(f'{str(dateNow())} {givenDateTimeOrTime}')
    return forcedlyGetDateTime(str(givenDateTimeOrTime)) - deltaInMinutes

def plusMinutes(givenDateTimeOrTime, minutes=None, deltaInMinutes=None):
    if ObjectHelper.isNotNone(minutes):
        deltaInMinutes = timeDelta(seconds=minutes*60)
    if isinstance(givenDateTimeOrTime, datetime.time):
        givenDateTimeOrTime = forcedlyParse(f'{str(dateNow())} {givenDateTimeOrTime}')
    return forcedlyGetDateTime(str(givenDateTimeOrTime)) + deltaInMinutes

def minusMinutes(givenDateTimeOrTime, minutes=None, deltaInMinutes=None):
    if ObjectHelper.isNotNone(minutes):
        deltaInMinutes = timeDelta(minutes=minutes)
    if isinstance(givenDateTimeOrTime, datetime.time):
        givenDateTimeOrTime = forcedlyParse(f'{str(dateNow())} {givenDateTimeOrTime}')
    return forcedlyGetDateTime(str(givenDateTimeOrTime)) - deltaInMinutes

def plusDays(givenDateTime, days=None, deltaInDays=None):
    if ObjectHelper.isNotNone(days):
        deltaInDays = timeDelta(days=days)
    return forcedlyGetDateTime(str(givenDateTime)) + deltaInDays

def minusDays(givenDateTime, days=None, deltaInDays=None):
    if ObjectHelper.isNotNone(days):
        deltaInDays = timeDelta(days=days)
    return forcedlyGetDateTime(str(givenDateTime)) - deltaInDays

def plusMonths(givenDateTime, months=None):
    if ObjectHelper.isNone(givenDateTime) or ObjectHelper.isNone(months):
        return givenDateTime
    dateTime = forcedlyGetDateTime(str(givenDateTime))
    return forcedlyGetDateTime(f'{dateOf(dateTime=dateTime) + relativedelta(months=months)} {timeOf(dateTime=dateTime)}')

def minusMonths(givenDateTime, months=None):
    return plusMonths(givenDateTime, months=-months)

def plusYears(givenDateTime, years=None):
    if ObjectHelper.isNone(givenDateTime) or ObjectHelper.isNone(years):
        return givenDateTime
    dateTime = forcedlyGetDateTime(str(givenDateTime))
    return forcedlyGetDateTime(f'{dateOf(dateTime=dateTime) + relativedelta(months=12*years)} {timeOf(dateTime=dateTime)}')

def minusYears(givenDateTime, years=None):
    return plusYears(givenDateTime, years=-years)

def getDefaultTimeBegin():
    return forcedlyGetTime(DEFAULT_TIME_BEGIN)

def getDatetimeMonthBegin():
    return parseToPattern(c.SPACE.join([c.DASH.join([*str(dateTimeNow()).split()[0].split(c.DASH)[:-1], '01']), DEFAULT_TIME_BEGIN]))

def getTodayDateAndTodayTime():
    dateTime = dateTimeNow()
    return dateOf(dateTime=dateTime), timeOf(dateTime=dateTime)

def getTodayDateTimeBegin():
    return parseToDateTime(f'{dateNow()} {DEFAULT_TIME_BEGIN}')

def getTodayDateTimeEnd():
    return parseToDateTime(f'{dateNow()} {DEFAULT_TIME_END}')

###- deprecated
def getWeekDay(dateTime=None, date=None, time=None):
    return getWeekDayOf(dateTime=dateTime, date=date, time=time)

def getWeekDayOf(dateTime=None, date=None, time=None):
    if ObjectHelper.isNotNone(dateTime):
        return forcedlyGetDateTime(dateTime).weekday()
    elif ObjectHelper.isNotNone(date) and ObjectHelper.isNotNone(time):
        return of(date=forcedlyGetDate(date), time=forcedlyGetTime(time)).weekday()
    elif ObjectHelper.isNotNone(date):
        return of(date=forcedlyGetDate(date), time=forcedlyGetTime(DEFAULT_TIME_END)).weekday()
    return dateTimeNow().weekday()

def addTimePotiomToDateAsStringIfNeeded(date):
    return None if ObjectHelper.isNone(date) else f'{str(date).strip()} {DEFAULT_TIME_BEGIN}' if ObjectHelper.equals(1, len(str(date).strip().split())) else date

def addNoise(givenDatetime):
    return givenDatetime + timeDelta(milliseconds=RandomHelper.integer(0,999))
