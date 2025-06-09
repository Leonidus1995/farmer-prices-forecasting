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

The Python notebook files used to clean the individual raw FAOSTAT datasets can be found [here](https://github.com/Leonidus1995/farmer-prices-forecasting/tree/main/files_data_cleaning).

In parallel, a relational database was set up locally using PostgreSQL. For each cleaned dataset, a corresponding table was created in the PostgreSQL database. The cleaned data were then loaded into their respective tables using the SQLAlchemy and Pandas libraries.

Once all datasets were stored in the database, the individual tables were integrated using a series of left joins, primarily based on common keys such as area, year, and item (where applicable). These join operations were executed using SQLAlchemy in combination with Pandas.

The final integrated dataset—comprising all contextual variables aligned with historical producer prices—was then exported as a CSV file. This consolidated file served as the input for further data wrangling, feature engineering, and model development.

All files related to database creation, data loading, and data integration could be found [here](https://github.com/Leonidus1995/farmer-prices-forecasting/tree/main/database_files).


# 🛠️ Pre-processing and Feature Engineering:

# 🤖 Modeling:

# 🧪 Model Evaluation:

# 🚀 Results / Deployment: