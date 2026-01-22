from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import LogHelper, ObjectHelper, ReflectionHelper, StringHelper, DateTimeHelper


NO_TRACEBACK_PRESENT = f'NoneType: None{c.NEW_LINE}'
NO_TRACEBACK_PRESENT_MESSAGE = 'Exception: '

FIRST_LAYER_COLOR = 'FIRST_LAYER_COLOR'
SECOND_LAYER_COLOR = 'SECOND_LAYER_COLOR'
LOG_TEXT = 'LOG_TEXT'

###- make sure to change it manually too on getOriginPortion function
###- as python does not allow variable introducing there
MAX_ORIGIN_LOG_SIZE = 32

DATE_TIME_COLLOR_LAYER = c.BRIGHT_BLACK

LEVEL_DICTIONARY = {
    LogHelper.LOG : {
        FIRST_LAYER_COLOR : c.BRIGHT_BLACK,
        SECOND_LAYER_COLOR: c.BRIGHT_BLACK,
        LOG_TEXT : c.LOG
    },
    LogHelper.INFO : {
        FIRST_LAYER_COLOR : c.BRIGHT_BLACK,
        SECOND_LAYER_COLOR : c.DARK_WHITE,
        LOG_TEXT : c.INFO
    },
    LogHelper.STATUS : {
        FIRST_LAYER_COLOR : c.BRIGHT_GREEN,
        SECOND_LAYER_COLOR : c.BRIGHT_WHITE,
        LOG_TEXT : c.STATUS
    },
    LogHelper.SUCCESS : {
        FIRST_LAYER_COLOR : c.DARK_GREEN,
        SECOND_LAYER_COLOR: c.BRIGHT_GREEN,
        LOG_TEXT : c.SUCCESS
    },
    LogHelper.SETTING : {
        FIRST_LAYER_COLOR : c.DARK_BLUE,
        SECOND_LAYER_COLOR: c.BRIGHT_BLUE,
        LOG_TEXT : c.SETTING
    },
    LogHelper.DEBUG : {
        FIRST_LAYER_COLOR : c.DARK_CYAN,
        SECOND_LAYER_COLOR: c.BRIGHT_CYAN,
        LOG_TEXT : c.DEBUG
    },
    LogHelper.WARNING : {
        FIRST_LAYER_COLOR : c.DARK_YELLOW,
        SECOND_LAYER_COLOR: c.BRIGHT_YELLOW,
        LOG_TEXT : c.WARNING
    },
    LogHelper.WRAPPER : {
        FIRST_LAYER_COLOR : c.BRIGHT_WHITE,
        SECOND_LAYER_COLOR: c.DARK_WHITE,
        LOG_TEXT : c.WRAPPER
    },
    LogHelper.FAILURE : {
        FIRST_LAYER_COLOR : c.DARK_MAGENTA,
        SECOND_LAYER_COLOR: c.BRIGHT_MAGENTA,
        LOG_TEXT : c.FAILURE
    },
    LogHelper.ERROR : {
        FIRST_LAYER_COLOR : c.DARK_RED,
        SECOND_LAYER_COLOR: c.BRIGHT_RED,
        LOG_TEXT : c.ERROR
    },
    LogHelper.TEST : {
        FIRST_LAYER_COLOR : c.BRIGHT_BLACK,
        SECOND_LAYER_COLOR: c.BRIGHT_BLACK,
        LOG_TEXT : c.TEST
    }
}


def getStatus(level) :
    status = LogHelper.LOG_HELPER_SETTINGS.get(level)
    return status if isinstance(status, str) and StringHelper.isNotBlank(status) else c.TRUE

def getColors(level) :
    if LogHelper.colorsEnabled():
        firstLayerColor = LEVEL_DICTIONARY.get(level).get(FIRST_LAYER_COLOR) if LEVEL_DICTIONARY.get(level) and LEVEL_DICTIONARY.get(level).get(FIRST_LAYER_COLOR) else c.BLANK
        secondLayerColor = LEVEL_DICTIONARY.get(level).get(SECOND_LAYER_COLOR) if LEVEL_DICTIONARY.get(level) and LEVEL_DICTIONARY.get(level).get(SECOND_LAYER_COLOR) else c.BLANK
        tirdLayerColor = c.MUTTED_COLOR if c.MUTTED_COLOR else c.BLANK
        resetColor = c.RESET_COLOR if c.RESET_COLOR else c.BLANK
        dateTimeColor = DATE_TIME_COLLOR_LAYER
    else :
        firstLayerColor = c.BLANK
        secondLayerColor = c.BLANK
        tirdLayerColor = c.BLANK
        resetColor = c.BLANK
        dateTimeColor = c.BLANK
    return (firstLayerColor, secondLayerColor, tirdLayerColor, resetColor, dateTimeColor) if StringHelper.isNotBlank(firstLayerColor) else (c.BLANK, c.BLANK, c.BLANK, c.BLANK, c.BLANK)

