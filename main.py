# Load libraries
from fastapi import Request, FastAPI, HTTPException
from contextlib import asynccontextmanager
from predict_ppi import InferenceEngine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create + load heavy stuff once
    engine = InferenceEngine(
        model_path = "artifacts/lgbm_ppi.txt",
        data_path = "after_eda_before_modeling.csv"
    )
    app.state.engine = engine

    yield

# Creates a FastAPI app object
app = FastAPI(lifespan = lifespan)

# Defining /health endpoint
@app.get('/health')
def health():
    return {"status": "ok"}

# Defining /echo endpoint to learn about the query parameters
@app.get("/echo")
def echo(country: str, item: str):
    return {"country": country, "item": item}

# Defining /predict endpoint for prediction
@app.get("/predict")
def predict(country: str, item: str, request: Request, year: int = 2023):
    try:
        engine = request.app.state.engine
        prediction = engine.predict(country, item, year)
        return {"prediction": prediction}
    except ValueError:
        raise HTTPException(status_code=404, detail=f"(country={country}, item={item}, year=2023) doesn't exist.")

