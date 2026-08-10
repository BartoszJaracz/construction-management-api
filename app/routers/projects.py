from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.project import ProjectCreate, ProjectStatusUpdate, ProjectResponse, ProjectDashboardResponse, ProjectBottleneckResponse
from app.schemas.common import MessageResponse
from app.database import get_db
from app.schemas.exceptions import project_not_found
from app.dependencies import require_admin
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
     prefix="/projects",
     tags=["Projects"]
)



#get all projects
@router.get(
     "",
     response_model=list[ProjectResponse]
     )
def get_projects(
     db: Session = Depends(get_db)
     ):

        result = db.execute(
            text("SELECT * FROM Project")
        )

        return [
             row._mapping for row in result.all()
        ]
   
   
#get one project with project_id
@router.get(
     "/{project_id}",
     response_model=ProjectResponse
     )
def get_project(
     project_id: int,
     db: Session = Depends(get_db)
     ):
     
        result = db.execute(
            text("""
                SELECT *
                FROM Project
                WHERE ProjectId = :project_id
            """),
            {"project_id": project_id}
        )

        row = result.fetchone()

        if row is None:
          #   return {"message": "Project not found"}
          project_not_found(project_id)
          

        return ProjectResponse(
             **row._mapping
        )

   
   
#get dashboard with project_id
@router.get(
     "/dashboard/{project_id}",
     response_model=ProjectDashboardResponse
     )
def get_project_dashboard(
     project_id: int,
     db: Session = Depends(get_db)
     ):
     
     result = db.execute(
          text("""
               SELECT * FROM vw_ProjectDashboardAdvanced vpda
               WHERE vpda.ProjectId = :project_id;
          """),
          {"project_id": project_id}
     )
     
     row = result.fetchone()
     
     if row is None:
          # return {"message": "Project not found"}
          project_not_found(project_id)
     
     return ProjectDashboardResponse(
          **row._mapping
     )


#get bottlenecks with project_id
@router.get(
     "/{project_id}/bottleneck",
     response_model=ProjectBottleneckResponse
     )
def get_project_bottleneck(
     project_id: int,
     db: Session = Depends(get_db)
     ):
     
     result = db.execute(
          text("""
               SELECT * FROM vw_ProjectBottlenecks vpb
               WHERE vpb.ProjectId = :project_id;
          """),
          {"project_id": project_id}
     )
     row = result.fetchone()
     
     if row is None:
          project_not_found(project_id)
     
     return ProjectBottleneckResponse(
          **row._mapping
     )


#create project
@router.post(
     "",
     response_model=MessageResponse,
     status_code=status.HTTP_201_CREATED
     )
def create_project(
     project: ProjectCreate,
     db: Session = Depends(get_db)
):
     try:
          db.execute(
               text("""
                    INSERT INTO Project
                    (
                         ProjectName,
                         Scope,
                         Location,
                         Status,
                         DueDate,
                         CreatedAt
                    )
                    VALUES
                    (
                         :ProjectName,
                         :Scope,
                         :Location,
                         :Status,
                         :DueDate,
                         GETDATE()
                    )
               """),
               project.model_dump()
          )
          # connection.commit()
          
          db.commit()
     
     except Exception:
          #rollback if error
          # connection.rollback()
          #print rollback message
          db.rollback()
          logger.exception("Database error")
          #raise error http
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Cannot create new project"
          )
     
     return MessageResponse(
          message="Project created successfully"
     )
     
     
     
#delete project
@router.delete(
     "/{project_id}",
     status_code=status.HTTP_204_NO_CONTENT
     )
def delete_project(
     project_id: int,
     current_user = Depends(require_admin),
     db: Session = Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    DELETE FROM Project WHERE ProjectId = :project_id;     
               """),
               {"project_id": project_id},
          )
          
          db.commit()
          
     except Exception:
          db.rollback()
          logger.exception("Database error")
          raise HTTPException (
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot delete Project with ID {project_id}"
          )
          
     if result.rowcount == 0:
          project_not_found(project_id)
          
     # return {
     #      "message": f"Project with ID {project_id} deleted successfully"
     # }
     
#update project status
@router.put(
     "/{project_id}/status",
     response_model=MessageResponse,
     status_code=status.HTTP_200_OK
     )
def update_project_status(
     project_id: int,
     status_update: ProjectStatusUpdate,
     db: Session = Depends(get_db)
):
     try:
          db.execute(
               text("""
                    EXEC sp_UpdateProjectStatus
                    @ProjectId = :project_id,
                    @NewStatus = :new_status;
               """),
               {
                    "project_id": project_id,
                    "new_status": status_update.new_status.value
               }
          )
          
          db.commit()
          
     except Exception:
          db.rollback()
          logger.exception("Database error")
          raise HTTPException (
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot update project with ID {project_id}"
          )
          
     return MessageResponse (
          message= f"Status {status_update.new_status} set to project with ID {project_id}"
     )
          