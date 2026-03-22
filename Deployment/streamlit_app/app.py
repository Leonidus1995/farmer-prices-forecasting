import streamlit as st
import pandas as pd
import numpy as np
import requests
import os


st.set_page_config(
    page_title="PPI Prediction App",
    layout="wide",
)

st.title("Producer Price Index (PPI) Prediction App")

# access API for prediction
API_BASE_URL = os.getenv("API_BASE_URL", "").rstrip("/")
API_URL = f"{API_BASE_URL}/predict"

# load the data
@st.cache_data
def load_data():
    return pd.read_csv("data/faostat_data.csv")

data = load_data()

# extract the list of countries available
countries = data['area'].unique().tolist()


left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Please enter your inputs below: ")

    country = st.selectbox(
        "**Select the country:**",
        options= countries,
        index=countries.index('United States of America')
    )

    if country:
        items = data.loc[data['area'] == country]['item'].unique().tolist()
        item = st.selectbox(
            "**Select the crop/item:**",
            options=items 
        )

    get_history = st.selectbox(
        '**Show historical PPI values?**',
        options=[True, False],
        index=1
        )

    if get_history:
        num_years = st.selectbox(
            "**Select number of years for historical PPI values:**",
            options=[1,2,3,4,5],
            index=2
        )
    else:
        num_years = 3

if st.button("**Predict PPI**"):
    input_data = {
       'country': country,
       'item': item,
       'year': 2023,
       'get_history': get_history,
       'num_years': num_years
    }

    with st.spinner("Predicting PPI..."):
        try:
            response = requests.post(API_URL, json=input_data)

            if response.status_code == 200:
                result = response.json()

                # --- return Prediction response --- #
                st.success(
                    f"Predicted PPI value for ({country}: {item}): {result['prediction']: .3f}"
                    )
                
                # --- return historical PPI if asked --- #
                history = result.get('history')
                if history:
                    history_df = pd.DataFrame(history)
                    history_df = history_df.rename(
                        columns={
                            'year': 'Year',
                            'producer_price_index': 'Producer Price Index'
                        }
                    )
                    st.subheader("Historical PPI values:")
                    st.dataframe(history_df, use_container_width=True)

                    with right_column:
                        df = data.loc[(data['area']==country) & (data['item']==item)]
                        df['year'] = df['year'].astype('category')
                        st.line_chart(df.set_index('year')['producer_price_index'])

            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server at: {API_URL}")

