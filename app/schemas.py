from pydantic import BaseModel
from datetime import date
from enum import Enum

class ProjectCreate(BaseModel):
     ProjectName: str
     Scope: str
     Location: str
     Status: str
     DueDate: date
     
class ProjectStatus(str, Enum):
     NOWY = "Nowy"
     W_TRAKCIE = "W trakcie"
     ZAKONCZONY  = "Zakonczony"
     WSTRZYMANY = "Wstrzymany"
     
class ProjectStatusUpdate(BaseModel):
    new_status: ProjectStatus