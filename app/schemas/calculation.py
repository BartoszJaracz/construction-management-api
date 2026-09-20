from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class CalculationResponse(BaseModel):
     CalculationId: int
     ElementId: int
     BendingMoment: Optional[Decimal]
     AxialForce: Optional[Decimal]
     LoadValue: Optional[Decimal]
     LoadCapacityFactor: Optional[Decimal]
     CreatedAt: datetime

class CalculationCreate(BaseModel):
     ElementId: int
     BendingMoment: Decimal
     AxialForce: Decimal
     LoadValue: Decimal
     LoadCapacityFactor: Decimal
     
class CalculationMessageResponse(BaseModel):
     CalculationId: int
     message: str
     
class CalculationNonNegativeUpdate(BaseModel):
     value: Decimal = Field(ge=0)
     
class CalculationPositiveUpdate(BaseModel):
     value: Decimal = Field(gt=0)
     
     
