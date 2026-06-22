from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from app.schemas import ProjectCreate, ProjectStatusUpdate
from app.database import get_db
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
     prefix="/projects",
     tags=["Projects"]
)



#get all projects
@router.get("")
def get_projects(connection = Depends(get_db)):

        result = connection.execute(
            text("SELECT TOP 10 * FROM Project")
        )

        projects = []

        for row in result:
            projects.append(dict(row._mapping))

        return projects
   
   
#get one project with project_id
@router.get("/{project_id}")
def get_project(project_id: int, connection = Depends(get_db)):
     
        result = connection.execute(
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
          
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Project with id {project_id} not found"
          )

        return dict(row._mapping)
   
   
#get dashboard with project_id
@router.get("/dashboard/{project_id}")
def get_dashboard(project_id: int, connection = Depends(get_db)):
     
     result = connection.execute(
          text("""
               SELECT * FROM vw_ProjectDashboardAdvanced vpda
               WHERE vpda.ProjectId = :project_id;
          """),
          {"project_id": project_id}
     )
     
     row = result.fetchone()
     
     if row is None:
          # return {"message": "Project not found"}
          
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Project with id {project_id} not found"
          )
     
     return dict(row._mapping)


#get bottlenecks with project_id
@router.get("/{project_id}/bottleneck")
def get_project_bottleneck(project_id: int, connection = Depends(get_db)):
     
     result = connection.execute(
          text("""
               SELECT * FROM vw_ProjectBottlenecks vpb
               WHERE vpb.ProjectId = :project_id;
          """),
          {"project_id": project_id}
     )
     row = result.fetchone()
     
     if row is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND
               detail=f"Project with id {project_id} not found"
          )
     
     return dict(row._mapping)


#first post
@router.post("")
def create_project(
     project: ProjectCreate,
     connection = Depends(get_db)
):
     try:
          connection.execute(
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
     
     except Exception as e:
          #rollback if error
          # connection.rollback()
          #print rollback message
          logger.error(f"Database error: {e}")
          #raise error http
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Cannot create new project"
          )
     
     raise HTTPException(
          status_code=status.HTTP_201_CREATED
     )
     
     
     
#delete project
@router.delete("/{project_id}")
def delete_project(
     project_id: int,
     connection = Depends(get_db)
):
     try:
          connection.execute(
               text("""
                    DELETE FROM Project WHERE ProjectId = :project_id;     
               """),
               {"project_id": project_id},
          )
          
     except Exception as e:
          
          logger.error(f"Database error: {e}")
          
          raise HTTPException (
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot delete Project with ID {project_id}"
          )
          
     return {
          "message": f"Project with ID {project_id} deleted successfully"
     }
     
     
#update project status
@router.put("/{project_id}/status")
def update_project_status(
     project_id: int,
     status_update: ProjectStatusUpdate,
     connection = Depends(get_db)
):
     try:
          connection.execute(
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
          
     except Exception as e:
          
          logger.error(f"Database error: {e}")
          
          raise HTTPException (
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot update project with ID {project_id}"
          )
          
     return {
          "message": f"Status {status_update.new_status} set to project with ID {project_id}"
     }