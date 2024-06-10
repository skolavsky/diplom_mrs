# %%
import pandas as pd

df_data = pd.read_csv("data/new_norm_data.csv")
# %%
grouped = df_data.groupby('>7 or <7')

df_zeros = grouped.get_group(0).sample(frac=1)
df_ones = grouped.get_group(1).sample(frac=1)
# %%

train_data = pd.concat(
    [df_zeros.iloc[int(len(df_zeros)*0.8):],
     df_ones.iloc[int(len(df_ones)*0.8):]],
    ignore_index=True
    )

train_data = train_data.sample(frac=1)

test_data = pd.concat(
    [df_zeros.iloc[:int(len(df_zeros)*0.2)],
     df_ones.iloc[:int(len(df_ones)*0.2)]],
    ignore_index=True
    )

test_data = test_data.sample(frac=1)

# %%

features = train_data.drop(columns=["Result", ">7 or <7"])
labels = train_data['>7 or <7']

# %%
import xgboost
import shap

model = xgboost.XGBRegressor().fit(features, labels)

# %%
# explain the model's predictions using SHAP
# (same syntax works for LightGBM, CatBoost, scikit-learn, transformers, Spark, etc.)
explainer = shap.Explainer(model)
shap_values = explainer(features)

# visualize the first prediction's explanation
shap.plots.bar(shap_values[:], 14)

# %%
shap.plots.beeswarm(shap_values[:], 14)
# %%
