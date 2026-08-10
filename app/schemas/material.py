from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class MaterialResponse(BaseModel):
     MaterialId: int
     Name: Optional[str]
     MaterialTypeId: int
     
class MaterialUsageResponse(BaseModel):
     ElementId: int
     MaterialId: int
     UnitId: int
     Quantity: Optional[Decimal]
     UsedAt: datetime

class TopMaterialPerProjectResponse(BaseModel):
     ProjectId: int
     MaterialTypeName: Optional[str]
     MaterialName: Optional[str]
     Symbol: Optional[str]
     SharePCT: Decimal
     
class MaterialUsageAdd(BaseModel):
     UnitId: Optional[int]
     Quantity: Optional[Decimal]
