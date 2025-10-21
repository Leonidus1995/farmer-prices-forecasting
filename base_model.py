"""
Baseline Model:

To assess the performance of our ML and DL models in predicting the target variable- 
Producer Price Index (PPI), we established a simple baseline model. This model 
predicts the 2023 PPI for each country–item pair as the average of its PPI values 
from the previous three years (2020, 2021, and 2022). Although simplistic, this 
baseline provides a useful reference point to gauge how much predictive accuracy 
is gained through more complex machine learning and deep learning approaches.
"""


# Load the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    root_mean_squared_error, r2_score, mean_absolute_error
)


# Load the dataset
df = pd.read_csv("/Users/gurjitsingh/Desktop/MS Data Science/MS_Project_Python/after_eda_before_modeling.csv")

# Filter rows where years in [2020, 2021, 2022]
df_1 = df.loc[df['year'].isin([2020, 2021, 2022])]

# Filter for required columns
df_1 = df_1[['area', 'year', 'item', 'producer_price_index']]

# Calculate the mean PPI for each (area, item) pair
df_1_grouped = df_1.groupby(['area', 'item'], as_index=False)['producer_price_index'].mean()

# Rename the PPI column as 'PPI_predicted'
df_1_grouped.rename(
    columns={
        'producer_price_index': 'PPI_predicted'
    }, inplace=True
)

# Filtering rows where the year is 2023
df_2 = df.loc[df['year']==2023]

# Filter for required columns
df_2 = df_2[['area', 'item', 'year', 'producer_price_index']]

# Rename PPI column as 'PPI_true'
df_2.rename(columns={'producer_price_index': 'PPI_true'}, inplace=True)

# Merging the two data frames to get 'PPI_true' and 'PPI_predicted' in the same 
# dataset
df_merged = df_2.merge(
    df_1_grouped,
    on = ['area', 'item'],
    how='left'
)

# Extract PPI_true and PPI_predicted
y_true = df_merged['PPI_true'].values
y_pred = df_merged['PPI_predicted'].values

# Calculate evaluation metrics to assess prediction accuracy
rmse_base = root_mean_squared_error(y_true, y_pred)
mae_base = mean_absolute_error(y_true, y_pred)
r2_base = r2_score(y_true, y_pred)

# Converting the prediction results into a dataframe
results_base = pd.Series(
    {
        'Model': 'Base',
        'n_test': len(y_pred),
        'RMSE': rmse_base,
        'MAE': mae_base,
        'R2-score': r2_base
    }
).to_frame().T

print('Evaluation results for the Base Model on test set:')
print(results_base)

# --- Make a plot of True versus Predicted PPI values ---
plt.scatter(y_true, y_pred, alpha=0.5)
plt.xlabel('True PPI Values')
plt.ylabel('Predicted PPI Values')
plt.title('Base Model: True VS Predicted', fontweight='bold')

# Add 45° reference line (y = x)
min_val = min(y_true.min(), y_pred.min())
max_val = max(y_true.max(), y_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], 'b--', linewidth=1.5, label='Perfect Prediction')

plt.legend()
plt.savefig('plots/Base_true_vs_predicted.png', dpi=360, bbox_inches='tight')
plt.show()
