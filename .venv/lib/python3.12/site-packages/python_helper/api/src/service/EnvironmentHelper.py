import os, sys, json
from python_helper.api.src.service import StringHelper, LogHelper, ObjectHelper, SettingHelper
from python_helper.api.src.domain import Constant as c

OS = os
SYS = sys
OS_SEPARATOR = OS.path.sep

# ┍━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━┑
# │ System              │ Value               │
# ┝━━━━━━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━━━━━━┥
# │ Linux               │ linux or linux2 (*) │
# │ Windows             │ win32               │
# │ Windows/Cygwin      │ cygwin              │
# │ Windows/MSYS2       │ msys                │
# │ Mac OS X            │ darwin              │
# │ OS/2                │ os2                 │
# │ OS/2 EMX            │ os2emx              │
# │ RiscOS              │ riscos              │
# │ AtheOS              │ atheos              │
# │ FreeBSD 7           │ freebsd7            │
# │ FreeBSD 8           │ freebsd8            │
# │ FreeBSD N           │ freebsdN            │
# │ OpenBSD 6           │ openbsd6            │
# ┕━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━┙

LINUX_OS_NAME_LIST = [
    'linux',
    'linux2'
]
WINDOWS_OS_NAME_LIST = [
    'win32',
    'win64',
    'cygwin',
    'msys'
]
MAC_OS_NAME_LIST = [
    'darwin'
]
OTHER_OS_NAME_LIST = [
    'os2',
    'os2emx',
    'riscos',
    'atheos',
    'freebsd7',
    'freebsd8',
    'freebsdN',
    'openbsd6'
]

clear = lambda: OS.system('cls')

def setMaxIntToStringDigits(number):
    SYS.set_int_max_str_digits(number if number else 4300)

def setRecursionLimit(number):
    SYS.setrecursionlimit(number if number else 2097152)
    # threading.stack_size(number if number else 134217728)

def get(environmentKey, default=None):
    environmentValue = default if ObjectHelper.isNone(environmentKey) else OS.environ.get(environmentKey)
    return environmentValue if ObjectHelper.isNotNone(environmentValue) else default

def update(environmentKey, environmentValue, default=None):
    if ObjectHelper.isNotEmpty(environmentKey):
        associatedValue = None
        if ObjectHelper.isNotNone(environmentValue):
            associatedValue = str(StringHelper.filterString(environmentValue))
            OS.environ[environmentKey] = associatedValue
        elif ObjectHelper.isNotNone(default):
            associatedValue = str(StringHelper.filterString(default))
            OS.environ[environmentKey] = associatedValue
        else :
            try:
                delete(environmentKey)
            except Exception as exception :
                LogHelper.warning(update, f'Failed to delete enviroment variable key "{environmentKey}" while updating it to "{environmentValue}"', exception=exception)
        return associatedValue
    else :
        LogHelper.debug(update, f'arguments: environmentKey: {environmentKey}, environmentValue: {environmentValue}, default: {default}')
        raise Exception(f'Error associating environment variable "{environmentKey}" key to environment variable "{environmentValue}" value')

def switch(environmentKey, environmentValue, default=None):
    originalEnvironmentValue = get(environmentKey, default=default)
    update(environmentKey, environmentValue, default=default)
    return originalEnvironmentValue

def reset(environmentVariables, originalEnvironmentVariables):
    if environmentVariables :
        for key in environmentVariables.keys():
            if key in originalEnvironmentVariables :
                update(key, originalEnvironmentVariables[key])

def delete(environmentKey):
    if ObjectHelper.isNotNone(environmentKey):
        OS.environ.pop(environmentKey)

def getSet(avoidRecursiveCall=False):
    try :
        return {key : OS.environ[key] for key in OS.environ}
    except Exception as exception :
        LogHelper.error(getSet, 'Not possible to load os.environ as a json. Returning os.environ as string by default', exception)
        return str(OS.environ)[8:-1]

def isNone(environmentKey, default=True, evaluateItInsted=None):
    if ObjectHelper.isNotNone(environmentKey):
        return c.NONE == (
            evaluateItInsted if ObjectHelper.isNotNone(evaluateItInsted) else get(environmentKey, default=c.NONE)
        )
    return default

def isNotNone(environmentKey, default=True, evaluateItInsted=None):
    if ObjectHelper.isNotNone(environmentKey):
        return not c.NONE == (
            evaluateItInsted if ObjectHelper.isNotNone(evaluateItInsted) else get(environmentKey, default=c.NONE)
        )
    return default

