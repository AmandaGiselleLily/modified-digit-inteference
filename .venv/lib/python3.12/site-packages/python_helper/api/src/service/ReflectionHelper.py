import inspect, functools
from python_helper.api.src.domain  import Constant as c
from python_helper.api.src.service import LogHelper, ObjectHelper, StringHelper, RandomHelper, EnvironmentHelper


MAXIMUN_ARGUMENTS = 20

UNKNOWN_TYPE_NAME = f'{c.UNKNOWN.lower()} type'
UNDEFINED = 'undefined'

NONE_VALUE_NAME = str(None)

class ThisIsAClass:
    def thisIsAMethod():
        ...

def thisIsAFunction():
    ...

METHOD_TYPE_NAMES = (
    c.TYPE_METHOD
    , c.TYPE_BUILTIN_FUNCTION_OR_METHOD
    , type(thisIsAFunction).__name__ ###- it cannot be a function ###- @staticmethod clashes with @Test assuming it
)


def hasAttributeOrMethod(instance, name):
    return False if ObjectHelper.isNone(instance) or ObjectHelper.isNone(name) else hasattr(instance, name)


def getAttributeOrMethod(instance, name, muteLogs=False, default=None):
    attributeOrMethodInstance = None
    if ObjectHelper.isNotNone(instance) and ObjectHelper.isNotNone(name):
        try :
            attributeOrMethodInstance = default if not hasattr(instance, name) else getattr(instance, name)
        except Exception as exception :
            if not muteLogs :
                LogHelper.warning(getAttributeOrMethod, f'Not possible to get "{name}" from "{getClassName(instance, typeClass=c.TYPE_CLASS, muteLogs=muteLogs) if ObjectHelper.isNotNone(instance) else instance}" instance', exception=exception)
    return default if ObjectHelper.isNone(attributeOrMethodInstance) else attributeOrMethodInstance


def setAttributeOrMethod(instance, name, attributeOrMethodInstance, muteLogs=False):
    if ObjectHelper.isNotNone(instance) and ObjectHelper.isNotNone(name):
        try :
            setattr(instance, name, attributeOrMethodInstance)
        except Exception as exception :
            if not muteLogs :
                LogHelper.warning(setAttributeOrMethod, f'Not possible to set "{name}:{attributeOrMethodInstance}" to "{getClassName(instance, typeClass=c.TYPE_CLASS, muteLogs=muteLogs) if ObjectHelper.isNotNone(instance) else instance}" instance', exception=exception)


def getAttributeOrMethodByNamePath(instance, namePath, muteLogs=False, default=None):
    if not (ObjectHelper.isEmpty(instance) or ObjectHelper.isEmpty(namePath) or namePath.startswith(c.DOT) or namePath.endswith(c.DOT)):
        return unsafellyGetAttributeOrMethodByNamePath(instance, namePath, muteLogs=muteLogs, default=default)
    return default


def unsafellyGetAttributeOrMethodByNamePath(instance, namePath, muteLogs=False, default=None):
    splittedMethodPath = namePath.split(c.DOT)
    if 1 > len(splittedMethodPath):
        return default if ObjectHelper.isNone(instance) else instance
    elif 1 == len(splittedMethodPath):
        return getAttributeOrMethod(instance, splittedMethodPath[0], muteLogs=muteLogs, default=default)
    else:
        return unsafellyGetAttributeOrMethodByNamePath(
            getAttributeOrMethod(instance, splittedMethodPath[0], muteLogs=muteLogs, default=default),
            StringHelper.join(splittedMethodPath[1:], character=c.DOT),
            muteLogs = muteLogs,
            default = default
        )


def getAttributeOrMethodNameList(instanceClass, muteLogs=False):
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass, muteLogs=muteLogs)
    return [
        attributeOrMethodName
        for attributeOrMethodName in dir(objectNullArgsInstance)
        if isNotPrivate(attributeOrMethodName, muteLogs=muteLogs)
    ]


