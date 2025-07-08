# 🌾 Project Overview:
Agricultural producer price—also known as farm-gate price refers to the price that farmers receive for selling their agricultural products at the point of production, typically before the products enter the broader market chain. This price excludes costs related to transportation, marketing, storage, and retail. It represents the actual income a farmer earns per unit of crop or livestock sold. 

These prices are a key economic indicator, influencing farm profitability, food security, and national agricultural planning. It’s a direct indicator of farm income. 

### Significance:
Forecasting producer prices is important because it empowers farmers to make informed production and marketing decisions, supports policymakers in designing effective interventions, and helps stabilize markets. Reliable forecasts also aid in managing food supply chains and guiding investments in the agricultural sector.

However, forecasting these prices is challenging due to the complex, interdependent, and often non-linear nature of the influencing factors. These include economic trends, climate variability, input costs, trade policies, and socio-political dynamics—many of which vary across crops, countries, and time periods.

### Objective:
**In this project, we aim to forecast agricultural producer prices using multi-dimensional datasets from FAOSTAT, leveraging information on economic, environmental, geographic, input-related, and policy factors.**

We explore key questions such as:

- What are the most influential factors driving agricultural producer price trends?

- How accurately can these prices be forecasted across different regions and crop types?

The intended audience includes farmers, farm managers, agricultural scientists, economists, and policymakers. By generating forward-looking insights, this project aims to improve decision-making at the farm and policy levels, enhance market resilience, and support strategic planning in the agricultural sector.


# 📊 Data:
To build a robust forecasting model for producer prices, we’ll need to assemble not only the historical price series itself but a rich set of contextual predictors that capture the many factors driving these prices. 

Fortunately, FAOSTAT offers a centralized, open-source platform where most of these datasets are readily available. Below is a summary of the datasets we integrated into our final modeling dataset, along with the rationale for including each: 

1. **Historical Producer Prices (Target variable):**
Annual farm-gate prices for each crop or commodity, by country and year.

2. **Crop Production:** 
Includes production volumes, yield, area harvested, production indices, and production values. 
*Why:* Variability in production affects supply-side dynamics, which directly impact producer prices.

3. **Input Usage:** 
Includes consumption and trade related data for fertilizers and pesticides. 
*Why:* Input availability and costs influence production costs and profitability, thereby shaping pricing trends.

4. **Trade:**
Includes import/export quantities and values, trade indices, and indicators such as the self-sufficiency ratio and agricultural trade openness index by country and year.
*Why:* International trade dynamics and global market integration often drive domestic price fluctuations.

5. **Macro-Economic Indicators:**
Encompasses GDP, gross fixed capital formation (GFCF), and value added by agriculture, disaggregated by country and year.
*Why:* National economic health affects both consumer demand and the financial capacity of producers to invest in agriculture.

6. **Policy & Institutional Data:**
Includes data related to government expenditure and foreign direct investment (FDI) in agriculture and related fields
*Why:* Policy decisions and institutional investments can incentivize or deter production, thereby influencing market supply and pricing.

7. **Climatic & Environmental Variables:**
Includes temperature changes on land, greenhouse gas emissions from agriculture, nutrient balance, land use changes, and other environmental indicators.
*Why:* Environmental stressors and climate variability have a direct impact on agricultural productivity and yield stability.

8. **Demographics and Employment:**
Covers rural and urban population distributions as well as employment statistics within the agricultural sector.
*Why:* Demographic trends influence labor availability and consumption demand, both of which are critical to understanding producer price movements.

### Data Handling
Each dataset was individually downloaded from the FAOSTAT website in its raw CSV format. The raw data files were then cleaned and transformed using the Pandas library in Python. This preprocessing step involved operations such as renaming columns, filtering relevant rows, data transformation, and converting data types to ensure consistency across datasets.

