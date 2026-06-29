from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from app.schemas import ProjectCreate, ProjectStatusUpdate, ProjectResponse, ProjectDashboardResponse, ProjectBottleneckResponse, MessageResponse
from app.database import get_db
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
     prefix="/projects",
     tags=["Projects"]
)

#httpException
def project_not_found(project_id: int):
     raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Project with ID {project_id} not found"
     )

#get all projects
@router.get("")
def get_projects(
     connection = Depends(get_db)
     ):

        result = connection.execute(
            text("SELECT TOP 10 * FROM Project")
        )

        projects = []

        for row in result:
            projects.append(dict(row._mapping))

        return projects
   
   
#get one project with project_id
@router.get(
     "/{project_id}",
     response_model=ProjectResponse
     )
def get_project(
     project_id: int,
     connection = Depends(get_db)
     ):
     
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
     connection = Depends(get_db)
     ):
     
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
     connection = Depends(get_db)
     ):
     
     result = connection.execute(
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


#first post
@router.post(
     "",
     response_model=MessageResponse,
     status_code=status.HTTP_201_CREATED
     )
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
     status_code=status.HTTP_200_OK
     )
def delete_project(
     project_id: int,
     connection = Depends(get_db)
):
     try:
          result = connection.execute(
               text("""
                    DELETE FROM Project WHERE ProjectId = :project_id;     
               """),
               {"project_id": project_id},
          )
          
     except Exception as e:
          
          logger.exception("Database error")
          
          raise HTTPException (
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot delete Project with ID {project_id}"
          )
          
     # return {
     #      "message": f"Project with ID {project_id} deleted successfully"
     # }
     
     if result.rowcount == 0:
          project_not_found(project_id)
     
#update project status
@router.put(
     "/{project_id}/status",
     response_model=MessageResponse,
     status_code=status.HTTP_202_ACCEPTED
     )
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
          
          logger.exception("Database error")
          
          raise HTTPException (
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot update project with ID {project_id}"
          )
          
     return MessageResponse (
          message= f"Status {status_update.new_status} set to project with ID {project_id}"
     )
          