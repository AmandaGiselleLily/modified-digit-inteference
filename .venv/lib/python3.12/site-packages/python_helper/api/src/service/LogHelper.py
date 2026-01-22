import colorama, traceback
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import SettingHelper, StringHelper, EnvironmentHelper, ObjectHelper, ReflectionHelper

LOG = 'LOG'
INFO = 'INFO'
STATUS = 'STATUS'
SUCCESS = 'SUCCESS'
SETTING = 'SETTING'
DEBUG = 'DEBUG'
WARNING = 'WARNING'
WRAPPER = 'WRAPPER'
FAILURE = 'FAILURE'
ERROR = 'ERROR'
TEST = 'TEST'

from python_helper.api.src.helper import LogHelperHelper

RESET_ALL_COLORS = colorama.Style.RESET_ALL
COLOR_SET = set([*[cv for dv in LogHelperHelper.LEVEL_DICTIONARY.values() for ck, cv in dv.items() if ck in [LogHelperHelper.FIRST_LAYER_COLOR, LogHelperHelper.SECOND_LAYER_COLOR]], c.RESET_COLOR])

LOGS_FILE_NAME = 'LOGS_FILE_NAME'
ENABLE_LOGS_WITH_COLORS = 'ENABLE_LOGS_WITH_COLORS'
LOGS_WITH_COLORS = 'LOGS_WITH_COLORS'


LOG_LEVEL_ENABLED_BY_DEFAULT_LIST = (
    ERROR
    , SUCCESS
    # , FAILURE
    #,  SETTING
    # , STATUS
    # , INFO
    # , WARNING
    # , DEBUG
    # , WRAPPER
    # , LOG
    # , TEST
)


global LOG_HELPER_SETTINGS


def colorsEnabled(enable=False):
    return enable or EnvironmentHelper.isTrue(ENABLE_LOGS_WITH_COLORS, default=False) or SettingHelper.activeEnvironmentIsLocal()

def logIt(text, **kwargs):
    # if not (text in LogHelperHelper.COLOR_SET):
    #     print(text, **kwargs)
    # print(f'{DateTimeHelper.now()} - {text}', **kwargs)
    EnvironmentHelper.printAndFlush(text, **kwargs)

def loadSettings(logsFileName=None, withColors=False, enabledByDefault=LOG_LEVEL_ENABLED_BY_DEFAULT_LIST):
    global LOG_HELPER_SETTINGS
    colorama.deinit()
    activeEnvironment = SettingHelper.getActiveEnvironment()
    colorsAreEnabled = withColors or colorsEnabled(enable=activeEnvironment==SettingHelper.LOCAL_ENVIRONMENT)
    LOG_HELPER_SETTINGS = {
        **{
            SettingHelper.ACTIVE_ENVIRONMENT: activeEnvironment,
            LOGS_FILE_NAME: logsFileName,
            LOGS_WITH_COLORS: colorsAreEnabled
        },
        **{
            level: (c.TRUE if EnvironmentHelper.isTrue(level, default=False) or level in enabledByDefault else c.FALSE) for level in LogHelperHelper.LEVEL_DICTIONARY
        }
    }
    if colorsAreEnabled:
        colorama.init()

    # global LOG_HELPER_SETTINGS
    # colorama.deinit()
    # settings = {}
    # settings[SettingHelper.ACTIVE_ENVIRONMENT] = SettingHelper.getActiveEnvironment()
    # for level in LogHelperHelper.LEVEL_DICTIONARY :
    #     settings[level] = c.TRUE if EnvironmentHelper.isTrue(level, default=True) else c.FALSE
    # LOG_HELPER_SETTINGS = settings
    # if colorsEnabled():
    #     colorama.init()
    #     # logIt(RESET_ALL_COLORS, end=c.BLANK)

loadSettings()

def log(origin, message, exception=None, muteStackTrace=False, newLine=False, level=LOG):
    LogHelperHelper.softLog(origin, message, level, muteStackTrace=muteStackTrace, newLine=newLine, exception=exception)

def info(origin, message, newLine=False):
    LogHelperHelper.softLog(origin, message, INFO, muteStackTrace=True, newLine=newLine)

def status(origin, message, newLine=False):
    LogHelperHelper.softLog(origin, message, STATUS, muteStackTrace=True, newLine=newLine)

def success(origin, message, newLine=False):
    LogHelperHelper.softLog(origin, message, SUCCESS, muteStackTrace=True, newLine=newLine)

def setting(origin, message, muteStackTrace=False, newLine=False):
    LogHelperHelper.softLog(origin, message, SETTING, muteStackTrace=muteStackTrace, newLine=newLine)

def debug(origin, message, exception=None, muteStackTrace=False, newLine=False):
    LogHelperHelper.softLog(origin, message, DEBUG, muteStackTrace=muteStackTrace, newLine=newLine, exception=exception)

def warning(origin, message, exception=None, muteStackTrace=False, newLine=False):
    LogHelperHelper.softLog(origin, message, WARNING, muteStackTrace=muteStackTrace, newLine=newLine, exception=exception)

def wrapper(origin, message, exception=None, muteStackTrace=False, newLine=False):
    LogHelperHelper.softLog(origin, message, WRAPPER, muteStackTrace=muteStackTrace, newLine=newLine, exception=exception)