def softLog(origin, message, level, exception=None, muteStackTrace=False, newLine=False) :
    if ObjectHelper.isNotNone(exception) :
        hardLog(origin, message, exception, level, muteStackTrace=muteStackTrace)
    elif c.TRUE == getStatus(level) :
        firstLayerColor, secondLayerColor, tirdLayerColor, resetColor, dateTimeColor = getColors(level)
        LogHelper.logIt(StringHelper.join([*getLogHeader(dateTimeColor, firstLayerColor, level), *getOriginPortion(origin, tirdLayerColor, resetColor), secondLayerColor, message, resetColor, getNewLine(newLine, exception=exception, muteStackTrace=muteStackTrace)]))
    elif not c.FALSE == getStatus(level) :
        levelStatusError(origin, level)

def hardLog(origin, message, exception, level, muteStackTrace=False, newLine=False) :
    if c.TRUE == getStatus(level) :
        firstLayerColor, secondLayerColor, tirdLayerColor, resetColor, dateTimeColor = getColors(level)
        LogHelper.logIt(StringHelper.join([*getLogHeader(dateTimeColor, firstLayerColor, level), *getOriginPortion(origin, tirdLayerColor, resetColor), secondLayerColor, message, *getErrorPortion(exception, muteStackTrace, firstLayerColor, secondLayerColor, tirdLayerColor, resetColor), resetColor, getNewLine(newLine, exception=exception, muteStackTrace=muteStackTrace)]))
    elif not c.FALSE == getStatus(level) :
        levelStatusError(origin, level)

def printMessageLog(level, message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None) :
    if condition :
        firstLayerColor, secondLayerColor, tirdLayerColor, resetColor, dateTimeColor = getColors(level)
        LogHelper.logIt(StringHelper.join([c.TAB if margin else c.BLANK, *getLogHeader(dateTimeColor, firstLayerColor, level), secondLayerColor, message, *getErrorPortion(exception, muteStackTrace, firstLayerColor, secondLayerColor, tirdLayerColor, resetColor), resetColor, getNewLine(newLine, exception=exception, muteStackTrace=muteStackTrace)]))

def getLogHeader(dateTimeColor, firstLayerColor, level):
    return [dateTimeColor, f'{str(DateTimeHelper.now()):0>26}', c.SPACE, firstLayerColor, LEVEL_DICTIONARY[level][LOG_TEXT]]

def getOriginPortion(origin, tirdLayerColor, resetColor):
    parsedOrigin = c.BLANK
    if origin and not origin == c.BLANK :
        moduleName = ReflectionHelper.getModuleName(origin)
        className = ReflectionHelper.getClassName(origin)
        moduleProtion = getLogThingName(moduleName)
        classPortion = getLogThingName(className)
        originalParserdOrigin = StringHelper.join([*moduleProtion, *classPortion, ReflectionHelper.getName(origin)])
        parsedOrigin = originalParserdOrigin
        if MAX_ORIGIN_LOG_SIZE < len(parsedOrigin):
            splittedParsedOrigin = StringHelper.split(parsedOrigin, character=c.DOT)
            parsedOrigin = StringHelper.join(
                [
                    reduceParsedOriginPortion(splittedParsedOrigin[0]),
                    *splittedParsedOrigin[1:]
                ],
                character = c.DOT
            ).strip()
            if MAX_ORIGIN_LOG_SIZE < len(parsedOrigin):
                splittedParsedOrigin = StringHelper.split(parsedOrigin, character=c.DOT)
                parsedOrigin = StringHelper.join(
                    [
                        *splittedParsedOrigin[:-1],
                        reduceParsedOriginPortion(splittedParsedOrigin[-1])
                    ],
                    character = c.DOT
                ).strip()
    return [tirdLayerColor, f'{parsedOrigin[getParsedOriginStartIndex(parsedOrigin):]:32}', c.COLON_SPACE, resetColor]

