from numbers import Number
import operator

from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import StringHelper, LogHelper, ReflectionHelper, DateTimeHelper
from python_helper.api.src.helper import ObjectHelperHelper


operator = operator

ASC_ORDER = 'ASC'
DESC_ORDER = 'DESC'


GENERATOR_CLASS_NAME = 'generator'
UNKNOWN_OBJECT_CLASS_NAME = c.UNKNOWN.lower()

METADATA_NAME = 'metadata'

NATIVE_CLASSES = (
    bool,
    int,
    str,
    float,
    bytes,
    type(ObjectHelperHelper.generatorInstance())
)

COLLECTION_CLASSES = (
    list,
    dict,
    tuple,
    set
)

type = type


def strComparator(value):
    # return StringHelper.join([v.replace(c.SPACE, c.DASH) for v in str(value).split(c.NEW_LINE)])
    return str(value)


def simpleEquals(
    expected,
    toAssert
):
    return expected is toAssert if isNone(expected) else expected == toAssert

    
def equals(
    expected,
    toAssert,
    ignoreCollectionOrder = False,
    ignoreKeyList = None,
    ignoreCharactereList = None,
    ignoreAttributeList = None,
    ignoreAttributeValueList = None,
    visitedIdInstances = None,
    muteLogs = True
):
    if isNone(ignoreKeyList):
        ignoreKeyList = []
    if isNone(ignoreCharactereList):
        ignoreCharactereList = []
    if isNone(ignoreAttributeValueList):
        ignoreAttributeValueList = []
    if isNone(ignoreAttributeList):
        ignoreAttributeList = []
    # ignoreAttributeValueList = [*ignoreAttributeValueList, *[c for c in ignoreCharactereList if c not in ignoreAttributeValueList]]
    if isNone(expected) or isNone(toAssert):
        return expected is None and toAssert is None
    if isNativeClass(type(expected)):
        return simpleEquals(expected, toAssert)
    if DateTimeHelper.isNativeDateTime(expected):
        return simpleEquals(expected, toAssert)
    if isNone(visitedIdInstances):
        visitedIdInstances = []
    if isDictionary(expected) and isDictionary(toAssert):
        innerIgnoreCharactereList = [c.SPACE, *ignoreCharactereList]
        filteredSortedExpectedResponseAsString = StringHelper.filterJson(
            str(sortIt(
                filterIgnoreKeyList(expected, ignoreKeyList),
                deepMode=True
            )),
            extraCharacterList=innerIgnoreCharactereList
        )
        filteredSortedToAssertResponseAsString = StringHelper.filterJson(
            str(sortIt(
                filterIgnoreKeyList(toAssert, ignoreKeyList),
                deepMode=True
            )),
            extraCharacterList=innerIgnoreCharactereList
        )
        return simpleEquals(filteredSortedExpectedResponseAsString, filteredSortedToAssertResponseAsString)
    elif isCollection(expected) and isCollection(toAssert):
        areEquals = True
        try:
            if not simpleEquals(len(expected), len(toAssert)):
                first, second = (1, 2) if len(expected)>len(toAssert) else (2, 1)
                raise Exception(f'Argument {first} is longer than argument {second}')
            for a, b in zip(
                list(expected if not ignoreCollectionOrder else sortIt(expected, deepMode=ignoreCollectionOrder)),
                list(toAssert if not ignoreCollectionOrder else sortIt(toAssert, deepMode=ignoreCollectionOrder))
            ):
                areEquals = equals(
                    a,
                    b,
                    ignoreCollectionOrder = ignoreCollectionOrder,
                    ignoreKeyList = ignoreKeyList,
                    ignoreCharactereList = ignoreCharactereList,
                    ignoreAttributeList = ignoreAttributeList,
                    ignoreAttributeValueList = ignoreAttributeValueList,
                    visitedIdInstances = visitedIdInstances,
                    muteLogs = muteLogs
                )
                if not areEquals :
                    break
            return areEquals
        except Exception as exception :
            areEquals = False
            LogHelper.log(equals, f'Different arguments in {expected} and {toAssert}. Returning "{areEquals}" by default', exception=exception)
    else:
        if isNotNone(toAssert):
            if id(toAssert) not in visitedIdInstances:
                areEquals = True
                try:
                    if not muteLogs :
                        LogHelper.prettyPython(equals, f'expected', expected, logLevel = LogHelper.DEBUG, condition=not muteLogs)
                        LogHelper.prettyPython(equals, f'toAssert', toAssert, logLevel = LogHelper.DEBUG, condition=not muteLogs)
                    areEquals = ObjectHelperHelper.leftEqual(
                        expected,
                        toAssert,
                        ignoreCollectionOrder,
                        ignoreKeyList,
                        ignoreCharactereList,
                        ignoreAttributeList,
                        ignoreAttributeValueList,
                        visitedIdInstances,
                        muteLogs = muteLogs
                    ) and ObjectHelperHelper.leftEqual(
                        toAssert,
                        expected,
                        ignoreCollectionOrder,
                        ignoreKeyList,
                        ignoreCharactereList,
                        ignoreAttributeList,
                        ignoreAttributeValueList,
                        visitedIdInstances,
                        muteLogs = muteLogs
                    )
                except Exception as exception :
                    areEquals = False
                    LogHelper.log(equals, f'Different arguments in {expected} and {toAssert}. Returning "{areEquals}" by default', exception=exception)
                visitedIdInstances.append(id(toAssert))
                return areEquals
            else:
                return True
        return simpleEquals(expected, toAssert)
    return simpleEquals(expected, toAssert)


