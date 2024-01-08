import pandas as pd
import numpy as np

exercises = ["OHP", "Squat", "Deadlift"]
sets = [
    [ex for ex, n_sets in zip(exercises, (2, 3, 1)) for _ in range(2 * n_sets + 1)],
    [
        "Set 1 Weight",
        "Set 1 Reps",
        "Set 2 Weight",
        "Set 2 Reps",
        "Notes",
        "Set 1 Weight",
        "Set 1 Reps",
        "Set 2 Weight",
        "Set 2 Reps",
        "Set 3 Weight",
        "Set 3 Reps",
        "Notes",
        "Set 1 Weight",
        "Set 1 Reps",
        "Notes",
    ],
]

dates = ["2023-1-1", "2023-1-2", "2023-1-3"]


columns = pd.MultiIndex.from_arrays(sets)

print(columns)


df = pd.DataFrame(np.random.randn(3, 15), index=dates, columns=columns)
print(df)
df.to_csv("test.csv")

"""
x = pd.read_csv("test.csv", header=[0,1], index_col=0)
print(x)
"""

print(df["OHP", "Set 1 Weight"]["2023-1-1"])

df["OHP", "Set 1 Weight"]["2023-1-1"] = 300

print(df)

print(df.loc['2023-1-1', ('OHP', 'Set 1 Weight')])

print(df.loc['2023-1-1', ('OHP')])

df.loc['2023-1-1', ('OHP')] = (300, 2, 600, 8, 'Hello!')

print(df.loc['2023-1-1', ('OHP')])

# get columns and 
print(df.index)
print(df.columns.get_level_values(0).unique())
print(df['OHP'].columns)


exercises = ["OHP", "Squat", "Deadlift"]
sets = [
    [ex for ex, n_sets in zip(exercises, (2, 3, 1)) for _ in range(2 * n_sets + 1)],
    [
        "Set 1 Weight",
        "Set 1 Reps",
        "Set 2 Weight",
        "Set 2 Reps",
        "Notes",
        "Set 1 Weight",
        "Set 1 Reps",
        "Set 2 Weight",
        "Set 2 Reps",
        "Set 3 Weight",
        "Set 3 Reps",
        "Notes",
        "Set 1 Weight",
        "Set 1 Reps",
        "Notes",
    ],
]


sets = [["OHP"]*2, 
        ["Set 1 Weight", "Set 1 Reps"]]

dates = ["2024-1-7"]
columns = pd.MultiIndex.from_arrays(sets)
new_df = pd.DataFrame(np.random.randn(1, 2), index=dates, columns=columns)

print(new_df)

print(df.reset_index().merge(new_df.reset_index(), how='outer').set_index('index'))
print(df)