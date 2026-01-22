import pandas as pd


def make_alldat():
    # Load participant.tsv file
    Tid = ['102', '103', '104', '105', '106', '107']
    # Load and join the files
    alldat = []
    for s, sid in enumerate(Tid):
        subj = pd.read_csv(f"/home/alily/Downloads/MDI Notebooks/behavioural data/MDI0_{sid}.dat")
        subj['SN'] = s
        subj['SID'] = sid
        subj["PosInQuartet"] = (subj["TN"] - 1) % 4 + 1
        alldat.append(subj)
    data = pd.concat(alldat)
    labels_dict = {1: 'AAMA', 2: 'AARA', 3: 'AAAA'}
    data['Quartet'] = data.QuartetType.map(labels_dict)
    data['correct'] = data.numCorrectDigits == 5
    return data
