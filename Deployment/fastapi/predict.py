# Load libraries
import pandas as pd
import pickle

class InferenceEngine:
    def __init__(self, df_path, model_path):
        self.df_path = df_path
        self.model_path = model_path

        # Load dataset
        self.df = pd.read_csv(self.df_path)

        # Load trained model 
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)

    def predict(self, country: str, item: str, year: int) -> float:
        # Filter the dataset
        df_test = self.df.loc[
            (self.df['area'] == country) &
            (self.df['item'] == item) &
            (self.df['year'] == year)
            ]
        
        # Check if the test set is not empty
        if df_test.empty:
            raise ValueError("No matching data found for prediction.")

        # define categorical columns for LightGBM
        cat_cols = ['area', 'item', 'region', 'sub_region']
        for col in cat_cols:
            if col in df_test.columns:
                df_test[col] = df_test[col].astype('category')

        # define input features
        x_test = df_test.drop('producer_price_index', axis=1)

        # make prediction
        y_hat = self.model.predict(x_test)

        # convert predicted outcome to native python type
        prediction = float(y_hat[0])

        return prediction
    
    # Method to return historical PPI values for given country-item pair
    def history(self, country: str, item: str, year: int, num_years: int):
        df_history = self.df.loc[
            (self.df['area'] == country) & 
            (self.df['item'] == item) &
            (self.df['year'] != year)
            ][['year','producer_price_index']]
        
        # get the last 'num_years' number of PPI values
        df_history = df_history.sort_values('year').tail(num_years)

        # convert the results into a dictionary
        df_history = df_history.set_index('year')['producer_price_index'].to_dict()

        return [
            {"year": int(y), "producer_price_index": float(p)}
            for y, p in df_history.items()
        ]