def notEquals(*args, **kwargs):
    return not equals(*args, **kwargs)


def sortIt(thing, deepMode=False, byAttribute: str = None, reverse: bool = False):
    # sorted_x = sorted(x, key=operator.attrgetter('attributeName'))
    # or
    # x.sort(key=operator.attrgetter('attributeName'))
    if isDictionary(thing):
        return {
            key: sortIt(thing[key], deepMode=deepMode, byAttribute=byAttribute, reverse=reverse)
            for key in sortIt([*thing.keys()], reverse=reverse)
        }
    elif isCollection(thing):
        return getSortedCollection(
            [
                sortIt(innerThing, deepMode=deepMode, byAttribute=byAttribute, reverse=reverse)
                for innerThing in thing
            ],
            deepMode = deepMode,
            byAttribute = byAttribute,
            reverse = reverse
        )
    else:
        return thing


def getSortedCollection(thing, deepMode=False, byAttribute: str = None, reverse: bool = False):
    if (
        isNotCollection(thing) or isEmpty(thing)
    ):
        return thing
    return handleComparisson(thing, deepMode=deepMode, byAttribute=byAttribute, reverse=reverse)


def handleComparisson(thing, deepMode=False, byAttribute: str = None, reverse: bool = False):
    try:
        if isNotNone(byAttribute):
            byAttributeAsStringList = (byAttribute if isinstance(byAttribute, str) else ReflectionHelper.getName(byAttribute)).split(c.SPACE)
            parsetAtributeName = byAttributeAsStringList[0]
            reverseIt = reverse if not (
                2 == len(byAttributeAsStringList) and 
                byAttributeAsStringList[-1] in [ASC_ORDER, DESC_ORDER]
            ) else byAttributeAsStringList[-1] == DESC_ORDER
            return sorted(thing, key=operator.attrgetter(parsetAtributeName), reverse=reverseIt)
        return sorted(
            thing,
            key=defaultComparissonHandler(deepMode)
        )
    except:
        return sorted(
            thing,
            key=defaultComparissonHandler(deepMode, deepModeProcessor=strComparator)
        )


def defaultComparissonHandler(deepMode, deepModeProcessor=None):
    return lambda x: (
        x is not None, c.NOTHING if isinstance(x, Number) else type(x).__name__, x if not deepMode else deepSort(x) if isNone(deepModeProcessor) else deepModeProcessor(deepSort(x))
    )


