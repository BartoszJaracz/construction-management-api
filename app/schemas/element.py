from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ElementResponse(BaseModel):
     ElementId: int
     ProjectId: int
     ElementTypeId: int
     Name: Optional[str] = None
     Dimensions: Optional[str] = None
     TechnicalParameters: Optional[str] = None
     CreatedAt: datetime

class ElementCreate(BaseModel):
     ProjectId: int
     ElementTypeId: int
     Name: Optional[str]
     Dimensions: Optional[str]
     TechnicalParameters: Optional[str]
     CreatedAt: datetime

class ElementMessageResponse(BaseModel):
     message: str

class ElementWithoutCalculationsResponse(BaseModel):
     ElementId: int
     ProjectId: int
     ProjectName: Optional[str]
     Name: Optional[str]
     Dimensions: Optional[str]
     TechnicalParameters: Optional[str]