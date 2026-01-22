from python_helper.api.src.service import StringHelper, LogHelper, ObjectHelper, EnvironmentHelper, SettingHelper
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.helper import StringHelperHelper

OPEN_SETTING_INJECTION = '${'
CLOSE_SETTING_INJECTION = '}'

SETTING_KEY = 'SETTING_KEY'
SETTING_VALUE = 'SETTING_VALUE'
SETTING_NODE_KEY = 'SETTING_NODE_KEY'

def getFilteredSetting(settingKey, settingValue, nodeKey, settingTree) :
    # print(f'getFilteredSetting: settingKey: {settingKey}, settingValue: "{settingValue}", type: {type(settingValue)}')
    if StringHelper.isNotBlank(settingValue) :
        settingEvaluationList = settingValue.split(c.COLON)
        if len(settingEvaluationList) > 1 :
            defaultSettingValue = c.COLON.join(settingEvaluationList[1:]).strip()
            # print(f'    defaultSettingValue: {defaultSettingValue}')
        else :
            # defaultSettingValue = c.NONE
            defaultSettingValue = settingValue
        if isSettingInjection(defaultSettingValue) :
            # print(f'        ----> getSettingInjectionValue: {settingKey} -> is setting injection: defaultSettingValue: {defaultSettingValue}, type: {type(settingValue)}')
            return getSettingInjectionValue(settingKey, defaultSettingValue, nodeKey, settingTree)
        # print(f'        ----> getValue: settingKey: {settingKey} -> not setting injection: defaultSettingValue: {defaultSettingValue}, type: {type(settingValue)}')
        return getValue(StringHelper.filterString(defaultSettingValue), ignoreCollections=True)
    # print(f'        ----> settingValue: settingKey: {settingKey} -> straight: settingValue: {settingValue}, type: {type(settingValue)}')
    return settingValue

def lineAproved(settingLine) :
    approved = True
    if c.NEW_LINE == settingLine  :
        approved = False
    if c.HASH_TAG in settingLine :
        filteredSettingLine = StringHelper.filterString(settingLine)
        if filteredSettingLine is None or c.NOTHING == filteredSettingLine or c.NEW_LINE == filteredSettingLine :
            approved = False
    return approved

def nextValidLineIsAtTheSameDepthOrLess(currentDepth, line, allSettingLines) :
    ###- currentDepth == depth and
    if line + 1 == len(allSettingLines) :
        return True
    for settingLine in allSettingLines[line+1:] :
        if lineAproved(settingLine) :
            # print(f'currentDepth: {currentDepth}, line: {line}, isValid: {currentDepth == getDepth(settingLine)}, settingLine: {settingLine}')
            return currentDepth >= getDepth(settingLine)
    # print(f'currentDepth: {currentDepth}, line: {line}, isValid: {False}')
    return False

def updateSettingTreeAndReturnNodeKey(settingKey, settingValue, nodeKey, settingTree, isSameDepth) :
    # print(f'nodeKey: {nodeKey}, settingKey: {settingKey}')
    updateSettingValue(settingKey, settingValue, nodeKey, settingTree, isSameDepth=isSameDepth)
    if not isSettingValue(settingValue) :
        if c.NOTHING == nodeKey :
            nodeKey += f'{settingKey}'
        else :
            nodeKey += f'{c.DOT}{settingKey}'
    return nodeKey

def accessTree(nodeKey,tree) :
    if ObjectHelper.isNotNone(tree) :
        strippedNodeKey = nodeKey.strip()
        if ObjectHelper.isEmpty(nodeKey) :
            returnTree = None
            try :
                returnTree = StringHelper.filterString(tree)
            except Exception as exception :
                LogHelper.failure(accessTree, f'Failed to get filtered string from {tree} tree. Returning it the way it is by default', exception)
                returnTree = tree
            return returnTree
        elif isinstance(nodeKey,str) :
            nodeKeyList = nodeKey.split(c.DOT)
            if len(nodeKeyList) == 1 :
                 nextNodeKey = c.NOTHING
            else :
                nextNodeKey = c.DOT.join(nodeKeyList[1:])
            return accessTree(nextNodeKey,tree.get(nodeKeyList[0]))

def safelyAccessTree(nodeKey, settingTree) :
    setting = None
    try :
        setting = accessTree(nodeKey,settingTree)
    except Exception as exception :
        LogHelper.log(safelyAccessTree, f'Not possible to safely access "{nodeKey}" node key while looping through setting tree. Returning "{setting}" by default', exception=exception)
    return setting

