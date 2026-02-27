import os

baseDir = os.path.join('/cifs/diedrichsen/data/ModifiedDigitInterference/')

if not os.path.exists(baseDir):
    baseDir = os.path.join('/Volumes/diedrichsen_data$/data/ModifiedDigitInterference/')

print(f'base directory: {baseDir}')

behavDir = 'behavioural'