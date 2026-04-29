import pandas as pd
import numpy as np
import os
import globals as gl

def make_alldat():
    # Load participant.tsv file
    Tid = [100, 101, 102, 104, 106, 107,109,110,111,112,113,114,115,116]
    # Load and join the files
    alldat = []
    for s, sid in enumerate(Tid):
        print(f'Doing participant {sid}')
        subj = pd.read_csv(os.path.join(gl.baseDir, gl.behavDir, f"MDI0_{sid}.dat"), sep='\t')
        subj['SN'] = s
        subj['SID'] = sid
        subj["PosInQuartet"] = (subj["TN"] - 1) % 4 + 1
        alldat.append(subj)
    data = pd.concat(alldat)
    labels_dict = {1: 'AAMA', 2: 'AARA', 3: 'AAAA'}
    data['Quartet'] = data.QuartetType.map(labels_dict)
    data['planError'] = data.reactionTime1 == 5
    data['correct'] = (data.numCorrectDigits == 5) & (data.planError==False)
    RTs = data[["reactionTime1","reactionTime2","reactionTime3","reactionTime4","reactionTime5"]].to_numpy()
    data[['ipi1', 'ipi2', 'ipi3', 'ipi4']] = np.diff(RTs, axis=-1)
    return data

if __name__ == "__main__":
    data = make_alldat()
    data.to_csv('/cifs/diedrichsen/data/ModifiedDigitInterference/behavioural/MDI0_merged.csv', index=False)



