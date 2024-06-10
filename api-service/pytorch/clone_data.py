# %%
import pandas as pd
import random

df_data = pd.read_csv("data/new_norm_data.csv")
# %%
new_clone_data = pd.DataFrame(columns=df_data.columns)
print(new_clone_data.shape)
# %%
for _, row in df_data.iterrows():
    row1 = row.copy()
    row2 = row.copy()

    delta = row['age'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['age'] += delta
        row2['age'] -= delta
    else:
        row1['age'] -= delta
        row2['age'] += delta

    row1['age'] = round(row1['age'], 2)
    row2['age'] = round(row2['age'], 2)

    delta = row['BMI'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['BMI'] += delta
        row2['BMI'] -= delta
    else:
        row1['BMI'] -= delta
        row2['BMI'] += delta

    delta = row['1test Ex'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['1test Ex'] += delta
        row2['1test Ex'] -= delta
    else:
        row1['1test Ex'] -= delta
        row2['1test Ex'] += delta
        
    row1['1test Ex'] = round(row1['1test Ex'], 3)
    row2['1test Ex'] = round(row2['1test Ex'], 3)

    delta = row['1test In'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['1test In'] += delta
        row2['1test In'] -= delta
    else:
        row1['1test In'] -= delta
        row2['1test In'] += delta
    row1['1test In'] = round(row1['1test In'], 3)
    row2['1test In'] = round(row2['1test In'], 3)

    delta = row['L 109'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['L 109'] += delta
        row2['L 109'] -= delta
    else:
        row1['L 109'] -= delta
        row2['L 109'] += delta
    row1['L 109'] = round(row1['L 109'], 4)
    row2['L 109'] = round(row2['L 109'], 4)

    delta = row['LF'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['LF'] += delta
        row2['LF'] -= delta
    else:
        row1['LF'] -= delta
        row2['LF'] += delta
    row1['LF'] = round(row1['LF'], 4)
    row2['LF'] = round(row2['LF'], 4)

    delta = row['ROX'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['ROX'] += delta
        row2['ROX'] -= delta
    else:
        row1['ROX'] -= delta
        row2['ROX'] += delta

    delta = row['Sp'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['Sp'] += delta
        row2['Sp'] -= delta
    else:
        row1['Sp'] -= delta
        row2['Sp'] += delta
    row1['Sp'] = round(row1['Sp'], 2)
    row2['Sp'] = round(row2['Sp'], 2)

    delta = row['SpO2'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['SpO2'] += delta
        row2['SpO2'] -= delta
    else:
        row1['SpO2'] -= delta
        row2['SpO2'] += delta
    row1['SpO2'] = round(row1['SpO2'], 2)
    row2['SpO2'] = round(row2['SpO2'], 2)

    delta = row['O2 L/min'] * random.uniform(0, 0.05)
    if random.randint(0, 1) == 1:
        row1['O2 L/min'] += delta
        row2['O2 L/min'] -= delta
    else:
        row1['O2 L/min'] -= delta
        row2['O2 L/min'] += delta
    row1['O2 L/min'] = round(row1['O2 L/min'], 2)
    row2['O2 L/min'] = round(row2['O2 L/min'], 2)

    new_clone_data = pd.concat([new_clone_data, row1.to_frame().T], ignore_index=True)
    new_clone_data = pd.concat([new_clone_data, row2.to_frame().T], ignore_index=True)
print(new_clone_data.shape)
# %%
new_clone_data.to_csv("data/new_clone_data.csv", index=False)
# %%