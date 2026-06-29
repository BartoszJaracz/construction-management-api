from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
from typing import Optional

class ProjectCreate(BaseModel):
     ProjectName: Optional[str] = None
     Scope: Optional[str] = None
     Location: Optional[str] = None
     Status: Optional[str] = None
     DueDate: date
     
class ProjectStatus(str, Enum):
     NOWY = "Nowy"
     W_TRAKCIE = "W trakcie"
     ZAKONCZONY  = "Zakonczony"
     WSTRZYMANY = "Wstrzymany"
     
class ProjectStatusUpdate(BaseModel):
    new_status: ProjectStatus
    
class ProjectResponse(BaseModel):
     ProjectId: int
     ProjectName: Optional[str] = None
     Scope: Optional[str] = None
     Location: Optional[str] = None
     Status: Optional[str] = None
     DueDate: date
     
class ProjectDashboardResponse(BaseModel):
     ProjectId: int
     ProjectName: Optional[str] = None
     Scope: Optional[str] = None
     Location: Optional[str] = None
     Status: Optional[str] = None
     DueDate: date
     ElementsCount: Optional[int] = None
     CalculationsCount: Optional[int] = None
     NotesCount: Optional[int] = None
     TotalMaterialQuantity: Optional[float] = None
     ScheduleStatus: Optional[str] = None
     
class ProjectBottleneckResponse(BaseModel):
     ProjectId: int
     ProjectName: Optional[str] = None
     ElementsWithoutCalcs: Optional[int] = None
     ElementsWithoutMaterials: Optional[int] = None
     MissingCalcsPct: Optional[int] = None
     MissingMaterialsPct: Optional[int] = None
     ProgressPct: Optional[int] = None
     DaysSinceLastActivity: Optional[int] = None
     DaysToDeadline: Optional[int] = None
     MainBottleneck: str
     BottleneckSeverity: str
     
class MessageResponse(BaseModel):
     message: str