def failure(origin, message, exception, muteStackTrace=False, newLine=False):
    LogHelperHelper.hardLog(origin, message, exception, FAILURE, muteStackTrace=muteStackTrace, newLine=newLine)

def error(origin, message, exception, muteStackTrace=False, newLine=False):
    LogHelperHelper.hardLog(origin, message, exception, ERROR, muteStackTrace=muteStackTrace, newLine=newLine)

def test(origin, message, exception=None, muteStackTrace=False, newLine=False):
    LogHelperHelper.softLog(origin, message, TEST, muteStackTrace=muteStackTrace, newLine=newLine, exception=exception)

def printLog(message, level=LOG, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None):
    LogHelperHelper.printMessageLog(level, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printInfo(message, condition=False, newLine=True, margin=True):
    LogHelperHelper.printMessageLog(INFO, message, condition=condition, muteStackTrace=True, newLine=newLine, margin=margin)

def printStatus(message, condition=False, newLine=True, margin=True):
    LogHelperHelper.printMessageLog(STATUS, message, condition=condition, muteStackTrace=True, newLine=newLine, margin=margin)

def printSuccess(message, condition=False, newLine=True, margin=True):
    LogHelperHelper.printMessageLog(SUCCESS, message, condition=condition, muteStackTrace=True, newLine=newLine, margin=margin)

def printSetting(message, condition=False, muteStackTrace=False, newLine=True, margin=True):
    LogHelperHelper.printMessageLog(SETTING, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin)

def printDebug(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None):
    LogHelperHelper.printMessageLog(DEBUG, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printWarning(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None):
    LogHelperHelper.printMessageLog(WARNING, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printWarper(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None):
    LogHelperHelper.printMessageLog(WRAPPER, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printFailure(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None):
    LogHelperHelper.printMessageLog(FAILURE, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printError(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None):
    LogHelperHelper.printMessageLog(ERROR, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def printTest(message, condition=False, muteStackTrace=False, newLine=True, margin=True, exception=None):
    LogHelperHelper.printMessageLog(TEST, message, condition=condition, muteStackTrace=muteStackTrace, newLine=newLine, margin=margin, exception=exception)

def prettyPython(
        origin,
        message,
        dictionaryInstance,
        quote = c.SINGLE_QUOTE,
        tabCount = 0,
        nullValue = c.NONE,
        trueValue = c.TRUE,
        falseValue = c.FALSE,
        logLevel = LOG,
        condition = True
    ):
    if condition :
        stdout, stderr = EnvironmentHelper.getCurrentSoutStatus()
        prettyPythonValue = StringHelper.prettyPython(
            dictionaryInstance,
            quote = quote,
            tabCount = tabCount,
            nullValue = nullValue,
            trueValue = trueValue,
            falseValue = falseValue,
            withColors = colorsEnabled(),
            joinAtReturn = False
        )
        LogHelperHelper.softLog(origin, StringHelper.join([message, c.COLON_SPACE, *prettyPythonValue]), logLevel)
        EnvironmentHelper.overrideSoutStatus(stdout, stderr)

def prettyJson(
        origin,
        message,
        dictionaryInstance,
        quote = c.DOUBLE_QUOTE,
        tabCount = 0,
        nullValue = c.NULL_VALUE,
        trueValue = c.TRUE_VALUE,
        falseValue = c.FALSE_VALUE,
        logLevel = LOG,
        condition = True
    ):
    if condition :
        stdout, stderr = EnvironmentHelper.getCurrentSoutStatus()
        prettyJsonValue = StringHelper.prettyJson(
            dictionaryInstance,
            quote = quote,
            tabCount = tabCount,
            nullValue = nullValue,
            trueValue = trueValue,
            falseValue = falseValue,
            withColors = colorsEnabled(),
            joinAtReturn = False
        )
        LogHelperHelper.softLog(origin, StringHelper.join([message, c.COLON_SPACE, *prettyJsonValue]), logLevel)
        EnvironmentHelper.overrideSoutStatus(stdout, stderr)

def getExceptionMessage(exception):
    if ObjectHelper.isEmpty(exception):
        return c.UNKNOWN
    exceptionAsString = str(exception)
    if c.BLANK == exceptionAsString :
        return ReflectionHelper.getName(exception.__class__)
    else :
        return exceptionAsString

def getTracebackMessage(muteStackTrace):
    tracebackMessage = c.BLANK
    try :
        tracebackMessage = traceback.format_exc()
    except :
        tracebackMessage = f'{c.NEW_LINE}'
    if muteStackTrace :
        return StringHelper.join(tracebackMessage.split(c.NEW_LINE)[-2:], character=c.NEW_LINE)
    return LogHelperHelper.NO_TRACEBACK_PRESENT_MESSAGE if LogHelperHelper.NO_TRACEBACK_PRESENT == str(tracebackMessage) else tracebackMessage


def debugIt(unnamedExpression, asDictionary=False, depthSkip=0):
    return logIt(f'{ReflectionHelper.getInstanceName(unnamedExpression, depthSkip=depthSkip+1)}: {StringHelper.prettyPython(unnamedExpression if not asDictionary else unnamedExpression)}')