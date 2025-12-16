
import pandas as pd
import lightgbm

class InferenceEngine:
    def __init__(self, data_path, model_path):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self.model_path = model_path
        self.model = lightgbm.Booster(model_file=model_path)

    def predict(self, country: str, item: str, year: int) -> float:
        """
        Method to return predicted PPI for the given country and item.
        """
        # Step 1: Filter data for given country and item; drop target column 
        df_filtered = self.df.loc[
            (self.df['area'] == country) & 
            (self.df['item'] == item) &
            (self.df['year'] == year)
            ]
        
        # Guardrail to check unmatched rows
        if df_filtered.empty:
            raise ValueError('This particular country-item pair does not exist. Try another item for this country.')
        
        # Initiate list of categorical columns
        categorical_cols = ['area', 'region', 'sub_region', 'item']

        # Explicitly set categorical columns as type 'category'
        for c in categorical_cols:
            if c in df_filtered.columns:
                df_filtered[c] = df_filtered[c].astype('category')

        # Step 2: Prepare feature vector
        X_test = df_filtered.drop('producer_price_index', axis=1)

        # Step 3: Call the model and predict
        y_pred = self.model.predict(X_test)

        # Convert predicted output to native python types
        prediction = float(y_pred[0])

        return prediction



    