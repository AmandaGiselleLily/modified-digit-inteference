from python_helper.api.src.service import StringHelper, LogHelper, ObjectHelper, EnvironmentHelper, FileHelper
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.helper import SettingHelperHelper

global ACTIVE_ENVIRONMENT_VALUE
ACTIVE_ENVIRONMENT_VALUE = None

ACTIVE_ENVIRONMENT = 'ACTIVE_ENVIRONMENT'
DEFAULT_ENVIRONMENT = 'default'
LOCAL_ENVIRONMENT = 'local'

def logEnvironmentSettings() :
    try :
        LogHelper.setting(logEnvironmentSettings, StringHelper.prettyJson(EnvironmentHelper.getSet()))
    except Exception as exception :
        LogHelper.failure(logEnvironmentSettings, 'Not possible do get a pretty json from EnvironmentHelper.getSet()', exception)
        LogHelper.setting(logEnvironmentSettings, EnvironmentHelper.getSet())

def updateActiveEnvironment(activeEnvironment) :
    global ACTIVE_ENVIRONMENT_VALUE
    ACTIVE_ENVIRONMENT_VALUE = DEFAULT_ENVIRONMENT if ObjectHelper.isNone(activeEnvironment) else activeEnvironment
    EnvironmentHelper.update(ACTIVE_ENVIRONMENT, ACTIVE_ENVIRONMENT_VALUE)
    return getValueAsString(ACTIVE_ENVIRONMENT_VALUE)

def softlyGetActiveEnvironment() :
    global ACTIVE_ENVIRONMENT_VALUE
    if ObjectHelper.isNone(ACTIVE_ENVIRONMENT_VALUE) :
        activeEnvironment = EnvironmentHelper.get(ACTIVE_ENVIRONMENT)
        if ObjectHelper.isNone(activeEnvironment) :
            ACTIVE_ENVIRONMENT_VALUE = updateActiveEnvironment(DEFAULT_ENVIRONMENT)
        else :
            ACTIVE_ENVIRONMENT_VALUE = activeEnvironment
    return getValueAsString(ACTIVE_ENVIRONMENT_VALUE)

def getActiveEnvironment() :
    global ACTIVE_ENVIRONMENT_VALUE
    ACTIVE_ENVIRONMENT_VALUE = updateActiveEnvironment(EnvironmentHelper.get(ACTIVE_ENVIRONMENT))
    return getValueAsString(ACTIVE_ENVIRONMENT_VALUE)

def activeEnvironmentIsDefault() :
    global ACTIVE_ENVIRONMENT_VALUE
    # return DEFAULT_ENVIRONMENT == getActiveEnvironment()
    return DEFAULT_ENVIRONMENT == ACTIVE_ENVIRONMENT_VALUE

def activeEnvironmentIsLocal() :
    global ACTIVE_ENVIRONMENT_VALUE
    # return LOCAL_ENVIRONMENT == getActiveEnvironment()
    return LOCAL_ENVIRONMENT == ACTIVE_ENVIRONMENT_VALUE

def getValueAsString(value) :
    return StringHelper.join([
        str(value)
    ])

def extractEnvironmentVariables(environmentVariables) :
    global ACTIVE_ENVIRONMENT_VALUE
    originalActiveEnvironment = None if ObjectHelper.isNone(ACTIVE_ENVIRONMENT_VALUE) else f'{ACTIVE_ENVIRONMENT_VALUE}'
    if ObjectHelper.isNotEmpty(originalActiveEnvironment) :
        ACTIVE_ENVIRONMENT_VALUE = None
    originalEnvironmentVariables = {}
    if ObjectHelper.isDictionary(environmentVariables) :
        for key, value in environmentVariables.items() :
            originalEnvironmentVariables[key] = EnvironmentHelper.switch(key, value)
    getActiveEnvironment()
    LogHelper.loadSettings()
    return originalEnvironmentVariables, originalActiveEnvironment

def recoverEnvironmentVariables(environmentVariables, originalEnvironmentVariables, originalActiveEnvironment) :
    global ACTIVE_ENVIRONMENT_VALUE
    EnvironmentHelper.reset(environmentVariables, originalEnvironmentVariables)
    LogHelper.loadSettings()
    ACTIVE_ENVIRONMENT_VALUE = originalActiveEnvironment