def updateSettingValue(
    settingKey,
    settingValue,
    nodeKey,
    settingTree,
    isSameDepth = False,
    isSettingInjection = False
) :
    # print(f'settingKey: {settingKey}, settingValue: {settingValue}, nodeKey: {nodeKey}, settingTree: {settingTree}, isSameDepth: {isSameDepth}')
    if StringHelper.isNotBlank(settingKey) and ObjectHelper.isNotNone(settingKey) :
        # print(f'accessTree({nodeKey},{settingTree})[{settingKey}]: {accessTree(nodeKey,settingTree)}[{settingKey}]')
        # print(f'type(accessTree(nodeKey,settingTree)): {type(accessTree(nodeKey,settingTree))}')

        accessTree(nodeKey,settingTree)[settingKey] = getSettingValueOrNewNode(
            nodeKey,
            settingKey,
            settingValue,
            isSameDepth=isSameDepth,
            isSettingInjection=isSettingInjection
        )
    elif StringHelper.isNotBlank(nodeKey) and ObjectHelper.isNotNone(nodeKey) :
        splittedNodeKey = nodeKey.split(c.DOT)
        if 1 < len(splittedNodeKey) :
            accessSettingKey = splittedNodeKey[-1]
            accessNodeKey = c.DOT.join(splittedNodeKey[:-1])
        else :
            accessSettingKey = splittedNodeKey[-1]
            accessNodeKey = None
        accessTree(accessNodeKey,settingTree)[accessSettingKey] = getSettingValueOrNewNode(
            nodeKey,
            settingKey,
            settingValue,
            isSameDepth=isSameDepth,
            isSettingInjection=isSettingInjection
        )
    else :
        errorMessage = 'Node key and setting key cannot be None at the same time'
        exception = Exception(errorMessage)
        LogHelper.error(updateSettingValue, f'Error parsing settingKey: "{settingKey}", settingValue: {settingValue}, nodeKey: {nodeKey}, settingTree: {StringHelper.prettyPython(settingTree)}', errorMessage)
        raise exception

def getDepth(settingLine) :
    depthNotFount = True
    depth = 0
    while not settingLine[depth] == c.NEW_LINE and depthNotFount:
        if settingLine[depth] == c.SPACE :
            depth += 1
        else :
            depthNotFount = False
    return depth

def settingTreeInnerLoop(
    settingLine,
    nodeKey,
    settingTree,
    longStringCapturing,
    quoteType,
    longStringList,
    settingInjectionList,
    lazyLoad,
    isSameDepth
) :
    # print(f'settingTreeInnerLoop: settingLine: {settingLine}')
    # print(f'settingTreeInnerLoop: nodeKey: {nodeKey}')
    # print(f'settingTreeInnerLoop: settingTree: {settingTree}')
    # print(f'    isSameDepth: {isSameDepth}')
    settingKey, settingValue = getAttributeKeyValue(settingLine)
    # print(f'    settingKey: {settingKey}, settingValue: {settingValue}')
    # print(f'    settingLine: {settingLine}')

    if containsSettingInjection(settingValue) :
        try :
            settingKey, settingValue, nodeKey, longStringCapturing, quoteType, longStringList = handleSettingInjection(
                settingKey,
                settingValue,
                nodeKey,
                settingTree,
                longStringCapturing,
                quoteType,
                longStringList,
                settingInjectionList,
                lazyLoad,
                isSameDepth
            )
        except Exception as exception :
            LogHelper.log(settingTreeInnerLoop, f'Not possible to handle association of "{nodeKey}{c.DOT}{settingKey}" setting key to "{settingValue}" setting value', exception=exception)
            settingInjectionList.append({
                SETTING_KEY : settingKey,
                SETTING_VALUE : settingValue,
                SETTING_NODE_KEY : nodeKey
            })
        # print(f'    if -> return {settingKey}, {settingValue}, {nodeKey}, {longStringCapturing}, {quoteType}, {longStringList}')
        return settingKey, settingValue, nodeKey, longStringCapturing, quoteType, longStringList
    else :
        # print(f'    nodeKey: {nodeKey}')
        settingKey, filteredSettingValue, nodeKey, longStringCapturing, quoteType, longStringList = handleLongStringOrSetting(
            settingKey,
            settingValue,
            nodeKey,
            settingTree,
            longStringCapturing,
            quoteType,
            longStringList,
            settingInjectionList,
            isSameDepth
        )
        # print(f'----------> nodeKey: {nodeKey}')
        # print(f'    else -> return {settingKey}, {settingValue}, {nodeKey}, {longStringCapturing}, {quoteType}, {longStringList}')
        return settingKey, filteredSettingValue, nodeKey, longStringCapturing, quoteType, longStringList

