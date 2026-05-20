import pandas as pd
import numpy as np
import os
import globals as gl

def make_alldat():
    # Load participant.tsv file
    Tid = [100, 101, 102, 103, 104, 106, 107, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
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

# def function for substract mean

if __name__ == "__main__":

    data = make_alldat()

    # make file with one row per trial
    data.to_csv(os.path.join(gl.baseDir, gl.behavDir, 'MDI0_alltrials.csv'), index=False)

    # make file with one row per participant per condition
    data_correct = data[(data.correct==1)]
    data_correct['MovementTimeDM'] = data_correct['MovementTime'] - data_correct.groupby('SID')['MovementTime'].transform('mean')
    mean = data_correct.groupby('SID')['MovementTime'].mean(numeric_only=True).mean()
    data_g_median = data_correct.groupby(['SID', 'PosInQuartet', 'Quartet']).median(numeric_only=True).reset_index()
    data_g_median['MovementTimeDM'] += mean
    data_g_median.to_csv(os.path.join(gl.baseDir, gl.behavDir, 'MDI0_MT_median.csv'))

    # make MDI0_IPI_median.csv