def getSettingTree(
    settingFilePath,
    settingTree = None,
    fallbackSettingFilePath = None,
    fallbackSettingTree = None,
    lazyLoad = False,
    keepDepthInLongString = False,
    depthStep = c.TAB_UNITS,
    encoding = c.ENCODING
) :
    settingInjectionList = []
    fallbackSettingInjectionList = []
    if ObjectHelper.isNotNone(fallbackSettingFilePath) :
        innerFallbackSettingTree, fallbackSettingInjectionList = getSettingTree(
            fallbackSettingFilePath,
            lazyLoad = True,
            keepDepthInLongString = keepDepthInLongString,
            depthStep = depthStep,
            encoding = encoding
        )
        # print(f'innerFallbackSettingTree: {innerFallbackSettingTree}')
        # print(f'fallbackSettingInjectionList: {fallbackSettingInjectionList}')
    else :
        innerFallbackSettingTree = {}
    # print('========= in ===========')
    # print('========= in ===========')
    # print('========= in ===========')
    # print(f'innerFallbackSettingTree: {innerFallbackSettingTree}')
    # print(f'fallbackSettingInjectionList: {fallbackSettingInjectionList}')
    allSettingLines = FileHelper.getFileLines(settingFilePath, encoding=encoding)
    longStringCapturing = False
    quoteType = None
    longStringList = None
    depth = 0
    nodeRefference = 0
    nodeKey = c.NOTHING
    if settingTree is None :
        settingTree = {}
    for line, settingLine in enumerate(allSettingLines) :
        if SettingHelperHelper.lineAproved(settingLine) :
            if longStringCapturing :
                # print('lineAproved')
                if not currentDepth :
                    currentDepth = 0
                longStringList.append(depthStep*c.SPACE + settingLine if keepDepthInLongString else settingLine[depth:])
                if quoteType in str(settingLine) :
                    longStringList[-1] = StringHelper.join(longStringList[-1].split(quoteType))[:-1] + quoteType
                    settingValue = StringHelper.join(longStringList)
                    nodeKey = SettingHelperHelper.updateSettingTreeAndReturnNodeKey(settingKey,settingValue,nodeKey,settingTree, False)
                    longStringCapturing = False
                    quoteType = None
                    longStringList = None
            else :
                currentDepth = SettingHelperHelper.getDepth(settingLine)
                isSameDepth = SettingHelperHelper.nextValidLineIsAtTheSameDepthOrLess(currentDepth, line, allSettingLines)
                # print(f'isSameDepth: {isSameDepth}')
                if currentDepth == depth :
                    # print('currentDepth == depth')
                    settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList = SettingHelperHelper.settingTreeInnerLoop(
                        settingLine,
                        nodeKey,
                        settingTree,
                        longStringCapturing,
                        quoteType,
                        longStringList,
                        settingInjectionList,
                        lazyLoad,
                        isSameDepth
                    )
                    # print('========= out ==========')
                    # print(f'settingKey: {settingKey}, settingValue: {settingValue}')
                elif currentDepth > depth :
                    # print('currentDepth > depth')
                    currentNodeRefference = currentDepth // (currentDepth - depth)
                    if currentNodeRefference - nodeRefference == 1 :
                        settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList = SettingHelperHelper.settingTreeInnerLoop(
                            settingLine,
                            nodeKey,
                            settingTree,
                            longStringCapturing,
                            quoteType,
                            longStringList,
                            settingInjectionList,
                            lazyLoad,
                            isSameDepth
                        )
                        # print('========= out ==========')
                        # print(f'settingKey: {settingKey}, settingValue: {settingValue}')
                        nodeRefference = currentNodeRefference
                        depth = currentDepth
                elif currentDepth < depth :
                    # print('currentDepth < depth')
                    nodeRefference = currentDepth // depthStep ###- if line.split(':')[0] == currentDepth + c.TAB_UNITS * ' ' +
                    depth = currentDepth
                    # print()
                    # print()
                    # print()
                    # print(str(line))
                    # print(str(nodeKey))
                    # print(str(settingLine))
                    splitedNodeKey = nodeKey.split(c.DOT)[:nodeRefference]
                    splitedNodeKeyLength = len(splitedNodeKey)
                    if splitedNodeKeyLength == 0 :
                        nodeKey = c.NOTHING
                    elif splitedNodeKeyLength == 1 :
                        nodeKey = splitedNodeKey[0]
                    else :
                        nodeKey = c.DOT.join(splitedNodeKey)
                    settingKey,settingValue,nodeKey,longStringCapturing,quoteType,longStringList = SettingHelperHelper.settingTreeInnerLoop(
                        settingLine,
                        nodeKey,
                        settingTree,
                        longStringCapturing,
                        quoteType,
                        longStringList,
                        settingInjectionList,
                        lazyLoad,
                        isSameDepth
                    )
                    # print('========= out ==========')
                    # print(f'settingKey: {settingKey}, settingValue: {settingValue}')
                    # if ObjectHelper.isNotNone(settingValue) and ObjectHelper.isNotEmpty(settingValue) :
                    depth = currentDepth
    # print(f'innerFallbackSettingTree: {innerFallbackSettingTree}')
    # print(f'fallbackSettingFilePath: {fallbackSettingFilePath}')
    # print('========= out ==========')
    # print('========= out ==========')
    # print('========= out ==========')
    if lazyLoad :
        # print('Lazy load')
        # print(f'settingTree: {settingTree}')
        # print(f'settingInjectionList: {settingInjectionList}')
        return settingTree, settingInjectionList
    elif (
        ObjectHelper.isNotEmptyCollection(innerFallbackSettingTree) and
        ObjectHelper.isNotNone(fallbackSettingFilePath)
    ):
        # print('Not lazy load')
        # print('Not lazy load')
        # print('Not lazy load')
        # print('Not lazy load')
        # print('Not lazy load')
        # print('Not lazy load')
        # print('Not lazy load')
        # print('Not lazy load')
        # print('Not lazy load')
        # print('Not lazy load')
        for fallbackSettingInjection in fallbackSettingInjectionList.copy() :
            for settingInjection in settingInjectionList.copy() :
                if (
                    fallbackSettingInjection[SettingHelperHelper.SETTING_KEY] == settingInjection[SettingHelperHelper.SETTING_KEY] and
                    fallbackSettingInjection[SettingHelperHelper.SETTING_NODE_KEY] == settingInjection[SettingHelperHelper.SETTING_NODE_KEY]
                ) :
                    fallbackSettingInjectionList.remove(fallbackSettingInjection)

        # print(f'fallbackSettingInjectionList: {fallbackSettingInjectionList}')
        # print(f'settingInjectionList: {settingInjectionList}')
        settingInjectionList += fallbackSettingInjectionList
        updateSettingTree(settingTree, innerFallbackSettingTree)
        SettingHelperHelper.handleSettingInjectionList(settingInjectionList, settingTree, fallbackSettingTree=innerFallbackSettingTree)
    SettingHelperHelper.handleSettingInjectionList(settingInjectionList, settingTree, fallbackSettingTree=fallbackSettingTree)
    updateSettingTree(settingTree, fallbackSettingTree)
    return settingTree