def handleSettingInjection(
    settingKey,
    settingValue,
    nodeKey,
    settingTree,
    longStringCapturing,
    quoteType,
    longStringList,
    settingInjectionList,
    lazyLoad,
    isSameDepth
) :
    # print(f'handleSettingInjection: settingKey: {settingKey}, settingValue: {settingValue}, settingInjectionList: {settingInjectionList}')
    if isSettingInjection(settingValue) :
        if lazyLoad :
            settingInjectionList.append({
                SETTING_KEY : settingKey,
                SETTING_VALUE : settingValue,
                SETTING_NODE_KEY : nodeKey
            })
            return settingKey, settingValue, nodeKey, longStringCapturing, quoteType, longStringList
        else :
            settingValue = getSettingInjectionValue(settingKey, settingValue, nodeKey, settingTree)
    if containsSettingInjection(settingValue) :
        settingInjectionList.append({
            SETTING_KEY : settingKey,
            SETTING_VALUE : settingValue,
            SETTING_NODE_KEY : nodeKey
        })
        return settingKey, settingValue, nodeKey, longStringCapturing, quoteType, longStringList
    return handleLongStringOrSetting(
        settingKey,
        settingValue,
        nodeKey,
        settingTree,
        longStringCapturing,
        quoteType,
        longStringList,
        settingInjectionList,
        isSameDepth
    )

def handleSettingInjectionList(settingInjectionList, settingTree, fallbackSettingTree=None) :
    # print(f'handleSettingInjectionList: settingTree: {settingTree}')
    if ObjectHelper.isNotEmptyCollection(settingInjectionList) and ObjectHelper.isNotNone(settingTree) :
        try :
            done, stuck = handleSettingInjectionListLoop(
                False,
                False,
                settingTree,
                settingInjectionList,
                fallbackSettingTree,
                getSettingInjectionValueIgnoringFallbackSettingTree,
                verifyer = verifyDefaultSettingInjectionListHandler
            )
        except Exception as exception :
            LogHelper.error(handleSettingInjectionList,'Not possible to load setting injections properly',exception)
            raise exception

def lazillyHandleSettingInjectionList(settingInjectionList, settingTree, fallbackSettingTree=None) :
    if ObjectHelper.isNotEmptyCollection(settingInjectionList) and ObjectHelper.isNotNone(settingTree) :
        try :
            done, stuck = handleSettingInjectionListLoop(
                False,
                False,
                settingTree,
                settingInjectionList,
                fallbackSettingTree,
                getSettingInjectionValueIgnoringFallbackSettingTree,
                verifyer = None
            )
        except Exception as exception :
            LogHelper.error(handleSettingInjectionList,'Not possible to lazilly load setting injections properly',exception)
            raise exception

################################################################################
################################################################################
################################################################################

def handleSettingInjectionListLoop(
    done,
    stuck,
    settingTree,
    settingInjectionList,
    fallbackSettingTree,
    handler,
    verifyer = None
) :
    # print(f'handleSettingInjectionListLoop: handler: {handler}')
    # print(f'handleSettingInjectionListLoop: settingTree: {settingTree}')
    while not done and not stuck :
        stuck = True
        isSettingInjectionCount = 0
        containsSettingInjectionCount = 0
        for settingInjection in settingInjectionList.copy() :
            done, stuck, isSettingInjectionCount, containsSettingInjectionCount = handleSettingInjectionListByCallingHandler(
                done,
                stuck,
                isSettingInjectionCount,
                containsSettingInjectionCount,
                settingInjection,
                settingTree,
                settingInjectionList,
                fallbackSettingTree,
                handler
            )
        if ObjectHelper.isNotNone(verifyer) :
            verifyer(done, stuck, isSettingInjectionCount, containsSettingInjectionCount, settingTree, settingInjectionList, fallbackSettingTree)
    # print(f'handleSettingInjectionListLoop: returning settingTree: {settingTree}')
    return done, stuck

