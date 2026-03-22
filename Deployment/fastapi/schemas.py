from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Annotated, Literal, Optional, List

class PredictRequest(BaseModel):
    country: Annotated[str, Field(..., min_length=1, description="Country name")]
    item: Annotated[str, Field(..., min_length=1, description="Commodity/Crop name")]
    year: Annotated[Literal[2023], Field(2023, description="Inference year. Currently only 2023 is supported.")]
    get_history: Annotated[bool, Field(False, description="Do you want to get historical PPI values? Default is False.")]
    num_years: Annotated[int, Field(3, ge=1, le=5, description="How many years you want to see historical PPI values for? Default is 3 and max is 5.")]

    @field_validator("country", "item")
    @classmethod  # validator cannot be an instance method. So, there is no self.
    def reject_blank(cls, v: str) -> str:
        if not v:
            raise ValueError("Must not be blank")
        else:
            return v

class HistoryPoint(BaseModel):
     year: int
     producer_price_index: float


class PredictResponse(BaseModel):
    prediction: float
    units: str = "PPI index"
    history: Optional[List[HistoryPoint]] = None 
    model: str = "LightGBM"
    model_version: str = "v1"
    trained_through_year: int = 2022