def isAttributeName(attributeName, objectNullArgsInstance, muteLogs=False):
    return isNotPrivate(attributeName, muteLogs=muteLogs) and isNotMethod(objectNullArgsInstance, attributeName, muteLogs=muteLogs)


def getAttributeNameList(instanceClass, muteLogs=False):
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass, muteLogs=muteLogs)
    return [
        attributeName
        for attributeName in dir(objectNullArgsInstance)
        if isAttributeName(attributeName, objectNullArgsInstance, muteLogs=muteLogs)
    ]


def getAttributeNameListFromInstance(instance):
    if ObjectHelper.isNone(instance):
        return []
    return [
        key
        for key in [*instance.__dir__()]
        if isAttributeName(key, instance)
    ]


def getMethodNameList(instanceClass, muteLogs=False):
    objectNullArgsInstance = instanciateItWithNoArgsConstructor(instanceClass, muteLogs=muteLogs)
    return [
        methodName
        for methodName in dir(objectNullArgsInstance)
        if isNotPrivate(methodName, muteLogs=muteLogs) and isMethod(objectNullArgsInstance, methodName, muteLogs=muteLogs)
    ]


def isMethodClass(methodClass, muteLogs=False):
    return False if ObjectHelper.isNone(methodClass) else methodClass.__name__ in METHOD_TYPE_NAMES


def isNotMethodClass(methodClass, muteLogs=False):
    return False if ObjectHelper.isNone(methodClass) else not isMethodClass(methodClass, muteLogs=muteLogs)


def isMethodInstance(methodInstance, muteLogs=False):
    return isMethodClass(type(methodInstance), muteLogs=muteLogs)


def isNotMethodInstance(methodInstance, muteLogs=False):
    return not isMethodInstance(methodInstance, muteLogs=muteLogs)


def isMethod(objectInstance, name, muteLogs=False):
    if ObjectHelper.isNone(objectInstance) or StringHelper.isBlank(name):
        return False
    return isMethodInstance(getAttributeOrMethod(objectInstance, name, muteLogs=muteLogs), muteLogs=muteLogs)


def isNotMethod(objectInstance, name, muteLogs=False):
    if ObjectHelper.isNone(objectInstance) or StringHelper.isBlank(name):
        return False
    return isNotMethodInstance(getAttributeOrMethod(objectInstance, name, muteLogs=muteLogs), muteLogs=muteLogs)


def isFunction(methodInstance):
    return isinstance(methodInstance, type(thisIsAFunction))


def isNotFunction(methodInstance):
    return not isFunction(methodInstance)


def instanciateItWithNoArgsConstructor(targetClass, amountOfNoneArgs=0, args=None, muteLogs=False):
    if ObjectHelper.isNone(args):
        args = []
    for _ in range(amountOfNoneArgs):
        args.append(None)
    objectInstance = None
    possibleExceptions = set()
    for _ in range(MAXIMUN_ARGUMENTS):
        try :
            objectInstance = targetClass(*args)
            break
        except Exception as exception:
            possibleExceptions.add(str(exception))
            args.append(None)
    if not isinstance(objectInstance, targetClass):
        raise Exception(f'Not possible to instanciate {getClassName(targetClass, typeClass=c.TYPE_CLASS, muteLogs=muteLogs)} with None as args constructor{c.BLANK if ObjectHelper.isEmpty(possibleExceptions) else f". Possible causes: {possibleExceptions}"}')
    return objectInstance


