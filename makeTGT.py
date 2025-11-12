import pandas as pd
import numpy as np

sn = 100
BN = 10

for bl in range(BN):
    template = pd.read_csv('target/template.tgt', sep='\t')
    nQuartets = template.shape[0] // 4
    sequence = []
    for q in range(nQuartets):
        Or = np.array([np.random.randint(1, 5) for i in range(5)])
        Mo = Or.copy()
        choices = [x for x in range(1, 5) if x != Or[2]]
        Mo[2] = np.random.choice(choices)
        Un = np.array([np.random.randint(1, 5) for i in range(5)])
        for i in range(4):
            nTrial = i + q * 4
            if i == 2:
                if template.loc[nTrial, 'QuartetType'] == 1:
                    sequence.append(''.join(map(str, Mo)))
                elif template.loc[nTrial, 'QuartetType'] == 2:
                    sequence.append(''.join(map(str, Un)))
                elif template.loc[nTrial, 'QuartetType'] == 3:
                    sequence.append(''.join(map(str, Or)))
            else:
                sequence.append(''.join(map(str, Or)))

    df = template.copy()
    df['BN'] = bl
    df['quartet_id'] = np.arange(len(df)) // 4
    df['sequence'] = pd.Series(sequence)
    shuffled_ids = np.random.permutation(df['quartet_id'].unique())
    df_shuffled = df.copy()
    df_shuffled = (
        pd.concat([df_shuffled[df_shuffled['quartet_id'] == q] for q in shuffled_ids], ignore_index=True)
        .drop(columns='quartet_id')
    )
    df['QuartetType'] = df_shuffled['QuartetType']
    df['sequence'] = df_shuffled['sequence']
    df = df.drop(columns='quartet_id')
    df.to_csv(f'target/mdi_{sn}_run{bl+1}.tgt', sep='\t', index=False)