from numbers import Number
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import ObjectHelper, StringHelper, ReflectionHelper

def getColorValue(thing, color) :
    return color if ObjectHelper.isNotNone(color) else c.NATIVE_PROMPT_COLOR.get(
        ReflectionHelper.getName(type(thing)),
        c.DARK_BLUE
    )

def newLine(strReturn, character, prettyFunction, withColors):
    if character == strReturn[-1][-len(character):] :
        return [c.NEW_LINE]
    else :
        return [*getItAsColoredString(c.COMA, prettyFunction, withColors, color=c.COMA_PROMPT_COLOR), *c.NEW_LINE]

def getValueCollection(outterValue) :
    return outterValue if not isinstance(outterValue, set) else ObjectHelper.getSortedCollection(outterValue)

def getItAsColoredString(thing, prettyFunction, withColors, replaceBy=None, color=None) :
    thingValue = str(thing) if ObjectHelper.isNone(replaceBy) else str(replaceBy)
    return [thingValue] if not withColors else [getColorValue(thing, color), thingValue, c.RESET_COLOR]

def getFilteredAndColoredQuote(keyOrValue, string, prettyFunction, withColors, color) :
    if ObjectHelper.isNativeClassInstance(keyOrValue) and not isinstance(keyOrValue, str) :
        return [c.NOTHING] if StringHelper.prettyPython == prettyFunction else getItAsColoredString(string, prettyFunction, withColors, color=color)
    return getItAsColoredString(string, prettyFunction, withColors, color=color)

def getStrReturn(
        key,
        value,
        collectionType,
        quote,
        prettyFunction,
        tabCount,
        nullValue,
        trueValue,
        falseValue,
        withColors
    ) :
    valueValue = prettyFunction(
        value,
        quote = quote,
        tabCount = tabCount,
        nullValue = nullValue,
        trueValue = trueValue,
        falseValue = falseValue,
        withColors = withColors,
        joinAtReturn = False
    )
    if c.TYPE_DICT == collectionType :
        filteredAndColoredQuote = getFilteredAndColoredQuote(key, quote, prettyFunction, withColors, c.QUOTE_PROMPT_COLOR)
        filteredAndColoredColonSpace = getItAsColoredString(c.COLON_SPACE, prettyFunction, withColors, color=c.COLON_PROMPT_COLOR)
        return [tabCount * c.TAB, *filteredAndColoredQuote, *getItAsColoredString(key if StringHelper.prettyPython==prettyFunction else StringHelper.filterString(prettyFunction(key, quote=quote, tabCount=tabCount, nullValue=nullValue, trueValue=trueValue, falseValue=falseValue)), prettyFunction, withColors), *filteredAndColoredQuote, *filteredAndColoredColonSpace, *valueValue]
    else :
        return [tabCount * c.TAB, *valueValue]

def prettyInstance(
        outterValue,
        quote,
        prettyFunction,
        tabCount,
        nullValue,
        trueValue,
        falseValue,
        withColors=False,
        joinAtReturn=False
    ) :
    strReturn = []
    if (isinstance(outterValue, int) or isinstance(outterValue, float)) and not isinstance(outterValue, bool) :
        strReturn += getItAsColoredString(outterValue, prettyFunction, withColors)
    elif isinstance(outterValue, bool) :
        if True == outterValue:
            strReturn += getItAsColoredString(outterValue, prettyFunction, withColors, replaceBy=trueValue)
        elif False == outterValue:
            strReturn += getItAsColoredString(outterValue, prettyFunction, withColors, replaceBy=falseValue)
    elif ObjectHelper.isNone(outterValue) :
        strReturn += getItAsColoredString(outterValue, prettyFunction, withColors, replaceBy=nullValue, color=c.NONE_PROMP_COLOR)
    else :
        filteredAndColoredQuote = getFilteredAndColoredQuote(outterValue, quote, prettyFunction, withColors, c.QUOTE_PROMPT_COLOR)
        strReturn += [*filteredAndColoredQuote, *getItAsColoredString(outterValue, prettyFunction, withColors), *filteredAndColoredQuote]
    return returnStr(strReturn, joinAtReturn)

def getCollectionCharacter(collectionType, openOrClose, withColors) :
    return c.COLLECTION_TYPE.get(
        collectionType,
        c.COLLECTION_TYPE.get(c.TYPE_LIST)
    ).get(openOrClose).get(
        withColors,
        c.COLLECTION_TYPE.get(
            collectionType,
            c.COLLECTION_TYPE.get(c.TYPE_LIST)
        ).get(openOrClose).get(c.WITHOUT_COLOR)
    )

def prettyCollection(
        outterValue,
        collectionType,
        quote,
        prettyFunction,
        tabCount,
        nullValue,
        trueValue,
        falseValue,
        withColors=False,
        joinAtReturn=False
    ) :
    openCollection = getCollectionCharacter(collectionType, c.OPEN_COLLECTION, withColors)
    closeCollection = getCollectionCharacter(collectionType, c.CLOSE_COLLECTION, withColors)
    strReturn = []
    if len(outterValue) == 0 :
        strReturn += [openCollection, closeCollection]
    else :
        strReturn += [openCollection]
        tabCount += 1
        if ObjectHelper.isDictionary(outterValue) :
            for key,value in outterValue.items() :
                strReturn += newLine(strReturn, openCollection, prettyFunction, withColors)
                strReturn += getStrReturn(key, value, collectionType, quote, prettyFunction, tabCount, nullValue, trueValue, falseValue, withColors)
        else :
            for value in outterValue :
                strReturn += newLine(strReturn, openCollection, prettyFunction, withColors)
                strReturn += getStrReturn(None, value, collectionType, quote, prettyFunction, tabCount, nullValue, trueValue, falseValue, withColors)
        strReturn += [c.NEW_LINE]
        tabCount -= 1
        strReturn += [tabCount * c.TAB, closeCollection]
    return returnStr(strReturn, joinAtReturn)

def returnStr(strReturn, joinAtReturn) :
    return strReturn if not joinAtReturn else StringHelper.join(strReturn)

def isNotOneLineLongString(quoteType, thing) :
    if isinstance(thing, str) and isinstance(quoteType, str) and quoteType in [c.TRIPLE_SINGLE_QUOTE, c.TRIPLE_DOUBLE_QUOTE] :
        return not 0 == thing.count(quoteType) % 2
    else :
        return True