def verifyDefaultSettingInjectionListHandler(
    done,
    stuck,
    isSettingInjectionCount,
    containsSettingInjectionCount,
    settingTree,
    settingInjectionList,
    fallbackSettingTree
) :
    if 0 == len(settingInjectionList) :
        done = True
    elif stuck :
        stuck = False
        done, stuck = handleSettingInjectionListLoop(
            done,
            stuck,
            settingTree,
            settingInjectionList,
            fallbackSettingTree,
            safelyGetSettingInjectionValue,
            verifyer = None
        )
        if 0 == len(settingInjectionList) :
            done = True
        elif stuck :
            LogHelper.setting(verifyDefaultSettingInjectionListHandler, f'Parsed settings: {StringHelper.prettyPython(settingTree)}')
            notParsedSettingInjectionDictionary = {}
            for settingInjection in settingInjectionList :
                notParsedSettingInjectionDictionary[f'{settingInjection[SETTING_NODE_KEY]}{c.DOT}{settingInjection[SETTING_KEY]}'] = (settingInjection)
            if 0 == isSettingInjectionCount and 0 == containsSettingInjectionCount :
                raise Exception(f'Circular reference detected in following setting injections: {StringHelper.prettyPython(notParsedSettingInjectionDictionary)}{c.NEW_LINE}FallbackSettingTree: {StringHelper.prettyPython(fallbackSettingTree)}{c.NEW_LINE}SettingTree: {StringHelper.prettyPython(settingTree)}')
            elif not 0 == len(settingInjectionList) :
                raise Exception(f'Not possible to parse the following setting injections: {StringHelper.prettyPython(notParsedSettingInjectionDictionary)}{c.NEW_LINE}FallbackSettingTree: {StringHelper.prettyPython(fallbackSettingTree)}{c.NEW_LINE}SettingTree: {StringHelper.prettyPython(settingTree)}')

def handleSettingInjectionListByCallingHandler(
    done,
    stuck,
    isSettingInjectionCount,
    containsSettingInjectionCount,
    settingInjection,
    settingTree,
    settingInjectionList,
    fallbackSettingTree,
    handler
) :
    # print()
    # print()
    # print(f'handleSettingInjectionListByCallingHandler: handler: {handler}')
    # print(f'handleSettingInjectionListByCallingHandler: settingTree: {settingTree}')
    try :
        if isSettingInjection(settingInjection[SETTING_VALUE]) :
            settingInjection[SETTING_VALUE] = handler(
                settingInjection[SETTING_KEY],
                settingInjection[SETTING_VALUE],
                settingInjection[SETTING_NODE_KEY],
                settingTree,
                fallbackSettingTree = fallbackSettingTree
            )
            settingInjectionArgs = list(settingInjection.values()) + [settingTree]
            updateSettingValue(*settingInjectionArgs, isSettingInjection=True)
            if not containsSettingInjection(settingInjection[SETTING_VALUE]) :
                settingInjectionList.remove(settingInjection)
                isSettingInjectionCount += 1
            stuck = False
        elif containsSettingInjection(settingInjection[SETTING_VALUE]) :
            settingInjectionListFromSettingValue = getSettingInjectionListFromSettingValue(settingInjection[SETTING_VALUE])
            newSettingInjection = settingInjection[SETTING_VALUE]
            for settingValue in settingInjectionListFromSettingValue :
                newSettingValue = handler(
                    settingInjection[SETTING_KEY],
                    settingValue,
                    settingInjection[SETTING_NODE_KEY],
                    settingTree,
                    fallbackSettingTree = fallbackSettingTree
                )
                if ObjectHelper.isList(newSettingInjection) :
                    for index, element in enumerate(newSettingInjection):
                        if settingValue == element :
                            newSettingInjection[index] = newSettingValue
                else :
                    newSettingInjection = newSettingInjection.replace(settingValue,str(newSettingValue))
            settingInjection[SETTING_VALUE] = newSettingInjection
            settingInjectionArgs = list(settingInjection.values()) + [settingTree]
            updateSettingValue(*settingInjectionArgs, isSettingInjection=True)
            if not containsSettingInjection(settingInjection[SETTING_VALUE]) :
                settingInjectionList.remove(settingInjection)
                containsSettingInjectionCount += 1
            stuck = False
    except Exception as exception :
        LogHelper.log(handleSettingInjectionListByCallingHandler, f'Ignored exception while handling {StringHelper.prettyPython(settingInjection)} setting injection list', exception=exception)
    # print(f'handleSettingInjectionListByCallingHandler: returning settingTree: {settingTree}')
    return done, stuck, isSettingInjectionCount, containsSettingInjectionCount

################################################################################
################################################################################
################################################################################

def appendSettingKey(nodeKey,settingKey):
    if StringHelper.isNotBlank(nodeKey) :
        if StringHelper.isNotBlank(settingKey) :
            return f'{nodeKey}{c.DOT}{settingKey}'
        else :
            return nodeKey
    elif StringHelper.isNotBlank(settingKey) :
        return settingKey
    else :
        return None

