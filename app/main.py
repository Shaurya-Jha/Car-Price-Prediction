from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema import CarFeatures, PredictionResponse
from model import predict_price, load_artifacts

app = FastAPI(title='Car Prediction API')

@app.on_event("startup")
def startup():
    load_artifacts()

@app.get('/')
def test():
    return JSONResponse(status_code=200, content={"success": True, "message": 'this is a test route'})

@app.get('/health')
def check_health():
    return JSONResponse(status_code=200, content={"success": True, "message": 'this is a test route'})

@app.post('/predict', response_model=PredictionResponse)
def predict(features: CarFeatures):
    price = predict_price(features.model_dump())
    
    return PredictionResponse(prediction_price=price)