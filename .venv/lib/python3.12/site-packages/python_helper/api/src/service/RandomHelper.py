import string as randstr
from random import randint
import random
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.helper import RandomHelperHelper
from python_helper.api.src.service import ObjectHelper

DEFAULT_MINIMUM_LENGHT = 0
DEFAULT_MAXIMUM_LENGHT = 10

def string(minimum=DEFAULT_MINIMUM_LENGHT, maximum=DEFAULT_MAXIMUM_LENGHT) :
    maximum = RandomHelperHelper.updateMaximum(minimum, maximum)
    stringRange = integer(minimum=minimum, maximum=maximum)
    return c.NOTHING.join(random.choice(randstr.ascii_uppercase + randstr.digits) for _ in range(stringRange))

def integer(minimum=DEFAULT_MINIMUM_LENGHT, maximum=DEFAULT_MAXIMUM_LENGHT) :
    maximum = RandomHelperHelper.updateMaximum(minimum, maximum)
    return randint(minimum, maximum)

def float(minimum=DEFAULT_MINIMUM_LENGHT, maximum=DEFAULT_MAXIMUM_LENGHT) :
    maximum = RandomHelperHelper.updateMaximum(minimum, maximum)
    difference = maximum - minimum
    return minimum + difference * random.random()

def sample(collection, length=None) :
    if ObjectHelper.isCollection(collection) :
        if ObjectHelper.isDictionary(collection) :
            if ObjectHelper.isNone(length) :
                key = RandomHelperHelper.sampleCollection(list(collection.keys()), list)
                return { key : collection[key] }
            sampleDictionaryKeys = RandomHelperHelper.sampleCollection(list(collection.keys()), list, length=length)
            sampleDictionary = {}
            for key in sampleDictionaryKeys :
                sampleDictionary[key] = collection[key]
            return sampleDictionary
        elif ObjectHelper.isList(collection) :
            return RandomHelperHelper.sampleCollection(collection, list, length=length)
        elif ObjectHelper.isSet(collection) :
            return RandomHelperHelper.sampleCollection(collection, set, length=length)
        elif ObjectHelper.isTuple(collection) :
            return RandomHelperHelper.sampleCollection(collection, tuple, length=length)
    raise Exception(f'The "{collection}" argument is not a collection')