def safelyGetSettingInjectionValue(settingKey, settingValue, nodeKey, settingTree, fallbackSettingTree=None) :
    exception = None
    newSettingValue = None
    try :
        newSettingValue = getSettingInjectionValue(settingKey, settingValue, nodeKey, settingTree)
    except Exception as e :
        exception = e
        LogHelper.log(safelyGetSettingInjectionValue, f'Not possible to load "{settingKey}" setting key from setting tree. Now trying to load it from fallback setting tree', exception=exception)
    if ObjectHelper.isNone(newSettingValue) and ObjectHelper.isNotNone(fallbackSettingTree) :
        return getSettingInjectionValue(settingKey, settingValue, nodeKey, fallbackSettingTree)
    if ObjectHelper.isNotNone(exception) :
        raise exception
    return newSettingValue

def handleLongStringOrSetting(
    settingKey,
    settingValue,
    nodeKey,
    settingTree,
    longStringCapturing,
    quoteType,
    longStringList,
    settingInjectionList,
    isSameDepth
) :
    # print(f'handleLongStringOrSetting: settingValue: {settingValue}')
    if StringHelper.isLongString(settingValue) :
        longStringCapturing = True
        splitedSettingValueAsString = settingValue.split(c.TRIPLE_SINGLE_QUOTE)
        if c.TRIPLE_SINGLE_QUOTE in settingValue and splitedSettingValueAsString and c.TRIPLE_DOUBLE_QUOTE not in splitedSettingValueAsString[0] :
            quoteType = c.TRIPLE_SINGLE_QUOTE
        else :
            quoteType = c.TRIPLE_DOUBLE_QUOTE
        longStringList = [settingValue + c.NEW_LINE]
    else :
        nodeKey = updateSettingTreeAndReturnNodeKey(settingKey, settingValue, nodeKey, settingTree, isSameDepth)
    filteredSettingValue = getFilteredSetting(settingKey, settingValue, nodeKey, settingTree)
    # print(f'handleLongStringOrSetting: settingKey: {settingKey}, settingValue: {settingValue}, type: {type(settingValue)} filteredSettingValue: {filteredSettingValue}, type: {type(settingValue)}')
    # print(longStringCapturing, quoteType, longStringList)
    return settingKey, filteredSettingValue, nodeKey, longStringCapturing, quoteType, longStringList

def getAttributeKeyValue(settingLine) :
    settingKey = getAttributeKey(settingLine)
    settingValue = getAttibuteValue(settingLine)
    return settingKey,settingValue

def getAttributeKey(settingLine) :
    possibleKey = StringHelper.filterString(settingLine)
    return possibleKey.split(c.COLON)[0].strip()

def getAttibuteValue(settingLine) :
    possibleValue = StringHelper.filterString(settingLine)
    return getValue(c.COLON.join(possibleValue.split(c.COLON)[1:]))

def isComposedUnwrapedInjectionValue(settingValue):
    unwrapedSettingInjectionValue = getUnwrappedSettingInjection(settingValue)
    return isSettingInjection(settingValue) and (
        not c.COLON_SPACE in unwrapedSettingInjectionValue and
        c.COLON in unwrapedSettingInjectionValue and
        ObjectHelper.equals(1, unwrapedSettingInjectionValue.count(c.COLON)) and (
            StringHelper.isNotBlank(unwrapedSettingInjectionValue.split(c.COLON)[0]) or
            StringHelper.isNotBlank(unwrapedSettingInjectionValue.split(c.COLON)[-1])
        ) and (
            StringHelper.isBlank(unwrapedSettingInjectionValue.split(c.COLON)[0]) or
            unwrapedSettingInjectionValue.split(c.COLON)[0].isupper()
        ) and (
            StringHelper.isBlank(unwrapedSettingInjectionValue.split(c.COLON)[-1]) or
            unwrapedSettingInjectionValue.split(c.COLON)[-1].islower()
        )
    )

def isSettingKey(possibleSettingKey) :
    return ObjectHelper.isNotNone(possibleSettingKey) and (
            isinstance(possibleSettingKey, str) and
            not isSettingInjection(possibleSettingKey) and
            not c.COLON in possibleSettingKey and
            not f'{2 * c.DASH}' in possibleSettingKey and
            possibleSettingKey == possibleSettingKey.lower()
        )

def isSettingValue(settingValue) :
    return ObjectHelper.isNotEmpty(settingValue) or ObjectHelper.isCollection(settingValue)

def getSettingValueOrNewNode(nodeKey, settingKey, settingValue, isSameDepth=False, isSettingInjection=False) :
    isActuallyASettingValue = isSettingValue(settingValue)
    # print(f'settingValue: {settingValue}, isActuallyASettingValue: {isActuallyASettingValue}, isSameDepth: {isSameDepth}')
    if not isActuallyASettingValue and isSameDepth :
        raise Exception(f'The key: "{nodeKey}{c.DOT}{settingKey}" has the following invalid value: "{settingValue}"')
    return settingValue if isActuallyASettingValue else None if isSettingInjection or isSameDepth else dict()