def isBoolean(environmentKey, default=False, evaluateItInsted=None):
    if ObjectHelper.isNotNone(environmentKey):
        if ObjectHelper.isNotNone(evaluateItInsted):
            return evaluateItInsted in [c.TRUE, c.FALSE] if isNotNone(environmentKey, evaluateItInsted=evaluateItInsted) else default
        return get(environmentKey, default=default) in [c.TRUE, c.FALSE]
    return default

def isTrue(environmentKey, default=False, evaluateItInsted=None):
    if ObjectHelper.isNotNone(environmentKey):
        if ObjectHelper.isNotNone(evaluateItInsted):
            return c.TRUE == evaluateItInsted if isBoolean(environmentKey, default=default, evaluateItInsted=evaluateItInsted) else default
        innerEvaluatItInsted = get(environmentKey, default=None)
        if ObjectHelper.isNotNone(innerEvaluatItInsted):
            return isTrue(environmentKey, default=default, evaluateItInsted=innerEvaluatItInsted)
        if isBoolean(environmentKey, evaluateItInsted=innerEvaluatItInsted):
            return c.TRUE == c.TRUE if isinstance(default, bool) and default else c.FALSE
    return default

def isFalse(environmentKey, default=True, evaluateItInsted=None):
    if ObjectHelper.isNotNone(environmentKey):
        if ObjectHelper.isNotNone(evaluateItInsted):
            return c.FALSE == evaluateItInsted if isBoolean(environmentKey, default=default, evaluateItInsted=evaluateItInsted) else default
        innerEvaluatItInsted = get(environmentKey, default=None)
        if ObjectHelper.isNotNone(innerEvaluatItInsted):
            return isTrue(environmentKey, default=default, evaluateItInsted=innerEvaluatItInsted)
        if isBoolean(environmentKey, evaluateItInsted=innerEvaluatItInsted):
            return c.FALSE == c.FALSE if isinstance(default, bool) and not default else c.TRUE
    return default

def execute(commandLine):
    return OS.system(commandLine)

def listDirectoryContent(path):
    return OS.listdir(path)

def isDirectory(path):
    return OS.path.isdir(path)

def isFile(path):
    return OS.path.isfile(path)

def getCurrentDirectory():
    return OS.getcwd()

def getParentDirectory(path):
    return OS.path.dirname(path)

def cdDirectory(path):
    return OS.chdir(path)

def cdBack():
    return cdDirectory(getParentDirectory(getCurrentDirectory()))

def copyFile(filePath, asFilePath):
    sourceAndDestination = f'{filePath}{c.SPACE}{asFilePath}'
    if isLinux() or isMacOs():
        return execute(f'cp{c.SPACE}{sourceAndDestination}')
    if isWindows():
        return execute(f'copy{c.SPACE}{sourceAndDestination}')

def removeFile(filePath):
    if isLinux() or isMacOs():
        return execute(f'rm{c.SPACE}{c.DASH}rf{c.SPACE}{filePath}')
    if isWindows():
        return execute(f'cmd{c.SPACE}{c.FOWARD_SLASH}C{c.SPACE}rmdir{c.SPACE}{c.FOWARD_SLASH}S{c.SPACE}{c.FOWARD_SLASH}Q{c.SPACE}{filePath}')

def makeDirectory(path, accessRights=0o777):
    ###- accessRights = 0o777 --> write, access and read
    ###- accessRights = 0o755 --> access and read
    return OS.makedirs(path, mode=accessRights)

def buildPath(*args):
    return StringHelper.join([str(arg) for arg in args], character=OS_SEPARATOR)

def appendPath(path):
    return SYS.path.append(path)

def getCurrentSoutStatus(avoidRecursiveCall=False):
    return SYS.stdout, SYS.stderr

def overrideSoutStatus(stdout, stderr):
    SYS.stdout = stdout
    SYS.stderr = stderr

def printAndFlush(text, **kwargs):
    kwargs['flush'] = True
    print(text, **kwargs)

def flushIO():
    for io in getCurrentSoutStatus():
        try:
            io.flush()
        except Exception as e:
            print(f'------------- EnvironmentHelper.flushIO exception: {e} -------------')

def isLinux():
    return SYS.platform in LINUX_OS_NAME_LIST

def isWindows():
    return SYS.platform in WINDOWS_OS_NAME_LIST

def isMacOs():
    return SYS.platform in MAC_OS_NAME_LIST

def isOtherOs():
    return (
        SYS.platform in OTHER_OS_NAME_LIST
        or not isLinux()
        or not isWindows()
        or not isMacOs()
    )