def getArgsOrder(targetClass, muteLogs=False):
    noneArgs = []
    noneInstance = instanciateItWithNoArgsConstructor(targetClass, amountOfNoneArgs=0, args=noneArgs, muteLogs=muteLogs)
    strArgs = []
    for arg in range(len(noneArgs)):
        strArgs.append(RandomHelper.string(minimum=10))
    try :
        instance = targetClass(*strArgs)
        instanceDataDictionary = getAttributeDataDictionary(instance, muteLogs=muteLogs)
        argsOrderDictionary = {}
        for key,value in instanceDataDictionary.items():
            if StringHelper.isNotBlank(value):
                argsOrderDictionary[strArgs.index(value)] = key
        argsOrder = [argsOrderDictionary[key] for key in sorted(argsOrderDictionary)]
    except Exception as exception :
        errorMessage = f'Not possible to get args order from "{getName(targetClass)}" target class'
        LogHelper.error(getArgsOrder, errorMessage, exception)
        raise Exception(errorMessage)
    return argsOrder


def isNotPrivate(attributeOrMethodName, muteLogs=False):
    return StringHelper.isNotBlank(attributeOrMethodName) and (
        not attributeOrMethodName.startswith(f'{2 * c.UNDERSCORE}') and
        not attributeOrMethodName.startswith(c.UNDERSCORE) and
        not ObjectHelper.METADATA_NAME == attributeOrMethodName
    )


def getAttributePointerList(instance, muteLogs=False):
    return [
        getattr(instance, instanceAttributeOrMethodName)
        for instanceAttributeOrMethodName in dir(instance)
        if isNotPrivate(instanceAttributeOrMethodName, muteLogs=muteLogs)
    ]


def getAttributeDataList(instance, muteLogs=False):
    return [
        (
            getattr(instance, instanceAttributeName),
            instanceAttributeName
        )
        for instanceAttributeName in dir(instance)
        if isAttributeName(instanceAttributeName, instance, muteLogs=muteLogs)
    ]


def getInstanceDataList(instance, muteLogs=False):
    return [
        (
            getattr(instance, instanceAttributeName),
            instanceAttributeName
        )
        for instanceAttributeName in dir(instance)
        if isNotPrivate(instanceAttributeName, muteLogs=muteLogs)
    ]


def getAttributeDataDictionary(instance, muteLogs=False):
    '''It can be a function, but not a method...'''
    # instanceDataDictionary = {}
    # for name in dir(instance):
    #     if isAttributeName(name, instance, muteLogs=muteLogs):
    #         instanceDataDictionary[name] = getattr(instance, name)
    # return instanceDataDictionary
    return {
        name: getattr(instance, name)
        for name in dir(instance)
        if isAttributeName(name, instance, muteLogs=muteLogs)
    }


def overrideSignatures(toOverride, original, forceName=None, forceModuleName=None):
    try :
        if ObjectHelper.isNotNone(original):
            toOverride.__name__ = original.__name__ if ObjectHelper.isNone(forceName) else set(forceName)
            toOverride.__qualname__ = original.__qualname__ if ObjectHelper.isNone(forceName) else set(forceName)
            toOverride.__module__ = original.__module__ if ObjectHelper.isNone(forceName) else set(c.NOTHING)
        else :
            toOverride.__name__ = forceName if ObjectHelper.isNotNone(forceName) else set(toOverride.__name__)
            toOverride.__qualname__ = forceName if ObjectHelper.isNotNone(forceName) else set(toOverride.__qualname__)
            toOverride.__module__ = forceModuleName if ObjectHelper.isNotNone(forceModuleName) else set(toOverride.__module__)
    except Exception as exception :
        LogHelper.error(overrideSignatures, f'''Not possible to override signatures of {toOverride} by signatures of {original} method''', exception)
        raise exception


def getClass(thing, typeClass=None, muteLogs=False):
    thingClass = None
    try :
        if ObjectHelper.isNone(thing):
            thingClass = typeClass
        else :
            # thingClass = thing.__class__
            thingClass = thing if isClass(thing) else thing.__class__
    except Exception as exception :
        thingClass = type(None)
        if not muteLogs :
            LogHelper.warning(getClass, f'Not possible to get class of {thing}. Returning {thingClass} insted', exception=exception)
    return thingClass


