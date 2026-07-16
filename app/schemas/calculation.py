from pydantic import BaseModel
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
     CreatedAt: datetime
     
class CalculationMessageResponse(BaseModel):
     message: str
     
