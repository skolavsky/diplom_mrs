# %%
import pandas as pd
# %%
df_data = pd.read_csv("data/new_data.csv")
# %%
df_data.columns.to_list()
# %%
df_data.min()
# %%
df_data.max()
# %%
norm_data = pd.DataFrame()
# %%
norm_data['age'] = df_data['age']/100
norm_data['BMI'] = df_data['BMI']/100
norm_data['gender'] = df_data['gender']
norm_data['1test Ex'] = df_data['1test Ex']/200
norm_data['1test In'] = df_data['1test In']/200
norm_data['ComorbAll'] = df_data['ComorbAll']
norm_data['L 109'] = df_data['L 109']/50
norm_data['LF'] = df_data['LF']/50
norm_data['ROX'] = df_data['ROX']/100
norm_data['Sp'] = df_data['Sp']/100
norm_data['SpO2'] = df_data['SpO2']/100
norm_data['O2 L/min'] = df_data['O2 L/min']/30
norm_data['Result'] = df_data['Result']
norm_data['>7 or <7'] = df_data['>7 or <7']
# %%
norm_data.to_csv("data/new_norm_data.csv", index=False)
# %%