def getValue(value, ignoreCollections=False) :
    filteredValue = StringHelper.filterString(value)
    if isSettingValue(filteredValue) :
        if not ignoreCollections:
            if StringHelper.isNotBlank(filteredValue) :
                if c.OPEN_LIST == filteredValue[0] :
                    return getList(filteredValue)
                elif c.OPEN_TUPLE == filteredValue[0] :
                    return getTuple(filteredValue)
                elif c.OPEN_DICTIONARY == filteredValue[0] :
                    return getDictionary(filteredValue)
                elif c.OPEN_SET == filteredValue[0] :
                    return getSet(filteredValue)
        parsedValue = None
        try :
            parsedValue = int(filteredValue)
        except :
            try :
                parsedValue = float(filteredValue)
            except :
                try :
                    parsedValue = filteredValue
                    if not filteredValue is None :
                        if filteredValue == c.TRUE :
                            parsedValue = True
                        elif filteredValue == c.FALSE :
                            parsedValue = False
                except:
                    parsedValue = filteredValue
        return parsedValue
    return filteredValue

def getList(value) :
    roughtValueList = value[1:-1].split(c.COMA)
    valueList = list()
    for value in roughtValueList :
        gottenValue = getValue(value)
        if ObjectHelper.isNotEmpty(gottenValue) :
            valueList.append(gottenValue)
    return valueList

def getTuple(value) :
    return tuple(getList(value))

def getSet(value) :
    roughtValueList = value[1:-1].split(c.COMA)
    valueSet = set()
    for value in roughtValueList :
        gottenValue = getValue(value)
        if ObjectHelper.isNotNone(gottenValue) :
            valueSet.add(gottenValue)
    return valueSet

def getDictionary(value) :
    splitedValue = value[1:-1].split(c.COLON)
    keyList = []
    for index in range(len(splitedValue) -1) :
        keyList.append(StringHelper.filterString(splitedValue[index].split(c.COMA)[-1].strip()))
    valueList = []
    valueListSize = len(splitedValue) -1
    for index in range(valueListSize) :
        if index == valueListSize -1 :
            correctValue = splitedValue[index+1].strip()
        else :
            correctValue = c.COMA.join(splitedValue[index+1].split(c.COMA)[:-1]).strip()
        valueList.append(getValue(correctValue))
    resultantDictionary = dict()
    for index in range(len(keyList)) :
        resultantDictionary[keyList[index]] = valueList[index]
    return resultantDictionary

def getSettingInjectionListFromSettingValue(settingValue) :
    if ObjectHelper.isList(settingValue) :
        allElements = []
        for element in settingValue :
            elements = getSettingInjectionListFromSettingValue(element)
            if ObjectHelper.isList(elements) :
                allElements += elements
        return allElements
    elif ObjectHelper.isNotNone(settingValue) and StringHelper.isNotBlank(settingValue) :
        splitedSettingValue = settingValue.split(OPEN_SETTING_INJECTION)
        settingValueList = []
        completeSettingValue = c.NOTHING
        for segment in splitedSettingValue if settingValue.startswith(OPEN_SETTING_INJECTION) else splitedSettingValue[1:] :
            if ObjectHelper.isNotNone(segment) and StringHelper.isNotBlank(segment) :
                if ObjectHelper.isNotNone(segment.count(c.OPEN_DICTIONARY)) and not segment.count(c.OPEN_DICTIONARY) == segment.count(c.CLOSE_DICTIONARY) and 0 < segment.count(c.OPEN_DICTIONARY) :
                    completeSettingValue += segment
                else :
                    splitedSegment = segment.split(CLOSE_SETTING_INJECTION)
                    completeSettingValue += splitedSegment[0]
                    if ObjectHelper.isNotNone(completeSettingValue) and StringHelper.isNotBlank(completeSettingValue) :
                        settingValueList.append(f'{OPEN_SETTING_INJECTION}{completeSettingValue}{CLOSE_SETTING_INJECTION}')
                    completeSettingValue = c.NOTHING
        return settingValueList
    return []

