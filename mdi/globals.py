import os

baseDir1 = os.path.join('/cifs/diedrichsen/data/ModifiedDigitInterference/')
baseDir2 = os.path.join('/Volumes/diedrichsen_data$/data/ModifiedDigitInterference/')

if os.path.exists(baseDir1):
    baseDir = baseDir1
elif os.path.exists(baseDir2):
    baseDir = baseDir2
else:
    print('No baseDir found')


behavDir = 'behavioural'