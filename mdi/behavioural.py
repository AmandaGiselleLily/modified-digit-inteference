import pandas as pd
import numpy as np
import os
import globals as gl


def demean_column(data, column, groupby):
    """
    Demean a column within groups, preserving the grand mean.

    Subtracts each group's mean from the column values (within-subject centering),
    then adds back the grand mean so the overall scale is retained. The result is
    stored in a new column named `<column>DM`.

    Parameters
    ----------
    data : pd.DataFrame
        Input dataframe.
    column : str
        Name of the column to demean.
    groupby : str or list of str
        Column(s) to group by when computing within-group means (e.g. 'SID').

    Returns
    -------
    pd.DataFrame
        Copy of `data` with an additional `<column>DM` column containing the
        demeaned values.
    """
    data_out = data.copy()
    mean = data.groupby(groupby)[column].mean(numeric_only=True).mean()
    data_out[f'{column}DM'] = data_out[column] - data_out.groupby(groupby)[column].transform('mean') 
    data_out[f'{column}DM'] += mean

    return data_out


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

    # make MT file with one row per participant per condition
    data_correct = data[(data.correct==1)]
    data_g = data_correct.groupby(['SID', 'PosInQuartet', 'Quartet']).median(numeric_only=True).reset_index()
    data_g_demean = demean_column(data_g, column='MovementTime', groupby='SID')
    data_g_demean.to_csv(os.path.join(gl.baseDir, gl.behavDir, 'MDI0_MT_median.csv'))

    # make IPI file with one row per participant per condition
    melted_ipi = data_correct.melt(id_vars=["Quartet", 'SID', 'PosInQuartet', 'TN', 'BN'],value_vars=["ipi1","ipi2","ipi3","ipi4"], value_name="IPI", var_name="IPI_id")
    melted_ipi_g = melted_ipi.groupby(['SID', 'PosInQuartet', 'Quartet', 'IPI_id']).median(numeric_only=True).reset_index()
    melted_ipi_g_demean = demean_column(melted_ipi_g, column='IPI', groupby='SID')
    melted_ipi_g_demean.to_csv(os.path.join(gl.baseDir, gl.behavDir, 'MDI0_IPI_median.csv'))

