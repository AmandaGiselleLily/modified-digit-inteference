import random
from python_helper.api.src.service import ObjectHelper

def updateMaximum(minimum, maximum) :
    if maximum < minimum :
        return minimum
    return maximum

def sampleCollection(collection, collectionClass, length=None) :
    if ObjectHelper.isNotNone(length) :
        if ObjectHelper.isList(collection) :
            return collectionClass(random.sample(collection, length))
        return collectionClass(random.sample(list(collection), length))
    if ObjectHelper.isList(collection) :
        return random.choice(collection)
    return random.choice(list(collection))
