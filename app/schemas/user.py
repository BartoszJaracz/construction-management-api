from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserResponse(BaseModel):
     UserId: int
     FirstName: Optional[str]
     LastName: Optional[str]
     Email: Optional[str]
     Role: Optional[str]
     IsActive: int
     CreatedAt: datetime
     
class ProjectUserResponse(BaseModel):
     ProjectId: int
     UserId: int
     ProjectRole: Optional[str]
     
#user registration
class UserRegister(BaseModel):
     first_name: str
     last_name: str
     email: EmailStr
     password: str = Field(min_length=8, max_length=100)
     
#user login & password validation
class UserLogin(BaseModel):
     email: EmailStr
     password: str = Field(min_length=8, max_length=100)
     
#jwt token response
class TokenResponse(BaseModel):
     access_token: str
     token_type: str