def getName(thing, typeName=None, muteLogs=False):
    name = None
    try :
        if ObjectHelper.isEmpty(thing): ###- shouldn't it be `if ObjectHelper.isNone(thing)`
            name = getUndefindeName(typeName)
        else :
            name = thing.__name__
    except Exception as exception :
        name = getUndefindeName(typeName)
        if not muteLogs :
            LogHelper.warning(getName, f'Not possible to get name of {thing}. Returning {name} insted', exception=exception)
    return name


def getClassName(thing, typeClass=None, muteLogs=False):
    name = None
    try :
        if ObjectHelper.isNone(thing):
            name = NONE_VALUE_NAME
        else :
            name = getName(getClass(thing, muteLogs=muteLogs), muteLogs=muteLogs)
    except Exception as exception :
        name = getUndefindeName(typeClass)
        if not muteLogs :
            LogHelper.warning(getClassName, f'Not possible to get class name of {thing}. Returning {name} insted', exception=exception)
    return name


def isClass(thing, typeClass=None, muteLogs=False):
    itIs = False
    try :
        if ObjectHelper.isNone(thing):
            itIs = False
        else :
            itIs = ObjectHelper.equals(str(type(thing)), str(type))
    except Exception as exception :
        if not muteLogs :
            LogHelper.warning(getClassName, f'Not possible to evaluate if {thing} is a class. Returning {itIs} by default', exception=exception)
    return itIs


def getMethodClassName(instanceClass):
    return instanceClass.__qualname__.split(c.DOT)[0]


def getModuleName(thing, typeModule=None, muteLogs=False):
    name = None
    try :
        if ObjectHelper.isEmpty(thing):
            name = getUndefindeName(typeModule)
        else :
            name = thing.__module__.split(c.DOT)[-1]
    except Exception as exception :
        name = getUndefindeName(typeModule)
        if not muteLogs :
            LogHelper.warning(getModuleName, f'Not possible to get module name of {thing}. Returning {name} insted', exception=exception)
    return name


def getMethodModuleNameDotName(instance):
    return f'{getModuleName(instance)}{c.DOT}{getName(instance)}'


def getUndefindeName(typeThing):
    if ObjectHelper.isEmpty(typeThing):
        return f'({UNDEFINED})'
    else :
        return f'({typeThing} {UNDEFINED})'


def getParentClass(instance):
    instanceParent = None
    try :
        instanceParent = unsafelyGetInstanceParent(instance)
    except Exception as exception:
        LogHelper.wrapper(getParentClass, 'Failed to get instance parent', exception)
    return instanceParent


def unsafelyGetInstanceParent(instance):
    if isinstance(instance, functools.partial):
        return unsafelyGetInstanceParent(instance.func)
    if inspect.ismethod(instance) or (inspect.isbuiltin(instance) and getattr(instance, '__self__', None) is not None and getattr(instance.__self__, '__class__', None)):
        for cls in inspect.getmro(instance.__self__.__class__):
            if instance.__name__ in cls.__dict__:
                return cls
        instance = getattr(instance, '__func__', instance)
    if inspect.isfunction(instance):
        cls = getattr(inspect.getmodule(instance), instance.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0], None)
        if isinstance(cls, type):
            return cls
    return getattr(instance, '__objclass__', None)


def getItNaked(it, depthSkip=0):
    printDetails(it)
    printClass(it)
    LogHelper.debugIt(it, depthSkip=depthSkip+2)
    try :
        LogHelper.prettyPython(getAttributePointerList, 'getAttributePointerList', getAttributePointerList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getAttributeOrMethodNameList, 'getAttributeOrMethodNameList', getAttributeOrMethodNameList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getAttributeNameList, 'getAttributeNameList', getAttributeNameList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getMethodNameList, 'getMethodNameList', getMethodNameList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getInstanceDataList, 'getInstanceDataList', getInstanceDataList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getAttributeDataList, 'getAttributeDataList', getAttributeDataList(it), logLevel=LogHelper.DEBUG)
    except : pass
    try :
        LogHelper.prettyPython(getAttributeDataDictionary, 'getAttributeDataDictionary', getAttributeDataDictionary(it), logLevel=LogHelper.DEBUG)
    except : pass