def reduceParsedOriginPortion(portion):
    reducedPortion = StringHelper.join(
        [
            f'{word[:3]}{c.BLANK if 3 >= len(word) else word[-1]}' for word in StringHelper.split(
                StringHelper.toTitle(portion)
            )
        ]
    )
    return f'{portion[0]}{reducedPortion[1:]}'

def getParsedOriginStartIndex(parsedOrigin):
    return 0 if len(parsedOrigin)<MAX_ORIGIN_LOG_SIZE else len(parsedOrigin)-MAX_ORIGIN_LOG_SIZE

def getLogThingName(thing) :
    return [] if thing in c.NATIVE_TYPES or (c.OPEN_TUPLE in thing and c.CLOSE_TUPLE in thing) else [thing, c.DOT]

def getErrorPortion(exception, muteStackTrace, firstLayerColor, secondLayerColor, tirdLayerColor, resetColor) :
    if ObjectHelper.isEmpty(exception) :
        return [c.BLANK]
    exceptionMessage = LogHelper.getExceptionMessage(exception)
    traceBackMessage = LogHelper.getTracebackMessage(muteStackTrace)
    traceBackMessageSplited = traceBackMessage.split(exceptionMessage)
    return [c.NEW_LINE, tirdLayerColor, *[t if t is not traceBackMessageSplited[-1] else t if t[-1] is not c.NEW_LINE else t[:-1] for t in traceBackMessageSplited if ObjectHelper.isNotNone(t)], secondLayerColor, exceptionMessage, resetColor]

def levelStatusError(origin, level) :
    LogHelper.failure(origin, f'"{level}" log level status is not properly defined: {getStatus(level)}', None)

def getNewLine(newLine, exception=None, muteStackTrace=False) :
    return c.NEW_LINE if (newLine and ObjectHelper.isNone(exception)) or (ObjectHelper.isNotNone(exception) and NO_TRACEBACK_PRESENT_MESSAGE == LogHelper.getTracebackMessage(muteStackTrace)) else c.BLANK

# FORE_SIMPLE_RESET_COLOR = colorama.Fore.RESET
# LEVEL_DICTIONARY = {
#     SUCCESS : {
#         FIRST_LAYER_COLOR : colorama.Fore.GREEN,
#         SECOND_LAYER_COLOR: colorama.Fore.GREEN + colorama.Style.BRIGHT
#     },
#     SETTING : {
#         FIRST_LAYER_COLOR : colorama.Fore.BLUE,
#         SECOND_LAYER_COLOR: colorama.Fore.BLUE + colorama.Style.BRIGHT
#     },
#     DEBUG : {
#         FIRST_LAYER_COLOR : colorama.Fore.CYAN,
#         SECOND_LAYER_COLOR: colorama.Fore.CYAN + colorama.Style.BRIGHT
#     },
#     WARNING : {
#         FIRST_LAYER_COLOR : colorama.Fore.YELLOW,
#         SECOND_LAYER_COLOR: colorama.Fore.YELLOW + colorama.Style.BRIGHT
#     },
#     WRAPPER : {
#         FIRST_LAYER_COLOR : colorama.Fore.WHITE + colorama.Style.BRIGHT,
#         SECOND_LAYER_COLOR: colorama.Fore.WHITE
#     },
#     FAILURE : {
#         FIRST_LAYER_COLOR : colorama.Fore.MAGENTA,
#         SECOND_LAYER_COLOR: colorama.Fore.MAGENTA + colorama.Style.BRIGHT
#     },
#     ERROR : {
#         FIRST_LAYER_COLOR : colorama.Fore.RED,
#         SECOND_LAYER_COLOR: colorama.Fore.RED + colorama.Style.BRIGHT
#     }
# }

# def print_format_table():
#     """
#     prints table of formatted text format options
#     """
#     for style in range(8):
#         for fg in range(30,38):
#             s1 = ''
#             for bg in range(40,48):
#                 format = ';'.join([str(style), str(fg), str(bg)])
#                 s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
#             print(s1)
#         print('\n')
#
# print_format_table()
#
# x = 0
# for i in range(24):
#   colors = ""
#   for j in range(5):
#     code = str(x+j)
#     colors = colors + "\33[" + code + "m\\33[" + code + "m\033[0m "
#   print(colors)
#   x=x+5