def containsValidSettingInjection(settingValue) :
    if ObjectHelper.isNotNone(settingValue) and StringHelper.isNotBlank(settingValue) and 0 < settingValue.count(OPEN_SETTING_INJECTION) and settingValue.count(c.OPEN_DICTIONARY) == settingValue.count(c.CLOSE_DICTIONARY) :
        splitedSettingValue = settingValue.split(OPEN_SETTING_INJECTION)
        settingValueList = []
        completeSettingValue = c.NOTHING
        for segment in splitedSettingValue if settingValue.startswith(OPEN_SETTING_INJECTION) else splitedSettingValue[1:] :
            if ObjectHelper.isNotNone(segment) :
                if ObjectHelper.isNotNone(segment.count(c.OPEN_DICTIONARY)) and not segment.count(c.OPEN_DICTIONARY) == segment.count(c.CLOSE_DICTIONARY) and 0 < segment.count(c.OPEN_DICTIONARY) :
                    completeSettingValue += segment
                else :
                    splitedSegment = segment.split(CLOSE_SETTING_INJECTION)
                    completeSettingValue += splitedSegment[0]
                    settingValueList.append(f'{OPEN_SETTING_INJECTION}{completeSettingValue}{CLOSE_SETTING_INJECTION}')
                    completeSettingValue = c.NOTHING
        return len(splitedSettingValue) == len(settingValueList) if settingValue.startswith(OPEN_SETTING_INJECTION) else len(splitedSettingValue) == len(settingValueList) + 1
    elif ObjectHelper.isList(settingValue) :
        return containsValidSettingInjection(str(settingValue))
    return False

def isSettingInjection(settingValue) :
    return ObjectHelper.isNotNone(settingValue) and (
        isinstance(settingValue, str) and
        settingValue.startswith(OPEN_SETTING_INJECTION) and
        settingValue.endswith(CLOSE_SETTING_INJECTION) and
        containsOnlyOneSettingInjection(settingValue)
    )

def containsSettingInjection(settingValue) :
    return False if not containsValidSettingInjection(settingValue) else 0 < len(getSettingInjectionListFromSettingValue(settingValue))

def containsOnlyOneSettingInjection(settingValue) :
    return False if not containsValidSettingInjection(settingValue) else 1 == len(getSettingInjectionListFromSettingValue(settingValue))

def getSettingInjectionValueIgnoringFallbackSettingTree(settingKey, settingValue, nodeKey, settingTree, fallbackSettingTree=None) :
    return getSettingInjectionValue(settingKey, settingValue, nodeKey, settingTree)