def updateSettingTree(toUpdateSettingTree, gatheringSettingTree) :
    if ObjectHelper.isNotEmpty(gatheringSettingTree) :
        if ObjectHelper.isNone(toUpdateSettingTree) or StringHelper.isBlank(toUpdateSettingTree) :
            toUpdateSettingTree = {}
        if ObjectHelper.isCollection(gatheringSettingTree) and ObjectHelper.isDictionary(gatheringSettingTree) :
            for key, value in gatheringSettingTree.items() :
                if ObjectHelper.isNotEmpty(value) and ObjectHelper.isNotNone(value):
                    if key not in toUpdateSettingTree or ObjectHelper.isEmpty(toUpdateSettingTree[key]) :
                        # print(f'        key: {key}, value: {value}')
                        toUpdateSettingTree[key] = value
                    else :
                        updateSettingTree(toUpdateSettingTree[key], gatheringSettingTree[key])
                elif key not in toUpdateSettingTree :
                    # print(f'        toUpdateSettingTree: key: {key}, value: {value}')
                    toUpdateSettingTree[key] = value
    return toUpdateSettingTree


def getSetting(nodeKey, settingTree) :
    setting = None
    try :
        setting = SettingHelperHelper.accessTree(nodeKey, settingTree)
    except Exception as exception :
        LogHelper.failure(getSetting, f'Not possible to get {nodeKey} node key. Returning "{setting}" by default', exception)
    return setting if not isinstance(setting, str) else StringHelper.filterString(setting)

def querySetting(keywordQuery, settingTree):
    if StringHelper.isBlank(keywordQuery) or ObjectHelper.isNotDictionary(settingTree) :
        LogHelper.warning(querySetting,f'''Not possible to parse "{settingTree}". It's either is not a dictionary or "{keywordQuery}" keyword query is blank''')
    querySet = {}
    SettingHelperHelper.keepSearching(keywordQuery, settingTree, querySet)
    return querySet

def printSettings(settingTree, name, depth=1, withColors=False):
    withColors = LogHelper.colorsEnabled() ###- activeEnvironmentIsLocal()
    settingKeyColor = SettingHelperHelper.getSettingKeyPrompColor(withColors)
    colonColor = SettingHelperHelper.getSettingColonPrompColor(withColors)
    print(f'{c.NEW_LINE}{settingKeyColor}{c.OPEN_LIST}{name.upper()}{c.CLOSE_LIST}{colonColor}{c.SPACE}{c.COLON}')
    SettingHelperHelper.printNodeTree(
        settingTree,
        depth,
        settingKeyColor = settingKeyColor,
        settingValueColor = SettingHelperHelper.getSettingValuePrompColor(withColors),
        colonColor = colonColor,
        resetColor = SettingHelperHelper.getSettingResetPrompColor(withColors)
    )
    print()
