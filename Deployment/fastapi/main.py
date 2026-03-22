# Load the libraries
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from predict import InferenceEngine
from schemas import PredictRequest, PredictResponse

@asynccontextmanager
async def lifespan(app = FastAPI):
    """
    FastAPI will call this function once when the app starts, to load heavy stuff.
    Code before the yield will run at startup.

    Benefit? 
    To avoid reloading heavy stuff at every request. 
    To make the app faster.
    """
    engine = InferenceEngine(
        model_path = 'artifacts/model.pkl',
        df_path = 'artifacts/after_eda_before_modeling.csv'
    )
    # store the engine at app.state which is a safe place for global objects 
    app.state.engine = engine

    yield


# create the FastAPI app
app = FastAPI(lifespan = lifespan)

# End-point to check status of the API
@app.get('/health')
def health():
    return {'Status': 'Ok'}

# End-point to provide information regarding the API
@app.get('/about')
def about():
    return {
        "name": "PPI Prediction API",
        "description": "Predicts Producer Price Index for crop-country pairs",
        "model_name": "LightGBM",
        "model_version": "v1",
        "trained_through_year": 2022,
        "api_version": "1.0.0"
        }

@app.post('/predict', response_model=PredictResponse)
def predict(input: PredictRequest, request: Request):
    engine = request.app.state.engine
    yhat = engine.predict(input.country, input.item, input.year)

    if input.get_history:
        history_points = engine.history(input.country, input.item, input.year, input.num_years)
    else:
        history_points = None

    return PredictResponse(
        prediction=yhat, 
        history=history_points
        )