def deepSort(x):
    if isNotSet(x):
        return (
            sortIt(x, deepMode=True)
            if isNotDictionary(x) else getSortedDictionary(x, deepMode=True)
        )
    else:
        for i in x:
            sortIt(i, deepMode=True)
        return x
    

def getDistinctAndOrdered(givenList):
    return deepSort(list(set(givenList)))


def getSortedDictionary(dictionary, deepMode=False):
    for k, v in [
        (
            key,
            sortIt(dictionary.pop(key), deepMode=deepMode)
        )
        for key in sortIt([*dictionary.keys()], deepMode=deepMode)
    ]:
        dictionary[k] = v
    return dictionary


def filterIgnoreKeyList(objectAsDictionary, ignoreKeyList):
    return filterIgnoreKeyListAvoidingRecursion(objectAsDictionary, ignoreKeyList, [])


def filterIgnoreKeyListAvoidingRecursion(objectAsDictionary, ignoreKeyList, visitedInstances):
    dictionaryId = id(objectAsDictionary)
    if isDictionary(objectAsDictionary) and isNotNone(ignoreKeyList) and dictionaryId not in visitedInstances:
        visitedInstances.append(dictionaryId)
        filteredObjectAsDict = {}
        for key, value in objectAsDictionary.items():
            if key not in ignoreKeyList :
                if isDictionary(value):
                    filteredObjectAsDict[key] = filterIgnoreKeyListAvoidingRecursion(value, ignoreKeyList, visitedInstances)
                else:
                    filteredObjectAsDict[key] = objectAsDictionary[key]
        return filteredObjectAsDict
    return objectAsDictionary


def flatMap(lists):
    return [item for sublist in lists for item in sublist]


def isEmpty(thing):
    return StringHelper.isBlank(thing) if isinstance(thing, str) else isNone(thing) or isEmptyCollection(thing)


def isNotEmpty(thing):
    return not isEmpty(thing)


def isEmptyCollection(thing):
    return isCollection(thing) and simpleEquals(0, len(thing))


def isNotEmptyCollection(thing):
    return isCollection(thing) and 0 < len(thing)


def isList(thing):
    return isinstance(thing, list)


def isNotList(thing):
    return not isList(thing)


def isSet(thing):
    return isinstance(thing, set)


def isNotSet(thing):
    return not isSet(thing)


def isTuple(thing):
    return isinstance(thing, tuple)


def isNotTuple(thing):
    return not isTuple(thing)


def isDictionary(thing):
    return isinstance(thing, dict)


def isNotDictionary(thing):
    return not isDictionary(thing)


def isDictionaryClass(thingClass):
    return simpleEquals(dict, thingClass)


def isNotDictionaryClass(thingClass):
    return not isDictionaryClass(thingClass)


def isNone(instance):
    return instance is None


def isNotNone(instance):
    return not isNone(instance)


def isNativeClass(instanceClass):
    return isNotNone(instanceClass) and instanceClass in NATIVE_CLASSES


def isNotNativeClass(instanceClass):
    return not isNativeClass(instanceClass)


def isNativeClassInstance(instance):
    return isNotNone(instance) and (
        isNativeClass(instance.__class__) or
        True in {isinstance(instance, c) for c in NATIVE_CLASSES}
    )


def isNotNativeClassIsntance(instance):
    return not isNativeClassInstance(instance)


def isCollection(instance):
    return isNotNone(instance) and True in {isinstance(instance, c) for c in COLLECTION_CLASSES}


def isNotCollection(instance):
    return not isCollection(instance)


def isNeitherNoneNorBlank(thing):
    return not isNoneOrBlank(thing)


def isNoneOrBlank(thing):
    return isNone(thing) or StringHelper.isBlank(str(thing))


def deleteDictionaryEntry(entryKey, dictionary):
    if entryKey in dictionary:
        dictionary.pop(entryKey)