def printDetails(toDetail):
    print(f'{2 * c.TAB}printDetails({toDetail}):')
    try :
        print(f'{2 * c.TAB}type({toDetail}).__name__ = {getName(type(toDetail), typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__ = {type(toDetail).__class__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__.__module__ = {type(toDetail).__class__.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}type({toDetail}).__class__.__name__ = {getName(type(toDetail).__class__, typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__name__ = {getName(toDetail.__class__, typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__module__ = {toDetail.__class__.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{toDetail}.__class__.__qualname__ = {toDetail.__class__.__qualname__}')
    except :
        pass


def printClass(instanceClass):
    print(f'{2 * c.TAB}printClass({instanceClass}):')
    try :
        print(f'{2 * c.TAB}{instanceClass}.__name__ = {getName(instanceClass, typeName=UNKNOWN_TYPE_NAME)}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{instanceClass}.__module__ = {instanceClass.__module__}')
    except :
        pass
    try :
        print(f'{2 * c.TAB}{instanceClass}.__qualname__ = {instanceClass.__qualname__}')
    except :
        pass


INNER_INSTANCE_NAME_LIST = [
    '__inner_instance__'
]


def getDefaultInstanceName(innerInstanceName, __inner_instance__):
    return f'{innerInstanceName} of class {getClassName(__inner_instance__)}: {str(__inner_instance__)}'



def replaceInnerInstanceName(__inner_instance__, instanceNameList):
    return [
        instanceName if ObjectHelper.notEquals(innerInstanceName, instanceName) else getDefaultInstanceName(innerInstanceName, __inner_instance__)
        for innerInstanceName in INNER_INSTANCE_NAME_LIST
        for instanceName in instanceNameList
    ]


def getCompleteInstanceNameList(__inner_instance__):
    if ObjectHelper.isNone(__inner_instance__):
        return [NONE_VALUE_NAME]
    frame = EnvironmentHelper.SYS._getframe()
    # import inspect
    # frame = inspect.currentframe()
    return replaceInnerInstanceName(
        __inner_instance__, 
        [
            instanceName 
            for instanceName, instanceValue in ObjectHelper.flatMap([
                # f.f_locals
                # for f in iter(lambda: frame.f_back, None)
                frame.f_back.f_back.f_back.f_back.f_back.f_back.f_back.f_locals.items(),
                frame.f_back.f_back.f_back.f_back.f_back.f_back.f_locals.items(),
                frame.f_back.f_back.f_back.f_back.f_back.f_locals.items(),  
                frame.f_back.f_back.f_back.f_back.f_locals.items(),  
                frame.f_back.f_back.f_back.f_locals.items(),  
                frame.f_back.f_back.f_locals.items(),  
                frame.f_back.f_locals.items(),
                frame.f_locals.items()
            ])
            if instanceValue is __inner_instance__
        ]
    )


def getInstanceNameList(__inner_instance__):
    accumulatedSet = set()
    def accumulateAndReturn(value):
        if value not in accumulatedSet:
            accumulatedSet.add(value)
        return value                
    nameList = [
        accumulateAndReturn(value)
        for value in getCompleteInstanceNameList(__inner_instance__)
        if value not in accumulatedSet
    ][:-1]
    # return replaceInnerInstanceName(__inner_instance__, nameList if 1 <= len(nameList) else [str(__inner_instance__)])
    return replaceInnerInstanceName(__inner_instance__, nameList if 1 <= len(nameList) else [getDefaultInstanceName('expression or value', __inner_instance__)])


def getInstanceName(__inner_instance__, depthSkip=0):
    instanceNameList = getInstanceNameList(__inner_instance__)
    return instanceNameList[0] if 1 >= len(instanceNameList) else instanceNameList[- (1 + depthSkip)]
