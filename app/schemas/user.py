from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
     UserId: int
     FirstName: Optional[str]
     LastName: Optional[str]
     Email: Optional[str]
     Password: str
     Role: Optional[str]
     IsActive: int
     CreatedAt: datetime
     
class ProjectUserResponse(BaseModel):
     ProjectId: int
     UserId: int
     ProjectRole: Optional[str]
     
class UserMessageResponse(BaseModel):
     message: str