def getSettingInjectionValue(settingKey, settingValue, nodeKey, settingTree, lazyLoad=False) :
    isComposedInjectionValue = isComposedUnwrapedInjectionValue(settingValue)
    unwrapedSettingInjectionValue = getUnwrappedSettingInjection(settingValue)
    # print(f'---> getSettingInjectionValue: settingKey: {settingKey}, unwrapedSettingInjectionValue: {unwrapedSettingInjectionValue}, settingTree: {settingTree}')
    existingValue = None
    try:
        # print(f'nodeKey: {nodeKey}, settingKey: {settingKey}, settingTree: {settingTree}')
        existingValue = safelyAccessTree(nodeKey,settingTree).get(settingKey)
        # print(f'existingValue: {existingValue}')
    except Exception as exception:
        # print(f'nodeKey: {nodeKey}, settingKey: {settingKey}, settingTree: {settingTree}, safelyAccessTree(nodeKey,settingTree): {safelyAccessTree(nodeKey,settingTree)}')
        LogHelper.log(getSettingInjectionValue, 'Error while evaluating existing value', exception)
    if ObjectHelper.isNotEmpty(existingValue) and not isSettingInjection(existingValue) and not containsSettingInjection(existingValue) and not isSettingKey(existingValue):
        # if ObjectHelper.isNotEmpty(existingValue) and not isSettingInjection(existingValue) and not containsSettingInjection(existingValue) and not isSettingKey(existingValue) and not (isinstance(existingValue) and existingValue.startswith(c.COLON)):
        # print(f'---> ---> first return {existingValue}')
        return existingValue
    if isSettingKey(unwrapedSettingInjectionValue) :
        selfReferenceSettingValue = safelyAccessTree(unwrapedSettingInjectionValue, settingTree)
        if ObjectHelper.isNone(selfReferenceSettingValue) :
            if lazyLoad:
                LogHelper.log(getSettingInjectionValue, f'Not possible to associate "{nodeKey}{c.DOT}{settingKey}" key to "{unwrapedSettingInjectionValue}" value. "{unwrapedSettingInjectionValue}" value is either not defined or not delayed defined. Example: "{OPEN_SETTING_INJECTION}:{nodeKey}{c.DOT}{settingKey}{CLOSE_SETTING_INJECTION}"')
                return unwrapedSettingInjectionValue
            raise Exception(f'Not possible to associate "{nodeKey}{c.DOT}{settingKey}" key to "{unwrapedSettingInjectionValue}" value. "{unwrapedSettingInjectionValue}" value is either not defined or not delayed defined. Example: "{OPEN_SETTING_INJECTION}:{nodeKey}{c.DOT}{settingKey}{CLOSE_SETTING_INJECTION}"')
        # print(f'---> ---> second return {selfReferenceSettingValue}')
        return selfReferenceSettingValue
    environmentKey = unwrapedSettingInjectionValue.split(c.COLON)[0]
    environmentValue = EnvironmentHelper.get(environmentKey)
    # print()
    # print()
    # print(f'getSettingInjectionValue: {settingKey} --> {environmentKey}: getValue(environmentValue): {getValue(environmentValue)}, type: {type(getValue(environmentValue))}') ##remove
    # print(f'getSettingInjectionValue: {settingKey} --> {environmentKey}: environmentValue: {environmentValue}, type: {type(environmentValue)}') ##remove
    if environmentValue :
        # print(f'---> ---> third return {getValue(environmentValue, ignoreCollections=True)}')
        return getValue(environmentValue, ignoreCollections=True)
        # return environmentValue
    elif isComposedInjectionValue :
        filteredSettingInjection = getFilteredSetting(settingKey, unwrapedSettingInjectionValue, nodeKey, settingTree)
        # print(f'---> ---> filteredSettingInjection: {filteredSettingInjection}')
        if ObjectHelper.isNeitherNoneNorBlank(filteredSettingInjection) :
            reWrappedSettingInjectionValue = f'{OPEN_SETTING_INJECTION}{filteredSettingInjection}{CLOSE_SETTING_INJECTION}'
            # print(f'---> ---> settingKey: {settingKey}, reWrappedSettingInjectionValue: {reWrappedSettingInjectionValue}, nodeKey: {nodeKey}, settingTree: {settingTree}')
            # print(f'---> ---> fourth return {getSettingInjectionValue(settingKey, reWrappedSettingInjectionValue, nodeKey, settingTree)}')
            return getSettingInjectionValue(settingKey, reWrappedSettingInjectionValue, nodeKey, settingTree, lazyLoad=True)
    # print(f'---> ---> settingKey: {settingKey}, unwrapedSettingInjectionValue: {unwrapedSettingInjectionValue}, nodeKey: {nodeKey}, settingTree: {settingTree}')
    # print(f'---> ---> fith return {getFilteredSetting(settingKey, unwrapedSettingInjectionValue, nodeKey, settingTree)}')
    return getFilteredSetting(settingKey, unwrapedSettingInjectionValue, nodeKey, settingTree)

def getUnwrappedSettingInjection(settingValue) :
    if isSettingInjection(settingValue) :
        return settingValue[2:-1]
    return settingValue

def keepSearching(keywordQuery,tree,querySet,history=None):
    if ObjectHelper.isDictionary(tree) :
        for key in tree.keys() :
            if StringHelper.isNotBlank(history) :
                newHistory = f'{history}.{key}'
            else :
                newHistory = f'{key}'
            if StringHelper.isNotBlank(keywordQuery) and key == keywordQuery :
                querySet[newHistory] = tree[key]
            keepSearching(keywordQuery,tree[key],querySet,history=newHistory)

def printNodeTree(
        tree,
        depth,
        settingKeyColor=c.NOTHING,
        settingValueColor=c.NOTHING,
        colonColor=c.NOTHING,
        resetColor=c.NOTHING
    ):
    depthSpace = c.NOTHING
    for nodeDeep in range(depth) :
        depthSpace += f'{c.TAB_UNITS * c.SPACE}'
    depth += 1
    for node in list(tree) :
        if ObjectHelper.isDictionary(tree[node]) :
            print(f'{depthSpace}{settingKeyColor}{node}{colonColor}{c.SPACE}{c.COLON}')
            printNodeTree(
                tree[node],
                depth,
                settingKeyColor=settingKeyColor,
                settingValueColor=settingValueColor,
                colonColor=colonColor,
                resetColor=resetColor
            )
        else :
            print(f'{depthSpace}{settingKeyColor}{node}{colonColor}{c.SPACE}{c.COLON_SPACE}{settingValueColor}{tree[node]}{resetColor}')

def getSettingKeyPrompColor(withColors) :
    return c.DARK_MAGENTA if withColors else c.NOTHING

def getSettingValuePrompColor(withColors) :
    return c.DARK_YELLOW if withColors else c.NOTHING

def getSettingColonPrompColor(withColors) :
    return c.BRIGHT_BLACK if withColors else c.NOTHING

def getSettingResetPrompColor(withColors) :
    return c.DEFAULT_COLOR if withColors else c.NOTHING