*The Python notebook files used to clean the individual raw FAOSTAT datasets can be found [here](https://github.com/Leonidus1995/farmer-prices-forecasting/tree/main/files_data_cleaning).*

In parallel, a relational database was set up locally using PostgreSQL. For each cleaned dataset, a corresponding table was created in the PostgreSQL database. The cleaned data were then loaded into their respective tables using the SQLAlchemy and Pandas libraries.

Once all datasets were stored in the database, the individual tables were integrated using a series of left joins, primarily based on common keys such as area, year, and item (where applicable). These join operations were executed using SQLAlchemy in combination with Pandas.

The final integrated dataset—comprising all contextual variables aligned with historical producer prices—was then exported as a CSV file. This consolidated file served as the input for further data wrangling, feature engineering, and model development.

*All files related to database creation, data loading, and data integration could be found [here](https://github.com/Leonidus1995/farmer-prices-forecasting/tree/main/database_files).*


# 🛠️ Pre-processing and Feature Engineering:
The integrated dataset, created by merging individual FAOSTAT datasets, initially contained 392,856 rows and 116 features. Among these, 22 features had more than 50% missing values, and 10 of them had over 90% missingness, making them unsuitable for reliable analysis. Meanwhile, 75 features had missing values under 20%, which are more manageable.

![Before pre-processing](https://github.com/Leonidus1995/farmer-prices-forecasting/blob/main/plots/feat_dist_pre_clean.png)

Top 10 Features with >90% Missing Data:
1. laying – 97.66%
2. milk_animals – 96.27%
3. terms_of_trade – 96.19%
4. import_market_concentration_index – 95.50%
5. export_market_concentration_index – 95.46%
6. self_sufficiency_ratio – 95.23%
7. import_dependency_ratio – 95.23%
8. revealed_comparative_advantage_index – 94.95%
9. yield_or_carcass_weight – 92.30%
10. producing_animals_or_slaughtered – 92.25%

These 10 features were dropped due to the impracticality of imputing such large gaps without introducing bias.

### Strategy for Handling Features with 10–90% Missing Values
We identified 36 features with missing data between 10% and 90%. Our goal was to preserve as many of them as possible by identifying whether the missingness was concentrated in specific countries or items. Since the dataset contains 166 countries and 202 items, we examined how many of these each feature covered.

For example, the column "fdi_ag_forest_fish" has approximately 63% missing values. Upon inspection, it has data for only 101 countries but covers almost all items, suggesting that the missingness is primarily due to the absence of country-level data.

### Item-Level Filtering
We first performed item-level filtering to reduce missingness across key features. The goal was to preserve the 36 features with moderate to high missingness (10–90%) by identifying and removing items that contributed most to the data gaps.

The dataset originally included 202 items. We applied a two-step strategy to filter out problematic items:

1. **Removal of Animal-Related Items:**
We first removed 43 items related to animals and animal products. This decision was based on the observation that several of the top 10 features with >90% missingness (e.g., laying, milk_animals, yield_or_carcass_weight, and producing_animals_or_slaughtered) were exclusively associated with animal-related items. Retaining such items would not meaningfully contribute to analysis and would increase overall sparsity.

2. **Removal of Items with Systematic Missingness:**
We further removed 25 additional items that consistently lacked data across the 36 features we aimed to preserve. These items had minimal overlap with the retained features and provided little usable information.

By applying this filtering strategy, we retained 134 of the original 202 items, significantly improving data coverage across the selected features. This step was critical in reducing row-level missingness and ensuring more robust model training on the cleaned dataset.

### Country-Level Filtering
In addition to filtering items, we also performed country-level filtering to reduce missingness across key features. The goal was to retain as many countries as possible while ensuring data quality.

The dataset originally included 166 countries. We applied a two-step strategy to filter out problematic countries:

1. **Focus on Features with Sufficient Data:** 
We began by concentrating on features that had data for 100 to 131 countries. To prevent excessive country-level data loss, any features with fewer than 100 countries were dropped.

2. **Removal of Countries with Extensive Missingness:**
We observed that 71 countries had complete missingness in at least one of the 2 crucial features ('credit_to_ag_forest_fish', 'afs_employment_share_in_total_employment'). To strike a balance between retaining countries and ensuring data quality, we removed any country missing all values in both of these 2 key features.

By applying this filtering strategy, we retained 149 of the original 166 countries, significantly improving data coverage across the selected features. 

### Final Dataset After Cleaning

The dataset was reduced to 211,006 rows and 97 features. We removed the top 17 features with highest proportion of missing data (> 60%).

- 76 features now have missing values under 10%.

- 90 features have missing values under 40%.

This structured reduction minimized data loss while improving the overall quality and reliability of the dataset for modeling.

![After pre-processing](https://github.com/Leonidus1995/farmer-prices-forecasting/blob/main/plots/feat_dist_post_clean.png)

*Detailed step-by-step information about the data cleaning and pre-processing could be found [here](https://github.com/Leonidus1995/farmer-prices-forecasting/blob/main/pre_processing.ipynb).*

## Missing Data Assessment for effective Imputation Strategies
After data cleaning, the six features with the highest proportion of missing data are:  
- govt_expenditure_on_ag_forest_fish (50.00%), 
- producer_price (45.32%),
- afs_employment_share_in_total_employment (42.63%), 
- credit_to_ag_forest_fish_share_total_credit (41.29%),
- credit_to_ag_forest_fish (41.29%), and 
- aoi_credit_to_ag_forest_fish (41.29%)


Among these, the missing values in the **govt_expenditure_on_ag_forest_fish** column 
can be partially addressed by leveraging the following related variables: 
**agri_orientation_index_govt_expenditure, ag_forest_fish_share_in_total_gdp, and total_govt_expenditure**.

The Agricultural Orientation Index (AOI) for governmental expenditure is defined as:

AOI = (Agriculture's share of government expenditure) / (Agriculture's share of GDP)

where, 
Agriculture's share of government expenditure =
(govt_expenditure_on_ag_forest_fish) / (total_govt_expenditure)

Hence, 
govt_expenditure_on_ag_forest_fish =
(agri_orientation_index_govt_expenditure) ×
(ag_forest_fish_share_in_total_gdp) ×
(total_govt_expenditure)

After estimate missing values in 'govt_expenditure_on_ag_forest_fish' using the formula above, we were able to reduce the amount of missing data in feature 'govt_expenditure_on_ag_forest_fish' from 50.00% to 33.36%.

Next, the other columns with high missing data have data for 118, 123, 129 countries out of 149 total. In order to reduce the amount of missingness in these columns, we tried to find the common countries that have missing data for all these columns.

Unfortunately, there was limited overlap among these columns in terms of countries 
with missing data.

**Due to the high sparsity in the producer_price column, we opted to remove it from the dataset. Instead, we will focus on forecasting the producer_price_index, which offers more consistent coverage across countries and years.** 

Additionally, we excluded FDI-related columns from the dataset owing to their substantial missingness. However, to retain some measure of foreign investment relevance, we derived a new feature: value_added_aff_per_total_fdi, calculated as the ratio of value_added_ag_forest_fish to total_fdi_inflows for each country-year pair. Both input variables have relatively high data availability, making the resulting ratio more reliable. This new feature serves as an indicator of how the agriculture, forestry, and fisheries sectors contribute to the national economy in relation to foreign direct investment.

Since no further improvement in data completeness is achievable through external sources or transformations, we now proceed to apply data imputation techniques to address the remaining gaps. Before initiating imputation, it is essential to incorporate indicator columns that categorize countries based on geographic (e.g., region, sub_region) and economic attributes (e.g., least_developed_country, european_union_country, low_income_food_deficit_country, etc.).

These groupings are critical for informed imputation, as they enable us to estimate missing values using data from countries with similar geographic and economic profiles. For instance, imputing missing values for an African country using data from European nations would be inappropriate due to the stark differences in regional and developmental contexts. Group-based imputation ensures that such contextual nuances are respected, improving both the validity and reliability of the imputed values.

At this stage, the merged dataset contains 211,006 rows and 106 columns.

![Missingness correlation heatmap](https://github.com/Leonidus1995/farmer-prices-forecasting/blob/main/plots/heatmap_top40.png)

The heatmap shows pairwise correlations in missingness across the top 40 variables.
A value closer to 1 means those variables often missing together. 

![Matrix plot for missingness](https://github.com/Leonidus1995/farmer-prices-forecasting/blob/main/plots/matrixplot_top30.png)

![Heatmap temporal missingness](https://github.com/Leonidus1995/farmer-prices-forecasting/blob/main/plots/heatmap_missing_top30.png)

The matrix plot and temporal heatmap above effectively reveal the missingness patterns among the top 30 variables with the highest proportion of missing data. Notably, 6 of the top 9 variables are missing nearly all data during the first decade (1990–2000), including: 

- 'afs_employment_share_in_total_employment'
- 'total_employment_afs'
- 'agri_orientation_index_govt_expenditure'
- 'govt_expenditure_on_ag_forest_fish'
- 'total_govt_expenditure'
- 'area_temporary_crops'

Imputing a large and consistent block of missing values—especially spanning a 
decade—poses a significant risk of introducing bias and unrealistic trends.

To address this, we decided to proceed with two parallel datasets. The first 
retains all 106 features but restricts the time span to 2001–2024, thereby 
avoiding the need to impute the substantial early-decade gaps in the six most 
problematic features. The second dataset excludes these six features entirely, 
allowing us to preserve the full temporal coverage from 1991 to 2024 without 
introducing unreliable imputations. 


*Detailed step-by-step information about the missing data assessment process could be found [here](https://github.com/Leonidus1995/farmer-prices-forecasting/blob/main/data_imputation.ipynb).*

# 🤖 Modeling:

# 🧪 Model Evaluation:

# 🚀 Results / Deployment: