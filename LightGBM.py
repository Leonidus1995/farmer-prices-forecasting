"""
LightGBM model
"""

# Load the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import lightgbm as lgb
from sklearn.metrics import (
    root_mean_squared_error, r2_score, mean_absolute_error
)
from lightgbm import LGBMRegressor
from sklearn.compose import TransformedTargetRegressor

# Load the dataset
df = pd.read_csv('/Users/gurjitsingh/Desktop/MS Data Science/MS_Project_Python/after_eda_before_modeling.csv')

# Initiate list of categorical columns
categorical_cols = ['area', 'region', 'sub_region', 'item']

# Work on a copy of the original dataset
df_1 = df.copy()


# Explicitly set categorical columns as type 'category' (LightGBM can handle the
# categorical columns internally)
for c in categorical_cols:
    if c in df_1.columns:
        df_1[c] = df_1[c].astype('category')

# Target column to be predicted
target = 'producer_price_index'

# Define training, validation, and testing sets
train_set = df_1.loc[df_1['year'] < 2022]
X_train = train_set.drop(target, axis=1)
y_train = train_set[target]

val_set = df_1.loc[df_1['year'] == 2022]
X_val = val_set.drop(target, axis=1)
y_val = val_set[target]

test_set = df_1.loc[df_1['year']==2023]
X_test = test_set.drop(target, axis=1)
y_test = test_set[target]

# Initiate the model
model = LGBMRegressor(
    objective='regression',
    n_estimators=5000,
    verbosity=-1,
    seed=42
)

# Fit the model with early stopping
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='rmse',
    callbacks=[lgb.early_stopping(stopping_rounds=200, verbose=False)]
)

# Predict on the training set
y_train_pred = model.predict(X_train, raw_score=False)

# Evaluate model predictions
rmse_1_train = root_mean_squared_error(y_train, y_train_pred)
mae_1_train = mean_absolute_error(y_train, y_train_pred)
r_score_1_train = r2_score(y_train, y_train_pred)

print("Evaluation results on Training Set:\n")

results_lgbm_train = {
    'RMSE': round(rmse_1_train, 3),
    'MAE': round(mae_1_train, 3),
    'R2-score': round(r_score_1_train, 3)
}

# Predict on the validation set
y_val_pred = model.predict(X_val, raw_score=False)

# Evaluate model predictions
rmse_1 = root_mean_squared_error(y_val, y_val_pred)
mae_1 = mean_absolute_error(y_val, y_val_pred)
r_score_1 = r2_score(y_val, y_val_pred)

print("Evaluation results on Validation Set:\n")

results_lgbm_val = {
    'RMSE': round(rmse_1, 3),
    'MAE': round(mae_1, 3),
    'R2-score': round(r_score_1, 3)
}

results_lgbm_val = pd.Series(
    {
        'Model': 'LightGBM',
        'n_test': len(y_val_pred),
        'RMSE': rmse_1,
        'MAE': mae_1,
        'R2-score': r_score_1
    }
).to_frame().T


print(results_lgbm_val)

# Plot the true versus predicted values
y_true = y_val
y_pred = y_val_pred
plt.scatter(y_true, y_pred, alpha=0.5)
plt.xlabel('True PPI Values')
plt.ylabel('Predicted PPI Values')
plt.title('LightGBM Model (without tuning): True VS Predicted', fontweight='bold')

# Add 45° reference line (y = x)
min_val = min(y_true.min(), y_pred.min())
max_val = max(y_true.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'b--', linewidth=1.5, label='Perfect Prediction')

plt.legend()
plt.savefig('plots/LightGBM_no_tuning_true_vs_predicted.png', dpi=360, bbox_inches='tight')
plt.show()


"""
To tune the hyper-parameters, lets use the manual grid search to test a bunch of 
combinations
"""

# --- Manual grid ---
results_train = []
results_val = []

# set the grid
grid = [
    {"learning_rate": 0.05, "n_estimators": 1000, "num_leaves": 63,  "min_data_in_leaf": 50,
     "feature_fraction": 0.8, "bagging_fraction": 0.8, "bagging_freq": 1, "lambda_l2": 1.0, "max_bin": 255},
    {"learning_rate": 0.05, "n_estimators": 1500, "num_leaves": 127, "min_data_in_leaf": 30,
     "feature_fraction": 0.8, "bagging_fraction": 0.8, "bagging_freq": 1, "lambda_l2": 0.5, "max_bin": 511},
    {"learning_rate": 0.05, "n_estimators": 1500, "num_leaves": 31,  "min_data_in_leaf": 100,
     "feature_fraction": 0.7, "bagging_fraction": 0.7, "bagging_freq": 1, "lambda_l2": 2.0, "max_bin": 255},
    {"learning_rate": 0.08, "n_estimators": 1000, "num_leaves": 63,  "min_data_in_leaf": 50,
     "feature_fraction": 0.8, "bagging_fraction": 0.8, "bagging_freq": 1, "lambda_l2": 1.0, "max_bin": 255},
    {"learning_rate": 0.03, "n_estimators": 2000, "num_leaves": 63,  "min_data_in_leaf": 50,
     "feature_fraction": 0.8, "bagging_fraction": 0.8, "bagging_freq": 1, "lambda_l2": 1.0, "max_bin": 255},
]

# Iterate over each combination
for i, p in enumerate(grid, 1):
    lgbm = LGBMRegressor(
        objective='regression',
        max_depth=-1,
        min_sum_hessian_in_leaf=1.0,
        min_gain_to_split=0.0,
        verbosity=-1,
        random_state=42,
        **p
    )

    # Fit the model
    lgbm.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        eval_metric='rmse',
        callbacks=[lgb.early_stopping(stopping_rounds=200, verbose=False)] 
    )

    # Predict on the training set
    y_train_pred_grid = lgbm.predict(X_train, raw_score=False)

    # Evaluate model predictions
    rmse_2_train = root_mean_squared_error(y_train, y_train_pred_grid)
    mae_2_train = mean_absolute_error(y_train, y_train_pred_grid)
    r_score_2_train = r2_score(y_train, y_train_pred_grid)

    print("Evaluation results on Training Set:\n")

    results_train.append({
        "idx": i, **p,
        "TRAIN_RMSE": rmse_2_train, "TRAIN_MAE": mae_2_train, "TRAIN_R2": r_score_2_train
    })

    # Predict on the validation set
    y_val_pred_grid = lgbm.predict(X_val, raw_score=False)

    # Evaluate model predictions
    rmse_2_val = root_mean_squared_error(y_val, y_val_pred_grid)
    mae_2_val = mean_absolute_error(y_val, y_val_pred_grid)
    r_score_2_val = r2_score(y_val, y_val_pred_grid)

    print("Evaluation results on Validation Set:\n")

    results_val.append({
        "idx": i, **p,
        "VAL_RMSE": rmse_2_val, "VAL_MAE": mae_2_val, "VAL_R2": r_score_2_val
    })




