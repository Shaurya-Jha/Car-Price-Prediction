from enum import Enum
from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    prediction_price: float

class FuelType(str, Enum):
    petrol = "Petrol"
    diesel = "Diesel"
    cng = "CNG"

class SellerType(str, Enum):
    dealer = "Dealer"
    individual = "Individual"

class TransmissionType(str, Enum):
    manual = "Manual"
    automatic = "Automatic"

class CarFeatures(BaseModel):
    Car_Name: str = Field(..., example="Creta")
    Year: str = Field(..., example=2014)
    Present_Price: float = Field(..., example=5.59)
    Kms_Driven: int = Field(..., example=27000)
    Fuel_Type: FuelType
    Seller_Type: SellerType
    Transmission: TransmissionType
    Owner: int = Field(..., ge=0, le=3, example=1, description="Number of previous owners starting from (0,1 or 3)")
